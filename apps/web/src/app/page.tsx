export default function HomePage() {
  return (
    <div className="space-y-8">
      <div className="bg-gradient-to-r from-indigo-950/80 via-purple-950/40 to-slate-900 border border-indigo-800/50 rounded-2xl p-8 backdrop-blur shadow-2xl">
        <span className="text-xs uppercase tracking-widest text-indigo-400 font-semibold">Phase 0 Architecture Foundation</span>
        <h1 className="text-3xl font-extrabold text-white mt-2 mb-4">
          AgentEvalOps Platform Shell
        </h1>
        <p className="text-gray-300 max-w-3xl leading-relaxed text-sm">
          Multi-tenant AI-agent evaluation and LLMOps platform designed to observe, evaluate, diagnose, test, and govern AI agents across correctness, trajectory quality, tool usage, RAG quality, reliability, safety, state integrity, latency, and cost.
        </p>
        <div className="mt-6 flex flex-wrap gap-4">
          <a
            href="/status"
            className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-500/25"
          >
            Check Environment Status
          </a>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="px-5 py-2.5 rounded-xl bg-card border border-border hover:border-gray-600 text-gray-300 font-medium text-sm transition-all"
          >
            View OpenAPI Specs (FastAPI)
          </a>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-card/80 border border-border rounded-xl p-6 hover:border-indigo-500/50 transition-colors">
          <h3 className="font-bold text-white text-base mb-2">Control Plane API</h3>
          <p className="text-xs text-gray-400 mb-4">FastAPI async control plane with SQLAlchemy 2.0 multi-tenant database schema.</p>
          <span className="inline-block px-2.5 py-1 rounded bg-indigo-950 text-indigo-400 text-xs font-mono border border-indigo-800">
            http://localhost:8000
          </span>
        </div>

        <div className="bg-card/80 border border-border rounded-xl p-6 hover:border-emerald-500/50 transition-colors">
          <h3 className="font-bold text-white text-base mb-2">Python SDK</h3>
          <p className="text-xs text-gray-400 mb-4">Lightweight client package (`agentevalops`) with HTTP retry and tracer context abstractions.</p>
          <span className="inline-block px-2.5 py-1 rounded bg-emerald-950 text-emerald-400 text-xs font-mono border border-emerald-800">
            packages/python-sdk
          </span>
        </div>

        <div className="bg-card/80 border border-border rounded-xl p-6 hover:border-purple-500/50 transition-colors">
          <h3 className="font-bold text-white text-base mb-2">Evaluator Plugin Core</h3>
          <p className="text-xs text-gray-400 mb-4">Extensible evaluation engine interfaces spanning 9 core evaluation dimensions.</p>
          <span className="inline-block px-2.5 py-1 rounded bg-purple-950 text-purple-400 text-xs font-mono border border-purple-800">
            packages/evaluator-core
          </span>
        </div>
      </div>
    </div>
  );
}
