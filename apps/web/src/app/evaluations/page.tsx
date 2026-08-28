"use client";

import { useEffect, useState } from "react";

interface EvaluatorInfo {
  name: string;
  version: string;
  description: string;
}

interface EvalResult {
  evaluator_name: string;
  evaluator_version: string;
  score?: number | null;
  status: string;
  reason: string;
  severity: string;
}

interface EvalSuiteResponse {
  overall_status: string;
  overall_score: number;
  total_evaluators: number;
  passed_count: number;
  failed_count: number;
  results: EvalResult[];
}

export default function EvaluationsPage() {
  const [evaluators, setEvaluators] = useState<EvaluatorInfo[]>([]);
  const [lastSuite, setLastSuite] = useState<EvalSuiteResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const defaultEvaluators: EvaluatorInfo[] = [
    {
      name: "exact_match",
      version: "1.0.0",
      description: "Exact string or structure match against expected output",
    },
    {
      name: "tool_call_validity",
      version: "1.0.0",
      description: "Validates that tool calls executed successfully without schema/runtime errors",
    },
    {
      name: "latency_limit",
      version: "1.0.0",
      description: "Checks total trace execution duration against maximum allowed SLA (ms)",
    },
    {
      name: "cost_limit",
      version: "1.0.0",
      description: "Checks total USD cost and token counts against budget cap",
    },
    {
      name: "required_conditions",
      version: "1.0.0",
      description: "Validates that required strings/keywords are present in the final output",
    },
  ];

  const defaultSuite: EvalSuiteResponse = {
    overall_status: "passed",
    overall_score: 0.95,
    total_evaluators: 5,
    passed_count: 4,
    failed_count: 1,
    results: [
      {
        evaluator_name: "exact_match",
        evaluator_version: "1.0.0",
        score: 1.0,
        status: "passed",
        reason: "Output matched expected target exactly.",
        severity: "info",
      },
      {
        evaluator_name: "tool_call_validity",
        evaluator_version: "1.0.0",
        score: 1.0,
        status: "passed",
        reason: "All 3 tool calls executed successfully.",
        severity: "info",
      },
      {
        evaluator_name: "latency_limit",
        evaluator_version: "1.0.0",
        score: 1.0,
        status: "passed",
        reason: "Execution duration (1420 ms) within SLA limit (5000 ms).",
        severity: "info",
      },
      {
        evaluator_name: "cost_limit",
        evaluator_version: "1.0.0",
        score: 1.0,
        status: "passed",
        reason: "Total USD cost ($0.0012) within budget cap ($0.05).",
        severity: "info",
      },
      {
        evaluator_name: "required_conditions",
        evaluator_version: "1.0.0",
        score: 0.75,
        status: "failed",
        reason: "Missing required keyword: 'confirmation_code'.",
        severity: "medium",
      },
    ],
  };

  useEffect(() => {
    fetchEvaluators();
  }, []);

  const fetchEvaluators = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/v1/evaluations/evaluators");
      if (res.ok) {
        const json = await res.json();
        setEvaluators(json.length > 0 ? json : defaultEvaluators);
      } else {
        setEvaluators(defaultEvaluators);
      }
    } catch {
      setEvaluators(defaultEvaluators);
    }
  };

  const currentSuite = lastSuite || defaultSuite;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-950/80 via-indigo-950/40 to-slate-900 border border-emerald-800/50 rounded-2xl p-8 backdrop-blur shadow-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <span className="text-xs uppercase tracking-widest text-emerald-400 font-semibold">
              Phase 3 — Deterministic Evaluation Engine
            </span>
            <h1 className="text-3xl font-extrabold text-white mt-1 mb-2">
              Evaluation Engine & Rule Registry
            </h1>
            <p className="text-gray-300 text-sm max-w-2xl">
              Rule-based evaluation suite execution. Audit agent runs against exact matches, JSON schemas, tool validity, SLA latency limits, cost budgets, and required keywords.
            </p>
          </div>
          <div className="flex gap-3">
            <a
              href="/"
              className="px-4 py-2.5 rounded-xl bg-card border border-border hover:border-gray-600 text-gray-300 font-medium text-sm transition-all"
            >
              Trace Explorer
            </a>
            <a
              href="/analytics"
              className="px-4 py-2.5 rounded-xl bg-card border border-border hover:border-gray-600 text-gray-300 font-medium text-sm transition-all"
            >
              Observability
            </a>
          </div>
        </div>
      </div>

      {/* Summary KPI Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-card/80 border border-border rounded-xl p-5">
          <span className="text-xs text-gray-400 font-medium">Overall Suite Status</span>
          <div className="text-2xl font-bold mt-1">
            <span
              className={`px-3 py-1 rounded-full text-xs font-extrabold uppercase ${
                currentSuite.overall_status === "passed"
                  ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                  : "bg-rose-950 text-rose-400 border border-rose-800"
              }`}
            >
              {currentSuite.overall_status}
            </span>
          </div>
        </div>
        <div className="bg-card/80 border border-border rounded-xl p-5">
          <span className="text-xs text-gray-400 font-medium">Overall Score</span>
          <div className="text-2xl font-bold text-emerald-400 mt-1">
            {(currentSuite.overall_score * 100).toFixed(0)}%
          </div>
        </div>
        <div className="bg-card/80 border border-border rounded-xl p-5">
          <span className="text-xs text-gray-400 font-medium">Evaluators Executed</span>
          <div className="text-2xl font-bold text-white mt-1">
            {currentSuite.total_evaluators}
          </div>
        </div>
        <div className="bg-card/80 border border-border rounded-xl p-5">
          <span className="text-xs text-gray-400 font-medium">Passed / Failed</span>
          <div className="text-2xl font-bold mt-1 text-white">
            <span className="text-emerald-400">{currentSuite.passed_count}</span> /{" "}
            <span className="text-rose-400">{currentSuite.failed_count}</span>
          </div>
        </div>
      </div>

      {/* Registered Evaluators Catalog */}
      <div className="bg-card border border-border rounded-xl p-6 shadow-xl space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
          Registered Deterministic Evaluators Catalog
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {(evaluators.length > 0 ? evaluators : defaultEvaluators).map((e) => (
            <div
              key={e.name}
              className="bg-slate-900/60 border border-border rounded-xl p-4 hover:border-emerald-500/50 transition-all space-y-2"
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-sm font-bold text-emerald-300">{e.name}</span>
                <span className="text-xs text-gray-400 font-mono">v{e.version}</span>
              </div>
              <p className="text-xs text-gray-300 leading-relaxed">{e.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Suite Results Report */}
      <div className="bg-card border border-border rounded-xl p-6 shadow-xl space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
          Evaluation Suite Execution Report
        </h2>
        <div className="space-y-3">
          {currentSuite.results.map((r, i) => (
            <div
              key={i}
              className="p-4 rounded-xl border border-border bg-slate-900/40 flex flex-col md:flex-row md:items-center justify-between gap-3"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono font-bold text-sm text-white">{r.evaluator_name}</span>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold ${
                      r.status === "passed"
                        ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                        : "bg-rose-950 text-rose-400 border border-rose-800"
                    }`}
                  >
                    {r.status}
                  </span>
                </div>
                <p className="text-xs text-gray-300">{r.reason}</p>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-right">
                  <div className="text-xs text-gray-400">Score</div>
                  <div className="font-mono font-bold text-sm text-emerald-400">
                    {r.score !== undefined && r.score !== null ? (r.score * 100).toFixed(0) + "%" : "N/A"}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
