'use client';

import { useEffect, useState } from 'react';
import { fetchHealthStatus, fetchReadinessStatus, HealthCheckResponse, ReadinessResponse } from '@/lib/api';

export default function StatusPage() {
  const [health, setHealth] = useState<HealthCheckResponse | null>(null);
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkServices = async () => {
    setLoading(true);
    setError(null);
    try {
      const [h, r] = await Promise.all([fetchHealthStatus(), fetchReadinessStatus()]);
      setHealth(h);
      setReadiness(r);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to backend services');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkServices();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Environment & Infrastructure Health</h1>
          <p className="text-sm text-gray-400">Real-time status of AgentEvalOps backend services, database, and Redis cache</p>
        </div>
        <button
          onClick={checkServices}
          className="px-4 py-2 text-xs font-semibold rounded-lg bg-card border border-border hover:bg-slate-800 text-gray-200 transition-colors"
        >
          Refresh Status
        </button>
      </div>

      {loading && (
        <div className="p-8 text-center bg-card/50 border border-border rounded-xl text-gray-400 text-sm animate-pulse">
          Checking backend connection and dependency readiness...
        </div>
      )}

      {error && (
        <div className="p-6 bg-red-950/40 border border-red-800 rounded-xl text-red-300 text-sm">
          <p className="font-semibold text-red-200 mb-1">Backend Connectivity Warning</p>
          <p>{error}</p>
          <p className="text-xs text-red-400 mt-2">
            Ensure FastAPI is running (`uv run uvicorn apps.api.app.main:app --reload`) and Docker Compose services (`postgres`, `redis`) are active.
          </p>
        </div>
      )}

      {!loading && health && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-card border border-border rounded-xl p-6">
            <h3 className="text-sm uppercase tracking-wider text-gray-400 font-semibold mb-4">FastAPI Control Plane</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between py-1 border-b border-border/50">
                <span className="text-gray-400">Status</span>
                <span className="text-emerald-400 font-semibold font-mono">{health.status}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-border/50">
                <span className="text-gray-400">Service</span>
                <span className="text-gray-200 font-mono">{health.service}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-border/50">
                <span className="text-gray-400">Environment</span>
                <span className="text-indigo-400 font-mono">{health.environment}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-gray-400">Version</span>
                <span className="text-gray-200 font-mono">{health.version}</span>
              </div>
            </div>
          </div>

          <div className="bg-card border border-border rounded-xl p-6">
            <h3 className="text-sm uppercase tracking-wider text-gray-400 font-semibold mb-4">Infrastructure Dependencies</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between py-1 border-b border-border/50">
                <span className="text-gray-400">PostgreSQL Database</span>
                <span className={`font-semibold font-mono ${readiness?.components.database === 'ok' ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {readiness?.components.database || 'checking'}
                </span>
              </div>
              <div className="flex justify-between py-1 border-b border-border/50">
                <span className="text-gray-400">Redis Cache & Queue</span>
                <span className={`font-semibold font-mono ${readiness?.components.redis === 'ok' ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {readiness?.components.redis || 'checking'}
                </span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-gray-400">Overall Readiness</span>
                <span className={`font-semibold font-mono ${readiness?.status === 'ready' ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {readiness?.status || 'degraded'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
