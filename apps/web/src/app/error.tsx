'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="p-8 bg-card border border-red-900/50 rounded-xl text-center max-w-lg mx-auto my-12">
      <h2 className="text-xl font-bold text-red-400 mb-2">Application Error</h2>
      <p className="text-sm text-gray-300 mb-6">{error.message || 'An unexpected error occurred.'}</p>
      <button
        onClick={() => reset()}
        className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs transition-colors"
      >
        Try again
      </button>
    </div>
  );
}
