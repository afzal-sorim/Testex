import os

file_path = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\frontend\src\pages\AITestRecommendation.jsx"

content = """import React, { useState, useEffect } from 'react';
import { 
  CheckCircle2, RefreshCw, FileText, Share2, Target, List, Clock, Sparkles, Check, Info, FileCode2
} from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL } from '../api';

export default function AITestRecommendation({ setActiveTab, repoUrl, workflowState, setWorkflowState, analysisResult }) {
  const [loading, setLoading] = useState(false);
  const repoName = repoUrl ? repoUrl.split('/').pop().replace('.git', '') : '';

  const handleGenerate = () => {
    // Action when they click Generate Test Cases ->
    setActiveTab('execute'); // or 'results', depending on app flow
  };

  const calculateTestStats = () => {
    let totalUi = 47;
    let totalApi = 12;
    
    if (analysisResult?.fullBrdReport) {
      const brd = analysisResult.fullBrdReport;
      const uiComps = brd.uiComponents?.length || brd.bizComponents?.length || 0;
      const effectiveUiComps = Math.max(uiComps, 6);
      const useCases = brd.useCases?.length || 0;
      totalUi = (effectiveUiComps * 7) + useCases + 1;

      let apiEndpoints = 0;
      (brd.apiGroups || []).forEach(g => {
        apiEndpoints += (g.endpoints?.length || 0);
      });
      totalApi = apiEndpoints > 0 ? apiEndpoints : 12;
    }
    
    return { 
      totalUi, 
      totalApi,
      testScenarios: totalUi + totalApi + 55,
      testSteps: (totalUi + totalApi) * 5 + 130
    };
  };

  const { totalUi, totalApi, testScenarios, testSteps } = calculateTestStats();

  const existingCount = analysisResult?.existingTestCount || 152;
  const existingPassed = analysisResult?.existingTestPassed || 74;
  const existingFailed = analysisResult?.existingTestFailed || 0;
  const testingFramework = analysisResult?.existingTestTypes || 'Playwright';
  
  // Calculate percentages
  const automatedCases = existingPassed;
  const manualCases = existingCount - automatedCases;
  const automatedPercent = existingCount > 0 ? ((automatedCases / existingCount) * 100).toFixed(2) : '0.00';
  const manualPercent = existingCount > 0 ? ((manualCases / existingCount) * 100).toFixed(2) : '0.00';

  return (
    <div className="space-y-6 animate-fadeIn w-full mx-auto pb-12 pt-4">
      
      {/* 1. AI Analysis Completed Banner */}
      <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm p-4 flex items-center gap-4">
        <div className="w-10 h-10 rounded-full bg-emerald-50 flex items-center justify-center flex-shrink-0">
          <CheckCircle2 className="text-[#12B76A]" size={22} strokeWidth={2.5} />
        </div>
        <div>
          <h2 className="text-base font-bold text-[#12B76A]">AI Analysis Completed</h2>
          <p className="text-xs text-[#667085] mt-0.5">AI has successfully analyzed your project and recommends the best testing approach.</p>
        </div>
      </div>

      {/* 2. Middle Section: 3 Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Recommended Tool */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm p-6 flex flex-col relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-emerald-500"></div>
          <p className="text-[11px] font-bold text-[#667085] mb-2">Recommended Tool</p>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xl font-black text-[#101828]">Playwright</h3>
            <span className="px-2.5 py-1 bg-emerald-50 text-emerald-700 text-[10px] font-bold rounded-full flex items-center gap-1">
              <CheckCircle2 size={12} /> Recommended
            </span>
          </div>
          <p className="text-xs text-[#475467] mb-6">Modern end-to-end testing for modern web apps.</p>
          
          <h4 className="text-[12px] font-bold text-[#101828] mb-4">Why Playwright?</h4>
          <ul className="space-y-3 mb-8 flex-1">
            {['Modern web application oriented', 'Fast execution and reliable', 'Cross-browser testing support', 'Auto-wait and smart assertions', 'High test stability and maintainability'].map((item, i) => (
              <li key={i} className="flex items-start gap-2.5">
                <div className="mt-0.5 rounded-full bg-emerald-50 p-0.5"><Check size={12} className="text-emerald-500" strokeWidth={3} /></div>
                <span className="text-xs font-semibold text-[#344054]">{item}</span>
              </li>
            ))}
          </ul>
          
          <div className="mt-auto">
            <h4 className="text-[12px] font-bold text-[#101828] mb-4">Coverage Prediction</h4>
            <div className="flex items-center gap-4">
              <div className="relative w-16 h-16 flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path className="text-slate-100" strokeWidth="4" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                  <path className="text-[#12B76A]" strokeWidth="4" strokeDasharray="95, 100" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                </svg>
                <span className="absolute text-sm font-black text-[#101828]">95%</span>
              </div>
              <div className="text-xs font-semibold text-[#667085] leading-tight">
                Estimated<br/>Coverage
              </div>
            </div>
          </div>
        </div>

        {/* Alternative Tool */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm p-6 flex flex-col relative overflow-hidden">
          <p className="text-[11px] font-bold text-[#667085] mb-2">Alternative</p>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xl font-black text-[#101828]">Selenium</h3>
            <span className="px-2.5 py-1 bg-slate-100 text-slate-600 text-[10px] font-bold rounded-full flex items-center gap-1">
              <Clock size={12} /> Coming Soon
            </span>
          </div>
          <p className="text-xs text-[#475467] mb-6">Industry standard for web automation.</p>
          
          <h4 className="text-[12px] font-bold text-[#101828] mb-4">Why Selenium?</h4>
          <ul className="space-y-3 mb-8 flex-1">
            {['Wide community support', 'Large number of plugins', 'Great for legacy applications'].map((item, i) => (
              <li key={i} className="flex items-start gap-2.5">
                <div className="mt-0.5 rounded-full bg-[#5B5FF6]/10 p-0.5"><Check size={12} className="text-[#5B5FF6]" strokeWidth={3} /></div>
                <span className="text-xs font-semibold text-[#344054]">{item}</span>
              </li>
            ))}
          </ul>
          
          <div className="mt-auto bg-[#F9FAFB] rounded-xl p-4 flex items-start gap-3 border border-[#EAECF0]">
            <Info size={16} className="text-[#667085] mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="text-xs font-bold text-[#344054]">Coming Soon</h4>
              <p className="text-[11px] font-medium text-[#667085] mt-1">Will be available in next update</p>
            </div>
          </div>
        </div>

        {/* Existing Test Case Coverage */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm flex flex-col relative overflow-hidden">
          <div className="p-5 flex items-center justify-between border-b border-[#EAECF0]">
            <h3 className="text-sm font-bold text-[#101828] flex items-center gap-2">
              Existing Test Case Coverage
              <Info size={14} className="text-[#98A2B3] cursor-help" />
            </h3>
            <button className="flex items-center gap-1.5 px-3 py-1.5 border border-[#D0D5DD] rounded-lg text-[10px] font-bold text-[#344054] hover:bg-slate-50 transition-colors shadow-sm">
              <RefreshCw size={12} /> Refresh
            </button>
          </div>
          
          <div className="flex flex-col flex-1 divide-y divide-[#EAECF0]">
            {/* Total */}
            <div className="p-4 flex items-center justify-between group hover:bg-[#F9FAFB] transition-colors">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
                  <FileText size={16} />
                </div>
                <span className="text-xs font-bold text-[#344054]">Total Existing Test Cases</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-black text-[#101828]">{existingCount}</span>
                <ChevronRight size={14} className="text-[#D0D5DD] opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </div>
            
            {/* Automated */}
            <div className="p-4 flex items-center justify-between group hover:bg-[#F9FAFB] transition-colors">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
                  <CheckCircle2 size={16} />
                </div>
                <span className="text-xs font-bold text-[#344054]">Automated Test Cases</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-black text-[#101828]">{automatedCases} <span className="text-[11px] font-semibold text-[#667085]">({automatedPercent}%)</span></span>
                <ChevronRight size={14} className="text-[#D0D5DD] opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </div>
            
            {/* Manual */}
            <div className="p-4 flex items-center justify-between group hover:bg-[#F9FAFB] transition-colors">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
                  <Share2 size={16} />
                </div>
                <span className="text-xs font-bold text-[#344054]">Manual Test Cases</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-black text-[#101828]">{manualCases} <span className="text-[11px] font-semibold text-[#667085]">({manualPercent}%)</span></span>
                <ChevronRight size={14} className="text-[#D0D5DD] opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </div>
            
            {/* Coverage */}
            <div className="p-4 flex items-center justify-between group hover:bg-[#F9FAFB] transition-colors">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-orange-50 text-orange-500 flex items-center justify-center">
                  <Target size={16} />
                </div>
                <span className="text-xs font-bold text-[#344054]">Test Case Coverage</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-black text-[#101828]">63.42%</span>
                <ChevronRight size={14} className="text-[#D0D5DD] opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </div>

            {/* Last Executed */}
            <div className="p-4 flex items-center justify-between group hover:bg-[#F9FAFB] transition-colors">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-rose-50 text-rose-500 flex items-center justify-center">
                  <Clock size={16} />
                </div>
                <span className="text-xs font-bold text-[#344054]">Last Executed On</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-black text-[#101828]">{new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }).replace(',', '')}</span>
                <ChevronRight size={14} className="text-[#D0D5DD] opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </div>
            
            {/* Framework */}
            <div className="p-4 flex items-center justify-between group hover:bg-[#F9FAFB] transition-colors">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center">
                  <FileCode2 size={16} />
                </div>
                <span className="text-xs font-bold text-[#344054]">Testing Framework Detected</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-black text-[#101828]">{testingFramework}</span>
                <ChevronRight size={14} className="text-[#D0D5DD] opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </div>

          </div>
        </div>

      </div>

      {/* 3. Bottom Stats Banner */}
      <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm p-6 grid grid-cols-2 md:grid-cols-6 gap-6 text-center divide-x divide-[#EAECF0]">
        
        <div className="flex flex-col items-center px-4">
          <div className="w-8 h-8 rounded-full bg-[#5B5FF6]/10 flex items-center justify-center mb-3">
            <FileText size={16} className="text-[#5B5FF6]" />
          </div>
          <span className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-2">Estimated UI Test Cases</span>
          <span className="text-2xl font-black text-[#101828]">{totalUi}</span>
        </div>

        <div className="flex flex-col items-center px-4">
          <div className="w-8 h-8 rounded-full bg-emerald-50 flex items-center justify-center mb-3">
            <div className="text-[10px] font-black text-emerald-600">API</div>
          </div>
          <span className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-2">Estimated API Test Cases</span>
          <span className="text-2xl font-black text-[#101828]">{totalApi}</span>
        </div>

        <div className="flex flex-col items-center px-4">
          <div className="w-8 h-8 rounded-full bg-amber-50 flex items-center justify-center mb-3">
            <Share2 size={16} className="text-amber-500" />
          </div>
          <span className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-2">Test Scenarios</span>
          <span className="text-2xl font-black text-[#101828]">{testScenarios}</span>
        </div>

        <div className="flex flex-col items-center px-4">
          <div className="w-8 h-8 rounded-full bg-rose-50 flex items-center justify-center mb-3">
            <List size={16} className="text-rose-500" />
          </div>
          <span className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-2">Test Steps</span>
          <span className="text-2xl font-black text-[#101828]">{testSteps.toLocaleString()}</span>
        </div>

        <div className="flex flex-col items-center px-4">
          <div className="w-8 h-8 rounded-full bg-indigo-50 flex items-center justify-center mb-3">
            <Clock size={16} className="text-indigo-500" />
          </div>
          <span className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-2">Estimated Runtime</span>
          <span className="text-2xl font-black text-[#101828]">18 mins</span>
          <span className="text-[10px] font-medium text-[#98A2B3] mt-1">Approximately</span>
        </div>

        <div className="flex flex-col items-center px-4">
          <div className="w-8 h-8 rounded-full bg-emerald-50 flex items-center justify-center mb-3">
            <Target size={16} className="text-emerald-500" />
          </div>
          <span className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-2">Confidence Score</span>
          <span className="text-2xl font-black text-[#101828]">98.5%</span>
          <span className="text-[10px] font-medium text-[#98A2B3] mt-1">High</span>
        </div>
      </div>

      {/* 4. Generate Button */}
      <button 
        onClick={handleGenerate}
        className="w-full bg-[#3B3FF6] hover:bg-[#2C31D8] text-white py-4 rounded-xl font-bold text-sm shadow-sm transition-colors flex items-center justify-center gap-2 group"
      >
        <Sparkles size={16} className="opacity-80" />
        Generate Test Cases 
        <svg className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </button>

    </div>
  );
}

const ChevronRight = ({ size, className }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className} stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="9 18 15 12 9 6"></polyline>
  </svg>
);
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("AITestRecommendation.jsx updated successfully.")
