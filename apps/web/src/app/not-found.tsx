export default function NotFound() {
  return (
    <div className="p-12 text-center max-w-md mx-auto my-12 bg-card border border-border rounded-2xl">
      <h2 className="text-4xl font-extrabold text-indigo-400 mb-2">404</h2>
      <p className="text-lg font-semibold text-white mb-2">Page Not Found</p>
      <p className="text-xs text-gray-400 mb-6">The requested resource could not be found in AgentEvalOps.</p>
      <a
        href="/"
        className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs transition-colors"
      >
        Return to Home
      </a>
    </div>
  );
}
