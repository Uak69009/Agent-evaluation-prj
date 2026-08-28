"use client";

import { useEffect, useState } from "react";

interface SpanData {
  span_id: str;
  parent_span_id?: string | null;
  name: string;
  span_type: string;
  duration_ms?: number | null;
  status: string;
  error_message?: string | null;
  input?: any;
  output?: any;
  llm?: {
    model: string;
    total_tokens?: number | null;
    cost_usd?: number | null;
  } | null;
  tool_call?: {
    name: string;
    arguments?: any;
    output?: any;
  } | null;
}

interface TraceData {
  trace_id: string;
  run_id: string;
  agent_id: string;
  agent_version: string;
  project_id: string;
  start_time: string;
  duration_ms?: number | null;
  status: string;
  spans: SpanData[];
}

export default function TraceExplorerPage() {
  const [traces, setTraces] = useState<TraceData[]>([]);
  const [selectedTrace, setSelectedTrace] = useState<TraceData | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [loading, setLoading] = useState(false);

  // Default sample trace data if backend server is offline
  const sampleTraces: TraceData[] = [
    {
      trace_id: "trc_9a8b7c6d5e4f",
      run_id: "run_88a99b",
      agent_id: "customer_support_agent",
      agent_version: "1.2.0",
      project_id: "proj_production",
      start_time: new Date(Date.now() - 120000).toISOString(),
      duration_ms: 1420.5,
      status: "ok",
      spans: [
        {
          span_id: "span_1_root",
          name: "agent_orchestration",
          span_type: "agent",
          duration_ms: 1420.5,
          status: "ok",
          input: { query: "Refund request for order #8849" },
          output: { response: "Refund processed successfully." },
        },
        {
          span_id: "span_2_llm",
          parent_span_id: "span_1_root",
          name: "gpt-4o_intent_classifier",
          span_type: "llm",
          duration_ms: 380.2,
          status: "ok",
          llm: { model: "gpt-4o", total_tokens: 240, cost_usd: 0.0012 },
        },
        {
          span_id: "span_3_tool",
          parent_span_id: "span_1_root",
          name: "stripe_refund_api",
          span_type: "tool",
          duration_ms: 650.0,
          status: "ok",
          tool_call: { name: "issue_refund", arguments: { order_id: "8849", amount: 49.99 } },
        },
      ],
    },
    {
      trace_id: "trc_1f2e3d4c5b6a",
      run_id: "run_77x88y",
      agent_id: "code_reviewer_agent",
      agent_version: "2.0.1",
      project_id: "proj_dev",
      start_time: new Date(Date.now() - 450000).toISOString(),
      duration_ms: 2890.1,
      status: "error",
      spans: [
        {
          span_id: "span_1_root",
          name: "code_analysis",
          span_type: "agent",
          duration_ms: 2890.1,
          status: "error",
          error_message: "Rate limit exceeded on GitHub API",
        },
        {
          span_id: "span_2_tool",
          parent_span_id: "span_1_root",
          name: "github_fetch_diff",
          span_type: "tool",
          duration_ms: 410.0,
          status: "error",
          error_message: "429 Too Many Requests",
          tool_call: { name: "fetch_diff", arguments: { pr_id: 104 } },
        },
      ],
    },
  ];

  useEffect(() => {
    fetchTraces();
  }, []);

  const fetchTraces = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/traces");
      if (res.ok) {
        const data = await res.json();
        setTraces(data.traces || sampleTraces);
      } else {
        setTraces(sampleTraces);
      }
    } catch {
      setTraces(sampleTraces);
    } finally {
      setLoading(false);
    }
  };

  const filteredTraces = traces.filter((t) => {
    const matchesSearch =
      t.trace_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.agent_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.run_id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === "all" || t.status.toLowerCase() === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const totalTraces = traces.length;
  const avgDuration =
    totalTraces > 0
      ? (traces.reduce((acc, t) => acc + (t.duration_ms || 0), 0) / totalTraces).toFixed(1)
      : "0";
  const errorRate =
    totalTraces > 0
      ? ((traces.filter((t) => t.status === "error").length / totalTraces) * 100).toFixed(1)
      : "0";
  const totalTokens = traces.reduce((acc, t) => {
    return (
      acc +
      t.spans.reduce((sAcc, s) => sAcc + (s.llm?.total_tokens || 0), 0)
    );
  }, 0);

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-indigo-950/80 via-purple-950/40 to-slate-900 border border-indigo-800/50 rounded-2xl p-8 backdrop-blur shadow-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <span className="text-xs uppercase tracking-widest text-indigo-400 font-semibold">
              Phase 1 — Production Trace Ingestion
            </span>
            <h1 className="text-3xl font-extrabold text-white mt-1 mb-2">
              Agent Trace Explorer
            </h1>
            <p className="text-gray-300 text-sm max-w-2xl">
              Live multi-tenant telemetry dashboard. Observe real-time agent execution spans, LLM call metrics, tool invocations, latency breakdowns, and error tracebacks.
            </p>
          </div>
          <button
            onClick={fetchTraces}
            className="self-start md:self-auto px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-500/25 flex items-center gap-2"
          >
            Refresh Traces
          </button>
        </div>
      </div>

      {/* Metrics Header Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-card/80 border border-border rounded-xl p-5">
          <span className="text-xs text-gray-400 font-medium">Total Traces</span>
          <div className="text-2xl font-bold text-white mt-1">{totalTraces}</div>
        </div>
        <div className="bg-card/80 border border-border rounded-xl p-5">
          <span className="text-xs text-gray-400 font-medium">Avg Duration</span>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{avgDuration} ms</div>
        </div>
        <div className="bg-card/80 border border-border rounded-xl p-5">
          <span className="text-xs text-gray-400 font-medium">Total Tokens</span>
          <div className="text-2xl font-bold text-purple-400 mt-1">{totalTokens.toLocaleString()}</div>
        </div>
        <div className="bg-card/80 border border-border rounded-xl p-5">
          <span className="text-xs text-gray-400 font-medium">Error Rate</span>
          <div className={`text-2xl font-bold mt-1 ${Number(errorRate) > 0 ? "text-rose-400" : "text-emerald-400"}`}>
            {errorRate}%
          </div>
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="flex flex-col sm:flex-row gap-4 justify-between items-center bg-card/50 border border-border p-4 rounded-xl">
        <input
          type="text"
          placeholder="Search by Trace ID, Agent ID, or Run ID..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full sm:w-96 px-4 py-2 rounded-lg bg-background border border-border text-sm text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
        />
        <div className="flex gap-2 items-center w-full sm:w-auto">
          <span className="text-xs text-gray-400 font-medium">Status:</span>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 rounded-lg bg-background border border-border text-sm text-white focus:outline-none focus:border-indigo-500"
          >
            <option value="all">All Statuses</option>
            <option value="ok">OK</option>
            <option value="error">ERROR</option>
          </select>
        </div>
      </div>

      {/* Traces Table */}
      <div className="bg-card border border-border rounded-xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-300">
            <thead className="bg-slate-900/80 text-xs uppercase tracking-wider text-gray-400 border-b border-border">
              <tr>
                <th className="px-6 py-4 font-semibold">Status</th>
                <th className="px-6 py-4 font-semibold">Trace ID</th>
                <th className="px-6 py-4 font-semibold">Agent & Version</th>
                <th className="px-6 py-4 font-semibold">Spans</th>
                <th className="px-6 py-4 font-semibold">Duration</th>
                <th className="px-6 py-4 font-semibold">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {filteredTraces.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                    No traces found matching your criteria.
                  </td>
                </tr>
              ) : (
                filteredTraces.map((t) => (
                  <tr key={t.trace_id} className="hover:bg-slate-900/40 transition-colors">
                    <td className="px-6 py-4">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                          t.status === "ok"
                            ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                            : "bg-rose-950 text-rose-400 border border-rose-800"
                        }`}
                      >
                        {t.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-mono text-xs text-indigo-300 font-medium">
                      {t.trace_id}
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-white font-medium">{t.agent_id}</div>
                      <div className="text-xs text-gray-400">v{t.agent_version}</div>
                    </td>
                    <td className="px-6 py-4 font-medium text-white">{t.spans.length} spans</td>
                    <td className="px-6 py-4 text-gray-300">{t.duration_ms ? `${t.duration_ms} ms` : "-"}</td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => setSelectedTrace(t)}
                        className="px-3 py-1.5 rounded-lg bg-indigo-950 hover:bg-indigo-900 text-indigo-300 border border-indigo-800 text-xs font-medium transition-all"
                      >
                        Inspect Spans
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Trace Span Tree Modal / Drawer */}
      {selectedTrace && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex justify-end">
          <div className="w-full max-w-2xl bg-slate-950 border-l border-border h-full p-6 overflow-y-auto flex flex-col justify-between">
            <div className="space-y-6">
              <div className="flex items-center justify-between border-b border-border pb-4">
                <div>
                  <span className="text-xs text-indigo-400 font-mono font-semibold">TRACE DETAIL</span>
                  <h2 className="text-xl font-bold text-white font-mono">{selectedTrace.trace_id}</h2>
                </div>
                <button
                  onClick={() => setSelectedTrace(null)}
                  className="px-3 py-1 rounded bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs"
                >
                  Close
                </button>
              </div>

              {/* Overview */}
              <div className="grid grid-cols-2 gap-4 bg-slate-900/60 p-4 rounded-xl border border-border text-xs">
                <div>
                  <span className="text-gray-400">Agent:</span>{" "}
                  <span className="text-white font-semibold">{selectedTrace.agent_id}</span>
                </div>
                <div>
                  <span className="text-gray-400">Run ID:</span>{" "}
                  <span className="text-indigo-300 font-mono">{selectedTrace.run_id}</span>
                </div>
                <div>
                  <span className="text-gray-400">Duration:</span>{" "}
                  <span className="text-white">{selectedTrace.duration_ms} ms</span>
                </div>
                <div>
                  <span className="text-gray-400">Status:</span>{" "}
                  <span
                    className={selectedTrace.status === "ok" ? "text-emerald-400 font-bold" : "text-rose-400 font-bold"}
                  >
                    {selectedTrace.status.toUpperCase()}
                  </span>
                </div>
              </div>

              {/* Span Tree Execution View */}
              <div>
                <h3 className="text-sm font-semibold text-white mb-3">Span Execution Tree</h3>
                <div className="space-y-3">
                  {selectedTrace.spans.map((s) => (
                    <div
                      key={s.span_id}
                      className={`p-4 rounded-xl border ${
                        s.parent_span_id ? "ml-4 border-slate-800 bg-slate-900/40" : "border-indigo-800/60 bg-slate-900/80"
                      }`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] uppercase font-mono font-bold ${
                              s.span_type === "llm"
                                ? "bg-purple-950 text-purple-400 border border-purple-800"
                                : s.span_type === "tool"
                                ? "bg-amber-950 text-amber-400 border border-amber-800"
                                : "bg-indigo-950 text-indigo-400 border border-indigo-800"
                            }`}
                          >
                            {s.span_type}
                          </span>
                          <span className="text-sm font-semibold text-white">{s.name}</span>
                        </div>
                        <span className="text-xs text-gray-400 font-mono">{s.duration_ms} ms</span>
                      </div>

                      {s.error_message && (
                        <div className="mt-2 p-2 rounded bg-rose-950/60 border border-rose-800 text-rose-300 text-xs font-mono">
                          Error: {s.error_message}
                        </div>
                      )}

                      {s.llm && (
                        <div className="mt-2 p-2.5 rounded bg-slate-950 border border-slate-800 text-xs space-y-1">
                          <div className="text-gray-400">
                            Model: <span className="text-purple-300 font-mono">{s.llm.model}</span>
                          </div>
                          {s.llm.total_tokens && (
                            <div className="text-gray-400">
                              Tokens: <span className="text-white font-mono">{s.llm.total_tokens}</span>
                            </div>
                          )}
                        </div>
                      )}

                      {s.tool_call && (
                        <div className="mt-2 p-2.5 rounded bg-slate-950 border border-slate-800 text-xs font-mono">
                          <div className="text-amber-400 font-semibold mb-1">Tool: {s.tool_call.name}</div>
                          <pre className="text-[11px] text-gray-300 overflow-x-auto">
                            {JSON.stringify(s.tool_call.arguments, null, 2)}
                          </pre>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
