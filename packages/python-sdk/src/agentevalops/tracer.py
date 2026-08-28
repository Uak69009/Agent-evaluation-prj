import asyncio
import logging
import time
import uuid
from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager
from datetime import UTC, datetime
from typing import Any

from agentevalops_schemas.trace import (
    LLMData,
    RetrievalData,
    SpanSchema,
    SpanStatus,
    SpanType,
    ToolCallData,
    TraceSchema,
)

logger = logging.getLogger("agentevalops.sdk.tracer")


class SpanContext:
    def __init__(
        self,
        span_id: str,
        trace_id: str,
        name: str,
        parent_span_id: str | None = None,
        span_type: SpanType = SpanType.CUSTOM,
    ):
        self.span_id = span_id
        self.trace_id = trace_id
        self.name = name
        self.parent_span_id = parent_span_id
        self.span_type = span_type
        self.start_time = datetime.now(UTC)
        self.end_time: datetime | None = None
        self.duration_ms: float | None = None
        self.status = SpanStatus.OK
        self.error_message: str | None = None
        self.input: Any = None
        self.output: Any = None
        self.attributes: dict[str, Any] = {}
        self.llm: LLMData | None = None
        self.tool_call: ToolCallData | None = None
        self.retrieval: RetrievalData | None = None
        self._start_perf = time.perf_counter()

    def set_input(self, input_data: Any) -> None:
        self.input = input_data

    def set_output(self, output_data: Any) -> None:
        self.output = output_data

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def set_llm_data(
        self,
        model: str,
        provider: str = "openai",
        prompt: Any = None,
        completion: Any = None,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
        total_tokens: int | None = None,
        cost_usd: float | None = None,
        temperature: float | None = None,
    ) -> None:
        self.span_type = SpanType.LLM
        tot = total_tokens or ((prompt_tokens or 0) + (completion_tokens or 0))
        self.llm = LLMData(
            model=model,
            provider=provider,
            prompt=prompt,
            completion=completion,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=tot,
            cost_usd=cost_usd,
            temperature=temperature,
        )

    def set_tool_call(
        self, name: str, arguments: dict[str, Any], output: Any = None, error: str | None = None
    ) -> None:
        self.span_type = SpanType.TOOL
        self.tool_call = ToolCallData(
            name=name, arguments=arguments, output=output, error=error
        )
        if error:
            self.status = SpanStatus.ERROR
            self.error_message = error

    def set_retrieval(
        self, query: str, documents: list[dict[str, Any]], top_k: int = 5
    ) -> None:
        self.span_type = SpanType.RETRIEVAL
        self.retrieval = RetrievalData(query=query, documents=documents, top_k=top_k)

    def record_exception(self, exc: Exception) -> None:
        self.status = SpanStatus.ERROR
        self.error_message = str(exc)

    def finish(self) -> None:
        if self.end_time is None:
            self.end_time = datetime.now(UTC)
            self.duration_ms = round((time.perf_counter() - self._start_perf) * 1000, 2)

    def to_schema(self) -> SpanSchema:
        self.finish()
        return SpanSchema(
            span_id=self.span_id,
            trace_id=self.trace_id,
            parent_span_id=self.parent_span_id,
            name=self.name,
            span_type=self.span_type,
            start_time=self.start_time,
            end_time=self.end_time,
            duration_ms=self.duration_ms,
            status=self.status,
            error_message=self.error_message,
            input=self.input,
            output=self.output,
            attributes=self.attributes,
            llm=self.llm,
            tool_call=self.tool_call,
            retrieval=self.retrieval,
        )


class TraceContext:
    def __init__(
        self,
        trace_id: str,
        name: str,
        agent_id: str = "default_agent",
        agent_version: str = "1.0.0",
        run_id: str | None = None,
        organization_id: str = "org_default",
        project_id: str = "proj_default",
        metadata: dict[str, Any] | None = None,
    ):
        self.trace_id = trace_id
        self.run_id = run_id or f"run_{uuid.uuid4().hex[:8]}"
        self.name = name
        self.agent_id = agent_id
        self.agent_version = agent_version
        self.organization_id = organization_id
        self.project_id = project_id
        self.metadata = metadata or {}
        self.start_time = datetime.now(UTC)
        self.end_time: datetime | None = None
        self.duration_ms: float | None = None
        self.status = SpanStatus.OK
        self.spans: list[SpanContext] = []
        self._span_stack: list[SpanContext] = []
        self._start_perf = time.perf_counter()

    def add_span(self, name: str, attributes: dict[str, Any] | None = None) -> str:
        span_id = f"span_{len(self.spans) + 1}_{uuid.uuid4().hex[:6]}"
        s_ctx = SpanContext(span_id=span_id, trace_id=self.trace_id, name=name)
        if attributes:
            s_ctx.attributes = attributes
        self.spans.append(s_ctx)
        return span_id

    @contextmanager
    def span(
        self, name: str, span_type: SpanType = SpanType.CUSTOM
    ) -> Generator[SpanContext, None, None]:
        parent_id = self._span_stack[-1].span_id if self._span_stack else None
        span_id = f"span_{len(self.spans) + 1}_{uuid.uuid4().hex[:6]}"
        s_ctx = SpanContext(
            span_id=span_id,
            trace_id=self.trace_id,
            name=name,
            parent_span_id=parent_id,
            span_type=span_type,
        )
        self.spans.append(s_ctx)
        self._span_stack.append(s_ctx)
        try:
            yield s_ctx
        except Exception as exc:
            s_ctx.record_exception(exc)
            self.status = SpanStatus.ERROR
            raise
        finally:
            s_ctx.finish()
            self._span_stack.pop()

    @asynccontextmanager
    async def aspan(
        self, name: str, span_type: SpanType = SpanType.CUSTOM
    ) -> AsyncGenerator[SpanContext, None]:
        parent_id = self._span_stack[-1].span_id if self._span_stack else None
        span_id = f"span_{len(self.spans) + 1}_{uuid.uuid4().hex[:6]}"
        s_ctx = SpanContext(
            span_id=span_id,
            trace_id=self.trace_id,
            name=name,
            parent_span_id=parent_id,
            span_type=span_type,
        )
        self.spans.append(s_ctx)
        self._span_stack.append(s_ctx)
        try:
            yield s_ctx
        except Exception as exc:
            s_ctx.record_exception(exc)
            self.status = SpanStatus.ERROR
            raise
        finally:
            s_ctx.finish()
            self._span_stack.pop()

    def finish(self) -> None:
        if self.end_time is None:
            self.end_time = datetime.now(UTC)
            self.duration_ms = round((time.perf_counter() - self._start_perf) * 1000, 2)

    def to_schema(self) -> TraceSchema:
        self.finish()
        return TraceSchema(
            trace_id=self.trace_id,
            run_id=self.run_id,
            agent_id=self.agent_id,
            agent_version=self.agent_version,
            organization_id=self.organization_id,
            project_id=self.project_id,
            start_time=self.start_time,
            end_time=self.end_time,
            duration_ms=self.duration_ms,
            status=self.status,
            metadata=self.metadata,
            spans=[s.to_schema() for s in self.spans],
        )


class AgentTracer:
    """Production Agent Telemetry Tracer."""

    def __init__(self, client: Any = None, auto_export: bool = True):
        self.client = client
        self.auto_export = auto_export

    @contextmanager
    def trace(
        self,
        name: str,
        agent_id: str = "default_agent",
        agent_version: str = "1.0.0",
        run_id: str | None = None,
        organization_id: str = "org_default",
        project_id: str = "proj_default",
        metadata: dict[str, Any] | None = None,
    ) -> Generator[TraceContext, None, None]:
        trace_id = f"trc_{uuid.uuid4().hex[:12]}"
        ctx = TraceContext(
            trace_id=trace_id,
            name=name,
            agent_id=agent_id,
            agent_version=agent_version,
            run_id=run_id,
            organization_id=organization_id,
            project_id=project_id,
            metadata=metadata,
        )
        try:
            yield ctx
        finally:
            ctx.finish()
            if self.auto_export and self.client and hasattr(self.client, "export_trace"):
                try:
                    self.client.export_trace(ctx.to_schema())
                except Exception as e:
                    logger.debug(f"Auto trace export skipped: {e}")

    @contextmanager
    def start_trace(
        self,
        name: str,
        agent_id: str = "default_agent",
        agent_version: str = "1.0.0",
        run_id: str | None = None,
        organization_id: str = "org_default",
        project_id: str = "proj_default",
        metadata: dict[str, Any] | None = None,
    ) -> Generator[TraceContext, None, None]:
        with self.trace(
            name=name,
            agent_id=agent_id,
            agent_version=agent_version,
            run_id=run_id,
            organization_id=organization_id,
            project_id=project_id,
            metadata=metadata,
        ) as ctx:
            yield ctx

    @asynccontextmanager
    async def atrace(
        self,
        name: str,
        agent_id: str = "default_agent",
        agent_version: str = "1.0.0",
        run_id: str | None = None,
        organization_id: str = "org_default",
        project_id: str = "proj_default",
        metadata: dict[str, Any] | None = None,
    ) -> AsyncGenerator[TraceContext, None]:
        trace_id = f"trc_{uuid.uuid4().hex[:12]}"
        ctx = TraceContext(
            trace_id=trace_id,
            name=name,
            agent_id=agent_id,
            agent_version=agent_version,
            run_id=run_id,
            organization_id=organization_id,
            project_id=project_id,
            metadata=metadata,
        )
        try:
            yield ctx
        finally:
            ctx.finish()
            if self.auto_export and self.client and hasattr(self.client, "export_trace"):
                try:
                    if asyncio.iscoroutinefunction(self.client.export_trace):
                        await self.client.export_trace(ctx.to_schema())
                    else:
                        self.client.export_trace(ctx.to_schema())
                except Exception as e:
                    logger.debug(f"Auto async trace export skipped: {e}")
