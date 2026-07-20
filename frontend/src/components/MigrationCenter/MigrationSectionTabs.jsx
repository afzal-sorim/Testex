import React from 'react';
import { Clock, ShieldAlert, FileText, CheckCircle } from 'lucide-react';

export default function MigrationSectionTabs({ scrollToSection, refs }) {
  const tabs = [
    {
      id: 'history',
      label: 'Migration History',
      icon: <Clock size={16} />,
      ref: refs.historyRef
    },
    {
      id: 'build',
      label: 'Build Check & Verification',
      icon: <CheckCircle size={16} />,
      ref: refs.buildRef
    },
    {
      id: 'audit',
      label: 'Audit Reports',
      icon: <FileText size={16} />,
      ref: refs.auditRef
    },
    {
      id: 'llm',
      label: 'LLM Execution Log',
      icon: <FileText size={16} />,
      ref: refs.llmRef
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 animate-fadeIn my-8">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => scrollToSection(tab.ref)}
          className="flex flex-col items-center justify-center p-4 glass-card hover:bg-slate-50 dark:hover:bg-dark-900/50 transition-all cursor-pointer border border-slate-200/50 dark:border-dark-800/50 hover:border-brand-500/50 hover:shadow-md group"
        >
          <div className="p-3 bg-slate-100 dark:bg-dark-800 rounded-xl text-slate-500 dark:text-slate-400 group-hover:bg-brand-500/10 group-hover:text-brand-500 transition-colors mb-2">
            {tab.icon}
          </div>
          <span className="text-sm font-bold text-slate-700 dark:text-slate-300 group-hover:text-brand-600 dark:group-hover:text-brand-400">
            {tab.label}
          </span>
        </button>
      ))}
    </div>
  );
}
