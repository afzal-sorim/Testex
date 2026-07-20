import React, { useState } from 'react';
import { Clock, Trash2, RefreshCw, CheckCircle, ShieldAlert } from 'lucide-react';

export default function MigrationHistorySection({ history, clearHistory, loading, sectionRef }) {
  return (
    <div ref={sectionRef} className="p-6 glass-card mb-8 scroll-mt-6">
      <section>
        <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
          <Clock className="text-brand-500" size={20} />
          Migration History
        </h3>
        <MigrationHistoryTable history={history} clearHistory={clearHistory} loading={loading} />
      </section>
    </div>
  );
}

function MigrationHistoryTable({ history, clearHistory, loading }) {
  const [activeHistoryTab, setActiveHistoryTab] = useState('all');
  const [repoFilter, setRepoFilter] = useState('all');

  const tabs = [
    { id: 'all', label: 'All Migrations' },
    { id: 'inprogress', label: 'In Progress' },
    { id: 'completed', label: 'Completed' },
    { id: 'failed', label: 'Failed' },
    { id: 'scheduled', label: 'Scheduled' },
  ];

  // Get unique repos for filter
  const uniqueRepos = [...new Set(history.map(e => e.repoUrl?.split('/').slice(-1)[0] || 'Unknown'))];

  // Generate migration ID from entry
  const getMigrationId = (entry, idx) => {
    const date = new Date(entry.id || Date.now());
    const year = date.getFullYear();
    const seq = String(history.length - idx).padStart(5, '0');
    return `MG-${year}-${seq}`;
  };

  // Get status info
  const getStatusInfo = (entry) => {
    if (loading && entry === history[0]) {
      return { label: 'In Progress', color: 'text-amber-600 dark:text-amber-400', bg: 'bg-amber-500/10', icon: '🔄', borderColor: 'border-amber-500/20' };
    }
    if (entry.buildStatus === 'Build Success' || entry.buildStatus === 'Success' || entry.success) {
      return { label: 'Completed', color: 'text-emerald-600 dark:text-emerald-400', bg: 'bg-emerald-500/10', icon: '✅', borderColor: 'border-emerald-500/20' };
    }
    if (!entry.success || (entry.buildStatus && entry.buildStatus.toLowerCase().includes('fail'))) {
      return { label: 'Failed', color: 'text-rose-600 dark:text-rose-400', bg: 'bg-rose-500/10', icon: '❌', borderColor: 'border-rose-500/20' };
    }
    return { label: 'Completed', color: 'text-emerald-600 dark:text-emerald-400', bg: 'bg-emerald-500/10', icon: '✅', borderColor: 'border-emerald-500/20' };
  };

  // Get progress percentage
  const getProgress = (entry) => {
    if (loading && entry === history[0]) return Math.floor(Math.random() * 40 + 30);
    const status = getStatusInfo(entry);
    if (status.label === 'Completed') return 100;
    if (status.label === 'Failed') return Math.floor(Math.random() * 30 + 10);
    return 0;
  };

  // Get progress bar color
  const getProgressColor = (entry) => {
    const status = getStatusInfo(entry);
    if (status.label === 'Completed') return 'bg-emerald-500';
    if (status.label === 'In Progress') return 'bg-amber-500';
    if (status.label === 'Failed') return 'bg-rose-500';
    return 'bg-slate-400';
  };

  // Avatar colors
  const avatarColors = [
    'bg-brand-500', 'bg-indigo-500', 'bg-emerald-500', 'bg-amber-500',
    'bg-rose-500', 'bg-violet-500', 'bg-teal-500', 'bg-pink-500'
  ];

  // Filter history by active tab
  const filteredHistory = history.filter(entry => {
    const status = getStatusInfo(entry);
    if (activeHistoryTab === 'inprogress') return status.label === 'In Progress';
    if (activeHistoryTab === 'completed') return status.label === 'Completed';
    if (activeHistoryTab === 'failed') return status.label === 'Failed';
    if (activeHistoryTab === 'scheduled') return false; // No scheduled items yet
    return true; // 'all' tab
  }).filter(entry => {
    if (repoFilter === 'all') return true;
    return (entry.repoUrl?.split('/').slice(-1)[0] || 'Unknown') === repoFilter;
  });

  // Get tab count
  const getTabCount = (tabId) => {
    if (tabId === 'all') return history.length;
    return history.filter(entry => {
      const status = getStatusInfo(entry);
      if (tabId === 'inprogress') return status.label === 'In Progress';
      if (tabId === 'completed') return status.label === 'Completed';
      if (tabId === 'failed') return status.label === 'Failed';
      if (tabId === 'scheduled') return false;
      return false;
    }).length;
  };

  if (history.length === 0) return (
    <div className="p-8 text-center text-slate-400 border border-slate-200 dark:border-dark-800 rounded-xl">
      No migrations have been run yet.
    </div>
  );

  return (
    <div className="glass-card animate-fadeIn overflow-hidden">
      {/* Tabs Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between border-b border-slate-200/50 dark:border-dark-800/40 px-6 pt-4 gap-4 pb-2 md:pb-0">
        <div className="flex items-center gap-1 overflow-x-auto w-full pb-2 md:pb-0 scrollbar-thin">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveHistoryTab(tab.id)}
              className={`migration-history-tab whitespace-nowrap ${activeHistoryTab === tab.id ? 'active' : ''}`}
            >
              {tab.label}
              {getTabCount(tab.id) > 0 && (
                <span className="ml-1.5 text-[10px] font-bold opacity-60">
                  ({getTabCount(tab.id)})
                </span>
              )}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3 pb-2 w-full md:w-auto shrink-0 justify-between md:justify-end">
          {/* Repository Filter */}
          <div className="flex items-center gap-2 text-xs">
            <span className="text-slate-400 flex items-center gap-1 hidden md:flex">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
              </svg>
            </span>
            <select
              value={repoFilter}
              onChange={(e) => setRepoFilter(e.target.value)}
              className="text-xs px-3 py-1.5 bg-white dark:bg-dark-900 border border-slate-200 dark:border-dark-800 rounded-lg focus:outline-none focus:ring-1 focus:ring-brand-500 text-slate-600 dark:text-slate-300 font-medium cursor-pointer"
            >
              <option value="all">All Repositories</option>
              {uniqueRepos.map(repo => (
                <option key={repo} value={repo}>{repo}</option>
              ))}
            </select>
          </div>

          {/* Clear button */}
          <button
            onClick={clearHistory}
            className="flex items-center gap-1 px-3 py-1.5 text-xs font-semibold text-slate-400 hover:text-rose-500 dark:hover:text-rose-400 transition-colors rounded-lg hover:bg-rose-500/10"
          >
            <Trash2 size={12} /> Clear
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto max-h-[600px] scrollbar-thin">
        <table className="w-full text-sm text-left">
          <thead className="sticky top-0 bg-white/90 dark:bg-dark-950/90 backdrop-blur-md z-10 shadow-sm">
            <tr className="border-b border-slate-200/50 dark:border-dark-800/50">
              <th className="py-3 px-6 font-semibold text-slate-400 dark:text-slate-500 text-xs whitespace-nowrap" style={{ width: '40px' }}></th>
              <th className="py-3 px-4 font-semibold text-slate-400 dark:text-slate-500 text-xs whitespace-nowrap">
                Migration ID <span className="inline-block ml-0.5 text-[10px] opacity-60">↕</span>
              </th>
              <th className="py-3 px-4 font-semibold text-slate-400 dark:text-slate-500 text-xs whitespace-nowrap">Repository</th>
              <th className="py-3 px-4 font-semibold text-slate-400 dark:text-slate-500 text-xs whitespace-nowrap">Type</th>
              <th className="py-3 px-4 font-semibold text-slate-400 dark:text-slate-500 text-xs whitespace-nowrap">Status</th>
              <th className="py-3 px-4 font-semibold text-slate-400 dark:text-slate-500 text-xs whitespace-nowrap" style={{ minWidth: '180px' }}>Progress</th>
              <th className="py-3 px-4 font-semibold text-slate-400 dark:text-slate-500 text-xs whitespace-nowrap">Started At</th>
              <th className="py-3 px-4 font-semibold text-slate-400 dark:text-slate-500 text-xs whitespace-nowrap">Files Modified</th>
            </tr>
          </thead>
          <tbody>
            {filteredHistory.map((entry, idx) => {
              const repoName = entry.repoUrl?.split('/').slice(-1)[0]?.replace('.git', '') || 'Unknown';
              const initial = repoName.charAt(0).toUpperCase();
              const statusInfo = getStatusInfo(entry);
              const progress = getProgress(entry);
              const avatarColor = avatarColors[idx % avatarColors.length];
              const migrationId = getMigrationId(entry, idx);

              return (
                <tr
                  key={entry.id}
                  className="border-b border-slate-100/50 dark:border-dark-800/30 hover:bg-slate-50/80 dark:hover:bg-dark-900/30 transition-colors"
                >
                  {/* Avatar */}
                  <td className="py-3 px-6">
                    <div className={`migration-avatar ${avatarColor}`}>
                      {initial}
                    </div>
                  </td>

                  {/* Migration ID */}
                  <td className="py-3 px-4">
                    <span className="font-mono text-xs font-bold text-slate-600 dark:text-slate-300">
                      {migrationId}
                    </span>
                  </td>

                  {/* Repository */}
                  <td className="py-3 px-4">
                    <span className="font-semibold text-sm text-slate-800 dark:text-slate-200">
                      {repoName}
                    </span>
                  </td>

                  {/* Type */}
                  <td className="py-3 px-4">
                    <span className="text-xs text-slate-500 dark:text-slate-400 whitespace-nowrap">
                      Java 8 → Java {entry.targetVersion}
                    </span>
                  </td>

                  {/* Status */}
                  <td className="py-3 px-4">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${statusInfo.bg} ${statusInfo.color} border ${statusInfo.borderColor}`}>
                      {statusInfo.label === 'In Progress' && (
                        <RefreshCw size={11} className="animate-spin" />
                      )}
                      {statusInfo.label === 'Completed' && (
                        <CheckCircle size={11} />
                      )}
                      {statusInfo.label === 'Failed' && (
                        <ShieldAlert size={11} />
                      )}
                      {statusInfo.label}
                    </span>
                  </td>

                  {/* Progress */}
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-3">
                      <span className="text-xs font-bold text-slate-600 dark:text-slate-300 w-9 text-right">
                        {progress}%
                      </span>
                      <div className="flex-1 relative h-2.5 bg-slate-200/60 dark:bg-dark-800/60 rounded-full overflow-hidden">
                        <div
                          className={`absolute top-0 left-0 h-full rounded-full transition-all duration-700 ${getProgressColor(entry)}`}
                          style={{ width: `${progress}%` }}
                        />
                        {/* Rocket on in-progress items */}
                        {statusInfo.label === 'In Progress' && (
                          <div
                            className="absolute top-1/2 -translate-y-1/2 text-[10px] z-10 animate-rocketBounce"
                            style={{ left: `calc(${progress}% - 6px)` }}
                          >
                            🚀
                          </div>
                        )}
                      </div>
                    </div>
                  </td>

                  {/* Started At */}
                  <td className="py-3 px-4">
                    <span className="text-xs text-slate-400 dark:text-slate-500 whitespace-nowrap">
                      {entry.timestamp}
                    </span>
                  </td>

                  {/* Duration */}
                  <td className="py-3 px-4">
                    <span className="text-xs font-medium text-slate-500 dark:text-slate-400 whitespace-nowrap">
                      {entry.modifiedFiles ? `${entry.modifiedFiles} files` : '—'}
                    </span>
                  </td>
                </tr>
              );
            })}

            {filteredHistory.length === 0 && (
              <tr>
                <td colSpan={8} className="py-12 text-center text-sm text-slate-400 dark:text-slate-500">
                  No migrations found for this filter.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
