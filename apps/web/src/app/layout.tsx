import './globals.css';
import { Metadata } from 'next';
import { siteConfig } from '@/lib/config';

export const metadata: Metadata = {
  title: siteConfig.name,
  description: siteConfig.description,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-gray-100 antialiased min-h-screen flex flex-col">
        <header className="border-b border-border bg-card/60 backdrop-blur sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/30">
                A
              </div>
              <span className="font-bold text-lg tracking-wide text-white">AgentEvalOps</span>
              <span className="text-xs bg-indigo-950 text-indigo-400 border border-indigo-800 px-2 py-0.5 rounded-full font-mono">
                v0.1.0-Phase0
              </span>
            </div>
            <nav className="flex items-center gap-6 text-sm text-gray-400">
              <a href="/" className="hover:text-white transition-colors">Overview</a>
              <a href="/status" className="hover:text-white transition-colors font-medium text-indigo-400">Environment Status</a>
              <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">FastAPI Docs</a>
            </nav>
          </div>
        </header>

        <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8">
          {children}
        </main>

        <footer className="border-t border-border bg-card/30 py-6 text-center text-xs text-gray-500">
          AgentEvalOps Platform Foundation &copy; 2026 — Production AI-Agent Evaluation & Governance
        </footer>
      </body>
    </html>
  );
}
