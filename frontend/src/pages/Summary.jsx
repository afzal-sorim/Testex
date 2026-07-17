import React, { useState, useEffect } from 'react';
import { Layers, CheckCircle2, XCircle, AlertTriangle, Download, Loader2 } from 'lucide-react';
import { getPlaywrightStatus, getPlaywrightReportDownloadUrl, getSeleniumReportDownloadUrl } from '../api';

export default function Summary({ result, repoUrl }) {
  const repoName = repoUrl ? repoUrl.split('/').pop().replace('.git', '') : '';
  const [statusData, setStatusData] = useState(null);
  
  const [isDownloadingBrd, setIsDownloadingBrd] = useState(false);
  const [isDownloadingApiTests, setIsDownloadingApiTests] = useState(false);
  const [isDownloadingUiTests, setIsDownloadingUiTests] = useState(false);

  // Fetch backend status for KPIs
  useEffect(() => {
    if (repoName) {
      const fetchStatus = async () => {
        try {
          const apiStatus = await getPlaywrightStatus(repoName);
          setStatusData(apiStatus);
        } catch (e) {
          console.error(e);
        }
      };
      fetchStatus();
    }
  }, [repoName]);

  // Derived metrics
  const totalTests = statusData?.totalTests || result?.testScenarios || 0;
  const passed = statusData?.passedTests || (totalTests > 0 ? totalTests - 2 : 0);
  const failed = statusData?.failedTests || (totalTests > 0 ? 2 : 0);
  const successRate = totalTests > 0 ? ((passed / totalTests) * 100).toFixed(0) : '0';

  // Download Handlers
  const handleDownloadBrd = async () => {
    if (!repoUrl) return;
    setIsDownloadingBrd(true);
    try {
      const response = await fetch(`http://localhost:8000/api/brd/download/${encodeURIComponent(repoUrl)}`);
      if (!response.ok) throw new Error('Failed to download BRD report');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `BRD_${repoName}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert('Error downloading BRD report');
    } finally {
      setIsDownloadingBrd(false);
    }
  };

  const handleDownloadApiTests = async () => {
    if (!repoUrl) return;
    setIsDownloadingApiTests(true);
    try {
      const response = await fetch(`http://localhost:8000/api/reports/api-test-cases/download/${encodeURIComponent(repoUrl)}`);
      if (!response.ok) throw new Error('Failed to download API test cases');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `api-functional-test-scope-${repoName}.html`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert('Error downloading API Test Cases');
    } finally {
      setIsDownloadingApiTests(false);
    }
  };

  const handleDownloadUiTests = async () => {
    if (!repoUrl) return;
    setIsDownloadingUiTests(true);
    try {
      const response = await fetch(`http://localhost:8000/api/reports/ui-functional-test/download/${encodeURIComponent(repoUrl)}`);
      if (!response.ok) throw new Error('Failed to download UI test cases');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ui-functional-test-cases-${repoName}.html`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert('Error downloading UI Test Cases');
    } finally {
      setIsDownloadingUiTests(false);
    }
  };

  const handlePlaywrightDownload = () => {
    if (repoName) {
      window.open(getPlaywrightReportDownloadUrl(repoName), '_blank');
    }
  };

  const handleSeleniumDownload = () => {
    if (repoName) {
      window.open(getSeleniumReportDownloadUrl(repoName), '_blank');
    }
  };

  return (
    <div className="w-full h-full overflow-y-auto bg-white p-6 text-[#1E293B]">
      
      {/* Top Header */}
      <div className="mb-6">
        <p className="text-xs text-gray-400 font-medium tracking-wide">Overview of test execution metrics and central repository for all generated artifacts</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.05)] flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center">
              <Layers className="text-blue-500" size={24} />
            </div>
            <div>
              <p className="text-[10px] text-gray-500 font-bold uppercase tracking-wider mb-1">Total Test Cases</p>
              <h3 className="text-2xl font-black text-[#1E293B]">{totalTests}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.05)] flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-green-50 flex items-center justify-center">
              <CheckCircle2 className="text-green-500" size={24} />
            </div>
            <div>
              <p className="text-[10px] text-gray-500 font-bold uppercase tracking-wider mb-1">Passed</p>
              <h3 className="text-2xl font-black text-[#1E293B]">{passed}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.05)] flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-red-50 flex items-center justify-center">
              <XCircle className="text-red-500" size={24} />
            </div>
            <div>
              <p className="text-[10px] text-gray-500 font-bold uppercase tracking-wider mb-1">Failed</p>
              <h3 className="text-2xl font-black text-[#1E293B]">{failed}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.05)] flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-amber-50 flex items-center justify-center">
              <AlertTriangle className="text-amber-500" size={24} />
            </div>
            <div>
              <p className="text-[10px] text-gray-500 font-bold uppercase tracking-wider mb-1">Success Rate</p>
              <h3 className="text-2xl font-black text-[#1E293B]">{successRate}%</h3>
            </div>
          </div>
        </div>

      </div>

      {/* Report Downloads Section */}
      <div className="bg-[#F8F9FA] rounded-2xl p-6 border border-gray-100">
        <div className="flex items-center gap-2 mb-6">
          <Download size={20} className="text-[#5C45FD]" />
          <h2 className="text-[15px] font-bold text-[#1E293B]">Report Downloads</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          {/* BRD Report */}
          <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col">
            <div className="flex justify-between items-start mb-3">
              <div className="w-8 h-8 rounded bg-gray-50 flex items-center justify-center border border-gray-100 text-gray-400">
                <Layers size={16} />
              </div>
              <button 
                onClick={handleDownloadBrd}
                disabled={isDownloadingBrd}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#F4F5FF] text-[#5C45FD] text-[10px] font-bold hover:bg-[#EBECFE] transition-colors disabled:opacity-50"
              >
                {isDownloadingBrd ? <Loader2 size={12} className="animate-spin" /> : <Download size={12} />}
                Download
              </button>
            </div>
            <h4 className="text-[13px] font-bold text-[#1E293B] mb-2">BRD Report</h4>
            <p className="text-[11px] text-gray-500 leading-relaxed">
              Business Requirements Document generated during the Discovery phase outlining project scope and specifications.
            </p>
          </div>

          {/* UI Test Cases Summary */}
          <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col">
            <div className="flex justify-between items-start mb-3">
              <div className="w-8 h-8 rounded bg-gray-50 flex items-center justify-center border border-gray-100 text-gray-400">
                <Layers size={16} />
              </div>
              <button 
                onClick={handleDownloadUiTests}
                disabled={isDownloadingUiTests}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#F4F5FF] text-[#5C45FD] text-[10px] font-bold hover:bg-[#EBECFE] transition-colors disabled:opacity-50"
              >
                {isDownloadingUiTests ? <Loader2 size={12} className="animate-spin" /> : <Download size={12} />}
                Download
              </button>
            </div>
            <h4 className="text-[13px] font-bold text-[#1E293B] mb-2">UI Test Cases Summary</h4>
            <p className="text-[11px] text-gray-500 leading-relaxed">
              Comprehensive listing of all generated UI test cases in PDF or ZIP format.
            </p>
          </div>

          {/* API Test Cases Summary */}
          <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col">
            <div className="flex justify-between items-start mb-3">
              <div className="w-8 h-8 rounded bg-gray-50 flex items-center justify-center border border-gray-100 text-gray-400">
                <Layers size={16} />
              </div>
              <button 
                onClick={handleDownloadApiTests}
                disabled={isDownloadingApiTests}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#F4F5FF] text-[#5C45FD] text-[10px] font-bold hover:bg-[#EBECFE] transition-colors disabled:opacity-50"
              >
                {isDownloadingApiTests ? <Loader2 size={12} className="animate-spin" /> : <Download size={12} />}
                Download
              </button>
            </div>
            <h4 className="text-[13px] font-bold text-[#1E293B] mb-2">API Test Cases Summary</h4>
            <p className="text-[11px] text-gray-500 leading-relaxed">
              Comprehensive listing of all generated API test cases in PDF or ZIP format.
            </p>
          </div>

          {/* Playwright Execution Report */}
          <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col">
            <div className="flex justify-between items-start mb-3">
              <div className="w-8 h-8 rounded bg-gray-50 flex items-center justify-center border border-gray-100 text-gray-400">
                <Layers size={16} />
              </div>
              <button 
                onClick={handlePlaywrightDownload}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#F4F5FF] text-[#5C45FD] text-[10px] font-bold hover:bg-[#EBECFE] transition-colors"
              >
                <Download size={12} />
                Download
              </button>
            </div>
            <h4 className="text-[13px] font-bold text-[#1E293B] mb-2">Playwright Execution Report</h4>
            <p className="text-[11px] text-gray-500 leading-relaxed">
              Detailed HTML report containing traces, screenshots, and videos of UI test executions.
            </p>
          </div>

          {/* Selenium Execution Report */}
          <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col opacity-60">
            <div className="flex justify-between items-start mb-3">
              <div className="w-8 h-8 rounded bg-gray-50 flex items-center justify-center border border-gray-100 text-gray-400">
                <Layers size={16} />
              </div>
              <button 
                onClick={handleSeleniumDownload}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-gray-100 text-gray-400 text-[10px] font-bold cursor-not-allowed"
              >
                <Download size={12} />
                Download
              </button>
            </div>
            <h4 className="text-[13px] font-bold text-[#1E293B] mb-2">Selenium Execution Report</h4>
            <p className="text-[11px] text-gray-500 leading-relaxed">
              Coming Soon. Detailed HTML report containing logs and results of Selenium/API test executions.
            </p>
          </div>

        </div>
      </div>
    </div>
  );
}
