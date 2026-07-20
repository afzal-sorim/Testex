import React from 'react';
import { Download } from 'lucide-react';
import { getMigrationReportUrl } from '../../api';

export default function AuditReportsSection({ setActiveTab, sectionRef }) {
  return (
    <div ref={sectionRef} className="p-6 glass-card space-y-3 flex flex-col justify-center mb-8 scroll-mt-6">
      <h3 className="text-md font-bold text-slate-900 dark:text-white mb-2">Audit Reports</h3>
      <div className="flex flex-col sm:flex-row gap-4">
        <a
          href={getMigrationReportUrl()}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-slate-100 hover:bg-slate-200 dark:bg-dark-800 dark:hover:bg-dark-700 text-slate-800 dark:text-slate-200 font-semibold rounded-xl text-xs transition-all border border-slate-200/50 dark:border-dark-700"
        >
          <Download size={14} /> Download PDF Report
        </a>
      </div>
    </div>
  );
}
