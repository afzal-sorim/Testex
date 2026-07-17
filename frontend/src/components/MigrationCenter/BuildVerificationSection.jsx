import React from 'react';
import { CheckCircle, ShieldAlert, RefreshCw, Cpu, FileText } from 'lucide-react';

const parseGitDiff = (diffStr) => {
  if (!diffStr) return [];
  const lines = diffStr.split('\n');
  const files = [];
  let currentFile = null;
  let oldLineNum = 0;
  let newLineNum = 0;

  lines.forEach(line => {
    if (line.startsWith('diff --git')) {
      if (currentFile) files.push(currentFile);
      currentFile = { name: line.split(' b/')[1] || line, lines: [] };
    } else if (line.startsWith('@@ ')) {
      const match = line.match(/@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@/);
      if (match) {
        oldLineNum = parseInt(match[1], 10);
        newLineNum = parseInt(match[2], 10);
        currentFile.lines.push({ type: 'chunk', content: line });
      }
    } else if (currentFile) {
      if (line.startsWith('+') && !line.startsWith('+++')) {
        currentFile.lines.push({ type: 'add', content: line, newNum: newLineNum++ });
      } else if (line.startsWith('-') && !line.startsWith('---')) {
        currentFile.lines.push({ type: 'remove', content: line, oldNum: oldLineNum++ });
      } else if (!line.startsWith('---') && !line.startsWith('+++') && !line.startsWith('index ')) {
        currentFile.lines.push({ type: 'context', content: line, oldNum: oldLineNum++, newNum: newLineNum++ });
      }
    }
  });
  if (currentFile) files.push(currentFile);
  return files;
};

export default function BuildVerificationSection({ result, sectionRef }) {
  if (!result) return null;

  return (
    <div ref={sectionRef} className="space-y-6 mb-8 scroll-mt-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fadeIn">
        {/* Basic Build Verification Info */}
        <div className="p-6 glass-card flex flex-col justify-start h-full">
          <h3 className="text-md font-bold text-slate-900 dark:text-white mb-4 flex items-center justify-between">
            Build Check & Verification
          </h3>
          <div className={`p-4 rounded-xl flex items-center gap-3 border ${
            result.buildStatus?.includes('Success')
              ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-700 dark:text-emerald-400'
              : 'bg-rose-500/10 border-rose-500/20 text-rose-700 dark:text-rose-400'
          }`}>
            {result.buildStatus?.includes('Success') ? <CheckCircle size={20} /> : <ShieldAlert size={20} />}
            <div className="text-sm font-bold">{result.buildStatus}</div>
          </div>
          <h4 className="text-xs font-semibold text-slate-400 mt-6 mb-3 uppercase tracking-wider">Modified Files</h4>
          <div className="max-h-48 overflow-y-auto space-y-2 border border-slate-100 dark:border-dark-800 rounded-xl p-3 bg-slate-50/50 dark:bg-dark-900/10">
            {result.modifiedFiles && result.modifiedFiles.length > 0 ? (
              result.modifiedFiles.map((file, idx) => (
                <div key={idx} className="text-xs font-mono truncate text-slate-600 dark:text-slate-400">
                  📄 {file}
                </div>
              ))
            ) : (
              <div className="text-xs text-slate-400 italic">No files modified</div>
            )}
          </div>
        </div>

        {/* Self-Healing Fix History */}
        {result.fixHistory && result.fixHistory.length > 0 && (
          <div className="p-6 glass-card border-brand-500/20 h-full flex flex-col">
            <h3 className="text-md font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-4">
              <RefreshCw className="text-brand-500" size={18} />
              Self-Healing Execution Log
            </h3>
            <div className="space-y-4 overflow-y-auto max-h-[300px] scrollbar-thin flex-1">
              {result.fixHistory.map((history, idx) => (
                <div key={idx} className="bg-slate-50 dark:bg-dark-950/20 p-4 rounded-xl border border-slate-200/30 dark:border-dark-900/30">
                  <div className="font-bold text-xs text-brand-600 dark:text-brand-400 mb-2">Attempt #{history.attempt}</div>
                  <div className="space-y-2">
                    {history.fixes.map((fix, fidx) => (
                      <div key={fidx} className="text-xs font-mono text-slate-600 dark:text-slate-400 border-l-2 border-brand-500 pl-2">
                        <div>📄 {fix.file}</div>
                        <div className="text-emerald-600 dark:text-emerald-400">✓ Applied automated fix</div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AI Fix Suggestions */}
        {result.suggestedFixes && (
          <div className="p-6 glass-card h-full flex flex-col">
            <h3 className="text-md font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-4">
              <Cpu className="text-indigo-500" size={18} />
              AI Compile Recommendations
            </h3>
            <div className="prose dark:prose-invert max-w-none text-sm text-slate-700 dark:text-slate-300 leading-relaxed bg-white dark:bg-dark-950/50 p-6 rounded-2xl border border-slate-200 dark:border-dark-800 shadow-sm whitespace-pre-wrap font-sans overflow-y-auto max-h-[300px] scrollbar-thin flex-1">
              {result.suggestedFixes}
            </div>
          </div>
        )}
      </div>

      {/* GitHub-Style Diff Viewer */}
      {result.gitDiff && (
        <div className="p-6 glass-card animate-fadeIn mt-6">
          <h3 className="text-md font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-4">
            <FileText className="text-brand-500" size={18} />
            Migration Changes (Pull Request View)
          </h3>
          <div className="border border-slate-200 dark:border-dark-800 rounded-xl overflow-hidden bg-white dark:bg-dark-950">
            {parseGitDiff(result.gitDiff).map((file, idx) => (
              <div key={idx} className="mb-4 last:mb-0">
                <div className="bg-slate-100 dark:bg-dark-900 px-4 py-2 border-b border-slate-200 dark:border-dark-800 font-mono text-xs font-bold text-slate-700 dark:text-slate-300">
                  {file.name}
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-xs font-mono text-left border-collapse">
                    <tbody>
                      {file.lines.map((line, lidx) => (
                        <tr key={lidx} className={
                          line.type === 'add' ? 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400' :
                          line.type === 'remove' ? 'bg-rose-500/10 text-rose-700 dark:text-rose-400' :
                          line.type === 'chunk' ? 'bg-indigo-500/5 text-indigo-500 font-bold' :
                          'text-slate-600 dark:text-slate-400'
                        }>
                          <td className="px-2 py-0.5 whitespace-pre border-r border-slate-200 dark:border-dark-800/50 w-8 text-right text-slate-400 select-none">
                            {line.oldNum || ''}
                          </td>
                          <td className="px-2 py-0.5 whitespace-pre border-r border-slate-200 dark:border-dark-800/50 w-8 text-right text-slate-400 select-none">
                            {line.newNum || ''}
                          </td>
                          <td className="px-4 py-0.5 whitespace-pre w-full break-all">
                            {line.content}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
