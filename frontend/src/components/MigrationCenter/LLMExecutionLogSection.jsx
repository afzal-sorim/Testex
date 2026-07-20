import React from 'react';
import { FileText } from 'lucide-react';

export default function LLMExecutionLogSection({ result, sectionRef }) {
  if (!result) return null;

  return (
    <div ref={sectionRef} className="p-6 glass-card mb-8 scroll-mt-6">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-md font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <FileText className="text-indigo-500" size={18} />
          LLM Execution Log
        </h3>
        <span className={`px-3 py-1 text-xs font-bold rounded-full border ${
          result.success 
            ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-600 dark:text-emerald-400' 
            : 'bg-amber-500/10 border-amber-500/20 text-amber-600 dark:text-amber-400'
        }`}>
          {result.success ? 'LLM executed' : 'Execution Notice'}
        </span>
      </div>
      <pre className="p-4 rounded-xl bg-slate-900 text-slate-100 text-xs font-mono overflow-y-auto max-h-[500px] leading-relaxed scrollbar-thin">
        {result.migrationSummary || 'No log details generated.'}
      </pre>

      {/* Build validation logs if failed */}
      {result.buildErrors && (
        <div className="mt-6 p-6 rounded-2xl border border-rose-500/20 bg-rose-500/5">
          <h3 className="text-md font-bold text-rose-500 flex items-center gap-2 mb-4">
            <FileText size={18} />
            Compiler Error Log
          </h3>
          <pre className="p-5 rounded-2xl bg-rose-50/50 dark:bg-rose-950/20 text-rose-700 dark:text-rose-300 border border-rose-500/20 text-xs font-mono overflow-y-auto max-h-96 leading-relaxed shadow-sm scrollbar-thin">
            {result.buildErrors}
          </pre>
        </div>
      )}
    </div>
  );
}
