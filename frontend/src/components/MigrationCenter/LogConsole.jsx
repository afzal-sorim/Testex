import React from 'react';
import { Terminal, Copy, Check } from 'lucide-react';

export default function LogConsole({
  runnerLogs,
  setRunnerLogs,
  copiedPath,
  copyToClipboard
}) {
  return (
    <div className="flex flex-col h-full border border-slate-200/40 dark:border-dark-900/40 rounded-2xl overflow-hidden bg-slate-950/20 dark:bg-dark-950/20">
      <div className="flex items-center gap-1.5 px-4 py-2 bg-slate-900 dark:bg-dark-950 text-white border-b border-slate-800 text-xs font-bold shrink-0">
        <Terminal size={14} /> Log Console
      </div>
      <div className="relative flex-grow bg-slate-950 p-4 font-mono text-xs overflow-hidden flex flex-col">
        <div className="absolute top-2 right-4 flex gap-2">
          <button
            onClick={() => setRunnerLogs('')}
            className="px-2 py-1 bg-slate-800/80 hover:bg-slate-700/80 text-[10px] text-slate-300 font-bold rounded transition-colors"
          >
            Clear
          </button>
          <button
            onClick={() => copyToClipboard(runnerLogs)}
            className="px-2 py-1 bg-slate-800/80 hover:bg-slate-700/80 text-[10px] text-slate-300 font-bold rounded transition-colors flex items-center gap-1"
          >
            {copiedPath === runnerLogs ? <Check size={10} /> : <Copy size={10} />} Copy
          </button>
        </div>
        <pre
          id="runner-console"
          className="flex-grow w-full overflow-y-auto leading-relaxed text-slate-200 whitespace-pre-wrap select-text pr-2 scrollbar-thin text-left"
        >
          {runnerLogs || 'Console idle. Click Run Project above to boot server...'}
        </pre>
      </div>
    </div>
  );
}
