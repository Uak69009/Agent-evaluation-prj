export default function Loading() {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="flex items-center gap-3 text-indigo-400 font-medium text-sm animate-pulse">
        <div className="w-4 h-4 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin"></div>
        Loading AgentEvalOps Platform...
      </div>
    </div>
  );
}
