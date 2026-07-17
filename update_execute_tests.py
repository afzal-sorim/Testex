import os

file_path = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\frontend\src\pages\FunctionalTesting.jsx"

content = """import React, { useState, useEffect, useRef } from 'react';
import { 
  CheckCircle2, XCircle, Info, RotateCw, Monitor, Clock, Play, FileText, Download, StopCircle, RefreshCw, Box
} from 'lucide-react';
import {
  API_BASE_URL,
  getPlaywrightStatus, runPlaywrightTests,
  getSeleniumStatus, runSeleniumTests,
  getPlaywrightReportDownloadUrl, getSeleniumReportDownloadUrl
} from '../api';

export default function FunctionalTesting({ 
  setActiveTab, 
  repoUrl, 
  result, 
  workflowState 
}) {
  const repoName = repoUrl ? repoUrl.split('/').pop().replace('.git', '') : '';
  const recommendedTool = result?.recommendedTestingTool || 'playwright';
  const isPlaywright = recommendedTool.toLowerCase() === 'playwright';

  // State
  const [status, setStatus] = useState('IDLE'); // IDLE, RUNNING, COMPLETED, FAILED
  const [totalTests, setTotalTests] = useState(result?.testScenarios || 226);
  const [passed, setPassed] = useState(0);
  const [failed, setFailed] = useState(0);
  const [skipped, setSkipped] = useState(0);
  const [progress, setProgress] = useState(0);
  
  const [logs, setLogs] = useState([]);
  const [startTime, setStartTime] = useState(null);
  const [elapsedTime, setElapsedTime] = useState('00:00:00');
  const logsEndRef = useRef(null);

  // Auto-scroll logs
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  // Simulation Logic
  useEffect(() => {
    let interval;
    if (status === 'RUNNING') {
      interval = setInterval(() => {
        setPassed(p => {
          const newPassed = p + Math.floor(Math.random() * 3);
          const currentTotal = newPassed + failed + skipped;
          
          if (currentTotal >= totalTests) {
            setProgress(100);
            return totalTests - failed - skipped;
          }
          
          setProgress(Math.floor((currentTotal / totalTests) * 100));
          return newPassed;
        });

        // Add random log
        setLogs(prev => {
          const now = new Date();
          const timeString = now.toLocaleTimeString([], { hour12: false });
          const tcId = `TC_${String(prev.length + 1).padStart(3, '0')}`;
          const newLog = {
            id: prev.length,
            time: timeString,
            message: `${tcId}: Executing automated steps for module...`,
            status: Math.random() > 0.05 ? 'Passed' : (Math.random() > 0.5 ? 'Failed' : 'Skipped'),
            icon: 'filter'
          };
          return [...prev, newLog];
        });

        // Update elapsed time
        if (startTime) {
          const diff = new Date() - startTime;
          const hrs = Math.floor(diff / 3600000);
          const mins = Math.floor((diff % 3600000) / 60000);
          const secs = Math.floor((diff % 60000) / 1000);
          setElapsedTime(`${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`);
        }

      }, 1500);
    } else if (status === 'COMPLETED') {
      setProgress(100);
    }
    return () => clearInterval(interval);
  }, [status, totalTests, failed, skipped, startTime]);

  // Backend Polling
  useEffect(() => {
    if (repoName && status === 'RUNNING') {
      const fetchStatus = async () => {
        try {
          const apiStatus = isPlaywright ? await getPlaywrightStatus(repoName) : await getSeleniumStatus(repoName);
          if (apiStatus.status !== 'RUNNING') {
            setStatus(apiStatus.status === 'FAILED' ? 'FAILED' : 'COMPLETED');
            setLogs(prev => [...prev, {
              id: prev.length,
              time: new Date().toLocaleTimeString([], { hour12: false }),
              message: 'Test execution finished.',
              status: 'Info',
              icon: 'info'
            }]);
          }
        } catch (e) {
          // Fallback if API fails
        }
      };
      const poll = setInterval(fetchStatus, 5000);
      return () => clearInterval(poll);
    }
  }, [repoName, status, isPlaywright]);

  const handleStartExecution = async () => {
    if (!repoName) return;
    setStatus('RUNNING');
    setStartTime(new Date());
    setPassed(0); setFailed(0); setSkipped(0); setProgress(0);
    setLogs([{
      id: 0,
      time: new Date().toLocaleTimeString([], { hour12: false }),
      message: 'Starting test execution...',
      status: 'Info',
      icon: 'info'
    }]);

    try {
      if (isPlaywright) {
        await runPlaywrightTests(repoName);
      } else {
        await runSeleniumTests(repoName);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleStop = () => {
    setStatus('COMPLETED');
  };

  const handleDownloadReport = () => {
    if (isPlaywright) {
      window.open(getPlaywrightReportDownloadUrl(repoName), '_blank');
    } else {
      window.open(getSeleniumReportDownloadUrl(repoName), '_blank');
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn w-full mx-auto pb-12 pt-4">
      
      {/* Top Banner - Execution Progress */}
      <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-[#101828]">Execution in Progress</h2>
            <p className="text-xs text-[#667085] mt-1">PROVA is running your tests. Sit back and relax!</p>
          </div>
          <div className="flex items-center gap-2">
            {status === 'RUNNING' ? (
              <span className="flex items-center gap-1.5 px-3 py-1 bg-emerald-50 text-emerald-600 text-xs font-bold rounded-full border border-emerald-200">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Live
              </span>
            ) : status === 'IDLE' ? (
              <button 
                onClick={handleStartExecution}
                className="flex items-center gap-2 px-4 py-2 bg-[#3B3FF6] hover:bg-[#2C31D8] text-white text-xs font-bold rounded-lg transition-colors shadow-sm"
              >
                <Play size={14} /> Start Execution
              </button>
            ) : (
              <span className="flex items-center gap-1.5 px-3 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-full border border-slate-200">
                <CheckCircle2 size={14} className="text-slate-500" /> Completed
              </span>
            )}
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex-1 h-3 bg-[#F2F4F7] rounded-full overflow-hidden">
            <div 
              className="h-full bg-[#3B3FF6] rounded-full transition-all duration-500 ease-out relative overflow-hidden"
              style={{ width: `${progress}%` }}
            >
              <div className="absolute inset-0 bg-white/20 w-full animate-[shimmer_2s_infinite]"></div>
            </div>
          </div>
          <span className="text-sm font-black text-[#101828] w-10 text-right">{progress}%</span>
        </div>
      </div>

      {/* 4 Counter Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Passed */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm p-5 flex flex-col items-center justify-center relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-emerald-50 rounded-full opacity-50 group-hover:scale-150 transition-transform duration-500"></div>
          <div className="flex items-center gap-2 mb-2 z-10">
            <CheckCircle2 size={20} className="text-[#12B76A]" strokeWidth={2.5} />
            <span className="text-sm font-bold text-[#344054]">Passed</span>
          </div>
          <span className="text-3xl font-black text-[#101828] z-10">{passed}</span>
        </div>
        
        {/* Failed */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm p-5 flex flex-col items-center justify-center relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-rose-50 rounded-full opacity-50 group-hover:scale-150 transition-transform duration-500"></div>
          <div className="flex items-center gap-2 mb-2 z-10">
            <XCircle size={20} className="text-[#F04438]" strokeWidth={2.5} />
            <span className="text-sm font-bold text-[#344054]">Failed</span>
          </div>
          <span className="text-3xl font-black text-[#101828] z-10">{failed}</span>
        </div>
        
        {/* Skipped */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm p-5 flex flex-col items-center justify-center relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-amber-50 rounded-full opacity-50 group-hover:scale-150 transition-transform duration-500"></div>
          <div className="flex items-center gap-2 mb-2 z-10">
            <RotateCw size={20} className="text-[#F79009]" strokeWidth={2.5} />
            <span className="text-sm font-bold text-[#344054]">Skipped</span>
          </div>
          <span className="text-3xl font-black text-[#101828] z-10">{skipped}</span>
        </div>
        
        {/* Total */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm p-5 flex flex-col items-center justify-center relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-[#5B5FF6]/10 rounded-full opacity-50 group-hover:scale-150 transition-transform duration-500"></div>
          <div className="flex items-center gap-2 mb-2 z-10">
            <Box size={20} className="text-[#5B5FF6]" strokeWidth={2.5} />
            <span className="text-sm font-bold text-[#344054]">Total</span>
          </div>
          <span className="text-3xl font-black text-[#101828] z-10">{totalTests}</span>
        </div>
      </div>

      {/* Main Grid: Logs and Details */}
      <div className="grid grid-cols-1 lg:grid-cols-[1.2fr_1fr] gap-6">
        
        {/* Live Execution Logs */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm flex flex-col overflow-hidden h-[500px]">
          <div className="p-4 border-b border-[#EAECF0] bg-[#F9FAFB]">
            <h3 className="text-sm font-bold text-[#101828]">Live Execution Logs</h3>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {logs.length === 0 ? (
              <div className="h-full flex items-center justify-center text-sm font-semibold text-[#98A2B3]">
                Waiting to start execution...
              </div>
            ) : (
              logs.map((log) => (
                <div key={log.id} className="flex items-start gap-4 text-xs font-medium">
                  <span className="text-[#98A2B3] w-16 flex-shrink-0 font-mono">{log.time}</span>
                  <div className="mt-0.5 text-[#667085]">
                    {log.icon === 'info' ? <Info size={14} /> : (
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                    )}
                  </div>
                  <span className="text-[#344054] flex-1">{log.message}</span>
                  
                  {log.status === 'Passed' && (
                    <span className="px-2 py-0.5 bg-emerald-50 text-emerald-600 rounded-md text-[10px] font-bold flex items-center gap-1">
                      <CheckCircle2 size={10} /> Passed
                    </span>
                  )}
                  {log.status === 'Failed' && (
                    <span className="px-2 py-0.5 bg-rose-50 text-rose-600 rounded-md text-[10px] font-bold flex items-center gap-1">
                      <XCircle size={10} /> Failed
                    </span>
                  )}
                  {log.status === 'Skipped' && (
                    <span className="px-2 py-0.5 bg-amber-50 text-amber-600 rounded-md text-[10px] font-bold flex items-center gap-1">
                      <RotateCw size={10} /> Skipped
                    </span>
                  )}
                </div>
              ))
            )}
            <div ref={logsEndRef} />
          </div>
        </div>

        {/* Right Column: Details & Preview */}
        <div className="flex flex-col gap-6">
          
          {/* Execution Details */}
          <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm overflow-hidden">
            <div className="p-4 border-b border-[#EAECF0]">
              <h3 className="text-sm font-bold text-[#101828]">Execution Details</h3>
            </div>
            <div className="p-4 divide-y divide-[#EAECF0]">
              <div className="py-2.5 flex justify-between items-center">
                <span className="text-xs font-semibold text-[#667085]">Browser</span>
                <span className="text-xs font-black text-[#101828]">Chromium 125</span>
              </div>
              <div className="py-2.5 flex justify-between items-center">
                <span className="text-xs font-semibold text-[#667085]">Environment</span>
                <span className="text-xs font-black text-[#101828]">Windows 11</span>
              </div>
              <div className="py-2.5 flex justify-between items-center">
                <span className="text-xs font-semibold text-[#667085]">Resolution</span>
                <span className="text-xs font-black text-[#101828]">1920 x 1080</span>
              </div>
              <div className="py-2.5 flex justify-between items-center">
                <span className="text-xs font-semibold text-[#667085]">Start Time</span>
                <span className="text-xs font-black text-[#101828]">{startTime ? startTime.toLocaleTimeString([], { hour12: true }) : '-'}</span>
              </div>
              <div className="py-2.5 flex justify-between items-center">
                <span className="text-xs font-semibold text-[#667085]">Elapsed Time</span>
                <span className="text-xs font-black text-[#101828] font-mono">{elapsedTime}</span>
              </div>
            </div>
          </div>

          {/* Live Preview */}
          <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm overflow-hidden flex-1 flex flex-col">
            <div className="p-4 border-b border-[#EAECF0]">
              <h3 className="text-sm font-bold text-[#101828]">Live Preview</h3>
            </div>
            <div className="p-4 flex-1 flex items-center justify-center bg-[#F9FAFB]">
              {status === 'RUNNING' ? (
                <div className="w-full h-full min-h-[160px] bg-white border border-[#EAECF0] rounded-lg shadow-sm overflow-hidden flex flex-col">
                  {/* Fake Browser Top Bar */}
                  <div className="h-6 bg-slate-100 flex items-center px-2 gap-1.5 border-b border-[#EAECF0]">
                    <div className="w-2 h-2 rounded-full bg-rose-400"></div>
                    <div className="w-2 h-2 rounded-full bg-amber-400"></div>
                    <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
                    <div className="ml-2 flex-1 h-3 bg-white rounded-sm border border-slate-200"></div>
                  </div>
                  {/* Preview Content Simulator */}
                  <div className="flex-1 p-2 relative">
                    <div className="absolute inset-0 bg-white bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] opacity-30"></div>
                    <div className="w-full h-full flex flex-col gap-2">
                       <div className="w-full h-8 bg-blue-600/10 rounded-md animate-pulse"></div>
                       <div className="flex gap-2 flex-1">
                         <div className="w-16 h-full bg-slate-100 rounded-md animate-pulse"></div>
                         <div className="flex-1 h-full bg-slate-50 rounded-md animate-pulse"></div>
                       </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center">
                  <Monitor size={32} className="text-[#D0D5DD] mx-auto mb-2" />
                  <p className="text-xs font-semibold text-[#98A2B3]">Preview inactive</p>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>

      {/* Bottom Action Bar */}
      <div className="flex items-center justify-between border-t border-[#EAECF0] pt-6">
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 border border-[#D0D5DD] rounded-lg text-sm font-bold text-[#344054] hover:bg-slate-50 transition-colors shadow-sm">
            <FileText size={16} /> View Live Report
          </button>
          <button 
            onClick={handleDownloadReport}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-lg text-sm font-bold hover:bg-emerald-100 transition-colors shadow-sm"
          >
            <Download size={16} /> Download HTML Report
          </button>
        </div>
        
        {status === 'RUNNING' && (
          <button 
            onClick={handleStop}
            className="flex items-center gap-2 px-5 py-2 bg-[#F04438] hover:bg-[#D92D20] text-white rounded-lg text-sm font-bold shadow-sm transition-colors"
          >
            <StopCircle size={16} /> Stop Execution
          </button>
        )}
      </div>

    </div>
  );
}
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("FunctionalTesting.jsx updated successfully.")
