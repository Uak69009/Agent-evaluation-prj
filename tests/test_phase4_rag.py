from agentevalops_eval.rag import (
    CitationQualityEvaluator,
    ContextPrecisionEvaluator,
    FaithfulnessEvaluator,
)
from agentevalops_schemas.eval import EvaluationStatus


def test_rag_evaluators():
    """Verify Phase 4 RAG evaluation metrics (ContextPrecision, Faithfulness, CitationQuality)."""
    # 1. Context Precision Evaluator
    cp_eval = ContextPrecisionEvaluator()
    sample_retrieval_trace = {
        "spans": [
            {
                "span_type": "retrieval",
                "retrieval": {
                    "query": "What is Python?",
                    "documents": [
                        {"id": "doc_1", "text": "Python is a programming language.", "relevance_score": 0.95},
                        {"id": "doc_2", "text": "Python is a snake species.", "relevance_score": 0.3},
                    ],
                },
            }
        ],
        "output": "Python is a high-level programming language used for AI and software engineering.",
    }
    res_cp = cp_eval.evaluate(sample_retrieval_trace)
    assert res_cp.evaluator_name == "context_precision"
    assert res_cp.score == 0.5

    # 2. Faithfulness Evaluator
    faith_eval = FaithfulnessEvaluator()
    res_faith = faith_eval.evaluate(sample_retrieval_trace)
    assert res_faith.evaluator_name == "faithfulness"
    assert res_faith.status == EvaluationStatus.PASSED

    # 3. Citation Quality Evaluator
    cite_eval = CitationQualityEvaluator()
    res_cite = cite_eval.evaluate(sample_retrieval_trace)
    assert res_cite.evaluator_name == "citation_quality"
    assert res_cite.status == EvaluationStatus.PASSED
