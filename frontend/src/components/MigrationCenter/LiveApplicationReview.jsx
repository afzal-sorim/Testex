import React, { useState } from 'react';
import { Globe, RefreshCw, ShieldAlert, Server, ExternalLink, Search, Copy, Check, Cpu } from 'lucide-react';

export default function LiveApplicationReview({
  runnerStatus,
  runnerPreviewUrl,
  handleRefreshPreview,
  iframeKey,
  repoName,
  runnerErrorReason,
  runnerPort,
  runnerNoUiMessage,
  runnerSwaggerUrl,
  runnerEndpoints,
  copyToClipboard,
  copiedPath,
  previewBaseUrl,
  previewSrc
}) {
  const [endpointSearch, setEndpointSearch] = useState('');

  return (
    <div className="flex flex-col h-full border border-slate-200/40 dark:border-dark-900/40 rounded-2xl overflow-hidden bg-white dark:bg-dark-950 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between px-4 pt-2 pb-2 bg-indigo-600 text-white text-xs font-bold shrink-0">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5 text-white">
            <Globe size={14} /> Live Application Preview
          </div>
        </div>
        {(runnerStatus === 'RUNNING' || runnerStatus === 'STARTING') && (
          <button onClick={handleRefreshPreview} className="hover:text-indigo-200 transition-colors flex items-center gap-1">
            <RefreshCw size={12} /> Refresh
          </button>
        )}
      </div>
      
      <div className="flex-grow relative bg-slate-50 dark:bg-dark-900 overflow-hidden flex flex-col">
        {runnerStatus === 'STARTING' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-50/90 dark:bg-dark-900/90 backdrop-blur-sm z-10 p-6 text-center">
            <div className="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-4 shadow-lg shadow-indigo-500/20"></div>
            <p className="text-slate-600 dark:text-slate-300 font-bold text-sm">Launching Application...</p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 max-w-xs">
              Resolving dependencies, establishing database connections, and starting web servers.
            </p>
          </div>
        )}

        {runnerStatus === 'IDLE' || runnerStatus === 'STOPPED' ? (
          <div className="flex-grow flex flex-col items-center justify-center text-slate-400 dark:text-slate-600 p-8 text-center bg-slate-50 dark:bg-dark-950">
            <div className="w-20 h-20 rounded-full bg-slate-100 dark:bg-dark-900 flex items-center justify-center mb-4 shadow-inner border border-slate-200/50 dark:border-dark-800/50">
              <Globe size={32} className="opacity-50" />
            </div>
            <p className="font-medium text-sm">Preview Unavailable</p>
            <p className="text-xs mt-2 max-w-xs opacity-70">
              Start the project runner to view the live application preview or test its endpoints.
            </p>
          </div>
        ) : runnerStatus === 'FAILED' ? (
          <div className="flex-grow flex flex-col items-center justify-center text-rose-500 p-8 text-center bg-rose-50/50 dark:bg-rose-900/10">
            <div className="w-20 h-20 rounded-full bg-rose-100 dark:bg-rose-900/30 flex items-center justify-center mb-4 border border-rose-200 dark:border-rose-800">
              <ShieldAlert size={32} />
            </div>
            <p className="font-bold text-sm">Application Failed to Start</p>
            <p className="text-xs mt-2 text-rose-600 dark:text-rose-400 max-w-sm">
              {runnerErrorReason || 'The application process exited unexpectedly. Check the Log Console for stack traces and error details.'}
            </p>
          </div>
        ) : runnerStatus === 'RUNNING_JAVA' ? (
          <div className="h-full overflow-y-auto bg-slate-50 dark:bg-dark-900 p-6 flex flex-col gap-6">
            <div className="bg-white dark:bg-dark-950 rounded-2xl border border-indigo-500/20 p-5 shadow-sm">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-md font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <Server className="text-indigo-500" size={18} />
                    REST API Running
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-md">
                    {runnerNoUiMessage || "This is a backend service without a web UI. Use the detected endpoints below or view the Swagger UI if available."}
                  </p>
                </div>
                <div className="px-3 py-1 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold rounded-lg border border-emerald-500/20 text-xs flex items-center gap-1.5 shadow-[0_0_12px_rgba(16,185,129,0.15)]">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" /> ONLINE
                </div>
              </div>
              
              <div className="mt-5 grid grid-cols-2 gap-4">
                <div className="bg-slate-50 dark:bg-dark-900 rounded-xl p-3 border border-slate-200/50 dark:border-dark-800/50">
                  <p className="text-xs text-slate-400 mb-1">Base URL</p>
                  <div className="flex items-center gap-2">
                    <code className="text-xs font-mono text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30 px-2 py-0.5 rounded border border-indigo-100 dark:border-indigo-800/50">
                      {previewBaseUrl}
                    </code>
                  </div>
                </div>
                {runnerSwaggerUrl && (
                  <div className="bg-slate-50 dark:bg-dark-900 rounded-xl p-3 border border-slate-200/50 dark:border-dark-800/50">
                    <p className="text-xs text-slate-400 mb-1">API Documentation</p>
                    <a 
                      href={previewBaseUrl + runnerSwaggerUrl} 
                      target="_blank" 
                      rel="noreferrer"
                      className="text-xs font-bold text-violet-600 dark:text-violet-400 hover:underline flex items-center gap-1"
                    >
                      Swagger UI <ExternalLink size={10} />
                    </a>
                  </div>
                )}
              </div>
            </div>

            {runnerEndpoints && runnerEndpoints.length > 0 && (
              <div className="flex flex-col gap-3 flex-grow">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-bold text-slate-800 dark:text-slate-200 flex items-center gap-2">
                    <Cpu size={14} className="text-slate-400" /> Detected Endpoints
                  </h4>
                  <div className="relative">
                    <Search className="absolute left-2.5 top-1.5 text-slate-400" size={12} />
                    <input
                      type="text"
                      placeholder="Filter endpoints..."
                      value={endpointSearch}
                      onChange={(e) => setEndpointSearch(e.target.value)}
                      className="text-xs bg-white dark:bg-dark-950 border border-slate-200 dark:border-dark-800 rounded-lg pl-7 pr-3 py-1.5 focus:outline-none focus:border-indigo-500 w-48 text-slate-700 dark:text-slate-300 transition-colors"
                    />
                  </div>
                </div>
                
                <div className="bg-white dark:bg-dark-950 rounded-xl border border-slate-200/50 dark:border-dark-800/50 overflow-hidden flex flex-col h-full max-h-[300px]">
                  <div className="overflow-y-auto">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-slate-50 dark:bg-dark-900/50 sticky top-0 border-b border-slate-200/50 dark:border-dark-800/50">
                        <tr>
                          <th className="px-4 py-2 font-medium text-slate-500 w-24">Method</th>
                          <th className="px-4 py-2 font-medium text-slate-500">Path</th>
                          <th className="px-4 py-2 font-medium text-slate-500 w-16"></th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100 dark:divide-dark-800/50">
                        {runnerEndpoints
                          .filter(ep => ep.path.toLowerCase().includes(endpointSearch.toLowerCase()) || ep.method.toLowerCase().includes(endpointSearch.toLowerCase()))
                          .map((ep, idx) => (
                          <tr key={idx} className="hover:bg-slate-50/50 dark:hover:bg-dark-900/50 transition-colors group">
                            <td className="px-4 py-2.5">
                              <span className={`font-mono text-[10px] px-2 py-0.5 rounded-full border ${
                                ep.method === 'GET' ? 'bg-blue-50 text-blue-600 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800/50' :
                                ep.method === 'POST' ? 'bg-emerald-50 text-emerald-600 border-emerald-200 dark:bg-emerald-900/20 dark:border-emerald-800/50' :
                                ep.method === 'PUT' ? 'bg-amber-50 text-amber-600 border-amber-200 dark:bg-amber-900/20 dark:border-amber-800/50' :
                                ep.method === 'DELETE' ? 'bg-rose-50 text-rose-600 border-rose-200 dark:bg-rose-900/20 dark:border-rose-800/50' :
                                'bg-slate-100 text-slate-600 border-slate-300 dark:bg-dark-800 dark:border-dark-700'
                              }`}>
                                {ep.method}
                              </span>
                            </td>
                            <td className="px-4 py-2.5 font-mono text-slate-600 dark:text-slate-400">
                              <div className="flex flex-col">
                                <span>{ep.path}</span>
                                {ep.class_name && <span className="text-[9px] text-slate-400 mt-0.5">{ep.class_name}.{ep.method_name}</span>}
                              </div>
                            </td>
                            <td className="px-4 py-2.5 text-right">
                              <button 
                                onClick={() => copyToClipboard(previewBaseUrl + ep.path)}
                                className="text-slate-400 hover:text-indigo-500 opacity-0 group-hover:opacity-100 transition-opacity p-1 bg-white dark:bg-dark-800 rounded shadow-sm border border-slate-200 dark:border-dark-700"
                                title="Copy full URL"
                              >
                                {copiedPath === previewBaseUrl + ep.path ? <Check size={12} className="text-emerald-500" /> : <Copy size={12} />}
                              </button>
                            </td>
                          </tr>
                        ))}
                        {runnerEndpoints.length > 0 && runnerEndpoints.filter(ep => ep.path.toLowerCase().includes(endpointSearch.toLowerCase())).length === 0 && (
                           <tr>
                             <td colSpan="3" className="px-4 py-8 text-center text-slate-400">
                               No endpoints match your search.
                             </td>
                           </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : previewSrc ? (
          <iframe
            key={iframeKey}
            src={previewSrc}
            className={`w-full h-full border-none transition-opacity duration-300 opacity-100`}
            title="Live Application Preview"
            sandbox="allow-same-origin allow-scripts allow-forms"
          />
        ) : (
          <div className="flex-grow flex items-center justify-center text-slate-400 p-8 text-center bg-slate-50 dark:bg-dark-950">
            <div>
              <Globe size={32} className="mx-auto mb-4 opacity-50" />
              <p>Application is running, but no preview URL was detected.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
