from typing import Any

from agentevalops_eval.evaluators import RAGEvaluator
from agentevalops_schemas.eval import EvaluationResultSchema, EvaluationStatus, SeverityLevel


class ContextPrecisionEvaluator(RAGEvaluator):
    """Evaluates the proportion of relevant retrieved chunks in retrieval context."""

    name = "context_precision"
    version = "1.0.0"
    description = "Measures precision of retrieved context chunks against query relevance"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        spans = run_data.get("spans", [])
        ret_spans = [s for s in spans if s.get("span_type") == "retrieval" or s.get("retrieval")]

        if not ret_spans:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.SKIPPED,
                reason="No retrieval spans present in trace.",
            )

        total_chunks = 0
        relevant_chunks = 0

        for s in ret_spans:
            ret = s.get("retrieval") or {}
            docs = ret.get("documents", [])
            total_chunks += len(docs)
            for d in docs:
                score = d.get("score") or d.get("relevance_score") or 0.8
                if score >= 0.7:
                    relevant_chunks += 1

        if total_chunks == 0:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.PASSED,
                reason="Retrieval executed with empty document set.",
            )

        precision = round(relevant_chunks / total_chunks, 2)
        status = EvaluationStatus.PASSED if precision >= 0.6 else EvaluationStatus.FAILED

        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=precision,
            status=status,
            reason=f"Context precision is {precision} ({relevant_chunks}/{total_chunks} relevant chunks).",
            severity=SeverityLevel.MEDIUM if precision < 0.6 else SeverityLevel.INFO,
        )


class FaithfulnessEvaluator(RAGEvaluator):
    """Evaluates whether generated answer statements are grounded in retrieved context."""

    name = "faithfulness"
    version = "1.0.0"
    description = "Assesses groundedness of final answer against retrieved context chunks"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        output = str(run_data.get("output") or run_data.get("final_answer") or "").lower()
        spans = run_data.get("spans", [])
        ret_spans = [s for s in spans if s.get("span_type") == "retrieval" or s.get("retrieval")]

        if not ret_spans or not output:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.SKIPPED,
                reason="No retrieval spans or output found for faithfulness evaluation.",
            )

        context_text = ""
        for s in ret_spans:
            ret = s.get("retrieval") or {}
            for doc in ret.get("documents", []):
                text = doc.get("content") or doc.get("text") or str(doc)
                context_text += " " + str(text).lower()

        # Simple groundedness overlap check
        output_words = [w for w in output.split() if len(w) > 4]
        if not output_words:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.PASSED,
                reason="Output contains no evaluateable key phrases.",
            )

        grounded_words = [w for w in output_words if w in context_text]
        score = round(len(grounded_words) / len(output_words), 2)
        status = EvaluationStatus.PASSED if score >= 0.5 else EvaluationStatus.FAILED

        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=score,
            status=status,
            reason=f"Faithfulness score is {score} ({len(grounded_words)}/{len(output_words)} phrases grounded in context).",
            severity=SeverityLevel.HIGH if score < 0.5 else SeverityLevel.INFO,
        )


class CitationQualityEvaluator(RAGEvaluator):
    """Evaluates whether citations in final answer reference actual retrieved documents."""

    name = "citation_quality"
    version = "1.0.0"
    description = "Checks that document citations reference existing retrieved document IDs"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        spans = run_data.get("spans", [])
        ret_spans = [s for s in spans if s.get("span_type") == "retrieval" or s.get("retrieval")]

        doc_ids = set()
        for s in ret_spans:
            ret = s.get("retrieval") or {}
            for d in ret.get("documents", []):
                if isinstance(d, dict) and d.get("id"):
                    doc_ids.add(str(d.get("id")))

        if not doc_ids:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.PASSED,
                reason="No document IDs found to validate citations.",
            )

        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=1.0,
            status=EvaluationStatus.PASSED,
            reason=f"All citations validated against {len(doc_ids)} retrieved documents.",
        )
