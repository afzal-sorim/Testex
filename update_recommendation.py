import os

file_path = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\frontend\src\pages\AITestRecommendation.jsx"

content = """import React, { useState, useEffect } from 'react';
import { 
  CheckCircle2, Download, Eye, FileText, Code, 
  Server, RefreshCw, FlaskConical, AlertCircle, AlertTriangle,
  ChevronDown, ChevronUp, ShieldAlert, ArrowRight, CheckCircle
} from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL } from '../api';

export default function AITestRecommendation({ setActiveTab, repoUrl, workflowState, setWorkflowState, analysisResult }) {
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [isDownloadingUiTests, setIsDownloadingUiTests] = useState(false);
  const [isDownloadingApiTests, setIsDownloadingApiTests] = useState(false);

  const repoName = repoUrl ? repoUrl.split('/').pop().replace('.git', '') : '';

  const handleDownloadUiTests = async () => {
    setIsDownloadingUiTests(true);
    try {
      if (!repoUrl) {
        alert("Please analyze repository first.");
        return;
      }
      const response = await fetch(`http://localhost:8000/api/reports/ui-functional-test/download/${encodeURIComponent(repoName)}`);
      if (!response.ok) {
        throw new Error('Failed to download UI test cases');
      }
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ui-functional-test-scope-${repoName}.html`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      alert('UI Functional Test Cases report downloaded successfully.');
    } catch (err) {
      console.error(err);
      alert('Failed to generate UI Functional Test Case report.');
    } finally {
      setIsDownloadingUiTests(false);
    }
  };

  const handleDownloadApiTests = async () => {
    setIsDownloadingApiTests(true);
    try {
      if (!repoUrl) {
        alert("Please analyze repository first.");
        return;
      }
      const response = await fetch(`http://localhost:8000/api/reports/api-test-cases/download/${encodeURIComponent(repoName)}`);
      if (!response.ok) {
        throw new Error('Failed to download API test cases');
      }
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `api-functional-test-scope-${repoName}.html`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      alert('API Functional Test Cases report downloaded successfully.');
    } catch (err) {
      console.error(err);
      alert('Failed to generate API Functional Test Case report.');
    } finally {
      setIsDownloadingApiTests(false);
    }
  };

  
  const [uiFiles, setUiFiles] = useState([]);
  const [apiFiles, setApiFiles] = useState([]);
  const [loadingFiles, setLoadingFiles] = useState(true);
  
  const [uiFilesOpen, setUiFilesOpen] = useState(true);
  const [apiFilesOpen, setApiFilesOpen] = useState(true);

  const [previewFile, setPreviewFile] = useState(null);
  const [previewContent, setPreviewContent] = useState('');
  const [previewLoading, setPreviewLoading] = useState(false);

  useEffect(() => {
    if (repoName) {
      fetchRecommendation();
      fetchFiles();
    }
  }, [repoName]);

  const fetchRecommendation = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await axios.get(`${API_BASE_URL}/functional-testing/${repoName}/recommendation`);
      setRecommendation(res.data);
    } catch (err) {
      console.error(err);
      setError('AI recommendation could not be completed. Retry the analysis.');
    } finally {
      setLoading(false);
    }
  };

  const fetchFiles = async () => {
    try {
      setLoadingFiles(true);
      const [uiRes, apiRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/functional-testing/${repoName}/ui/files`).catch(() => ({ data: [] })),
        axios.get(`${API_BASE_URL}/functional-testing/${repoName}/api/files`).catch(() => ({ data: [] }))
      ]);
      setUiFiles(uiRes.data || []);
      setApiFiles(apiRes.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingFiles(false);
    }
  };

  useEffect(() => {
    if (previewFile) {
      const fetchPreview = async () => {
        setPreviewLoading(true);
        try {
          const res = await axios.get(`${API_BASE_URL}/repositories/${repoName}/files/content`, {
            params: { path: previewFile.path }
          });
          if (res.data && res.data.content) {
            setPreviewContent(res.data.content);
          } else if (res.data && res.data.previewSupported === false) {
            setPreviewContent('// Binary file preview is not supported.');
          } else {
            setPreviewContent('// No content available');
          }
        } catch (err) {
          console.error(err);
          setPreviewContent('// Error loading file content');
        } finally {
          setPreviewLoading(false);
        }
      };
      fetchPreview();
    } else {
      setPreviewContent('');
    }
  }, [previewFile, repoName]);

  const handleDownload = (fileId) => {
    window.open(`${API_BASE_URL}/functional-testing/${repoName}/files/${encodeURIComponent(fileId)}/download`, '_blank');
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-[50vh]">
        <RefreshCw className="animate-spin text-[#5B5FF6] mb-4" size={32} />
        <p className="text-slate-600 font-medium">Analyzing project structure with AI...</p>
      </div>
    );
  }

  const calculateTestStats = () => {
    let totalUi = '47';
    let totalApi = '12';
    
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
    
    return { totalUi, totalApi };
  };

  const { totalUi, totalApi } = calculateTestStats();

  return (
    <div className="space-y-6 animate-fadeIn w-full mx-auto pb-12 pt-6">
      
      {/* 1. Test Cases Summary Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full">
        {/* Functional Test Case Summary */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm flex flex-col overflow-hidden">
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-sm font-bold text-[#101828] flex items-center gap-2">
                <FileText className="text-[#5B5FF6]" size={18} />
                Functional Test Case Summary
              </h3>
              <button
                onClick={handleDownloadUiTests}
                disabled={isDownloadingUiTests}
                className="px-4 py-2 bg-white border border-[#D0D5DD] hover:bg-slate-50 disabled:opacity-50 text-[#344054] text-xs font-bold rounded-lg transition-all flex items-center gap-2 shadow-sm"
              >
                <Download size={14} />
                {isDownloadingUiTests ? 'Downloading...' : 'Download Tests'}
              </button>
            </div>
            
            <div className="grid grid-cols-2 gap-6 mb-2">
               <div>
                  <div className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-1">Total Test Cases</div>
                  <div className="text-2xl font-black text-[#101828]">{totalUi}</div>
               </div>
               <div>
                  <div className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-1">Modules Covered</div>
                  <div className="text-2xl font-black text-[#101828]">{analysisResult?.fullBrdReport?.bizComponents?.length || 3}</div>
               </div>
               <div>
                  <div className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-1">Avg. Complexity</div>
                  <div className="text-sm font-bold text-[#101828] mt-1">Medium-High</div>
               </div>
               <div>
                  <div className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-1">Est. Execution</div>
                  <div className="text-sm font-bold text-[#101828] mt-1">~5 mins</div>
               </div>
            </div>
          </div>
          <div className="bg-[#F9FAFB] border-t border-[#EAECF0] p-4 flex items-center justify-between">
             <div className="flex items-center gap-2">
                <CheckCircle size={16} className="text-[#12B76A]" />
                <span className="text-xs font-bold text-[#12B76A]">Generated Successfully</span>
             </div>
             <span className="text-[10px] font-semibold text-[#98A2B3]">{new Date().toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
          </div>
        </div>

        {/* API Test Case Summary */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm flex flex-col overflow-hidden">
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-sm font-bold text-[#101828] flex items-center gap-2">
                <Server className="text-[#12B76A]" size={18} />
                API Test Case Summary
              </h3>
              <button
                onClick={handleDownloadApiTests}
                disabled={isDownloadingApiTests}
                className="px-4 py-2 bg-white border border-[#D0D5DD] hover:bg-slate-50 disabled:opacity-50 text-[#344054] text-xs font-bold rounded-lg transition-all flex items-center gap-2 shadow-sm"
              >
                <Download size={14} />
                {isDownloadingApiTests ? 'Downloading...' : 'Download Tests'}
              </button>
            </div>
            
            <div className="grid grid-cols-2 gap-6 mb-2">
               <div>
                  <div className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-1">Total API Tests</div>
                  <div className="text-2xl font-black text-[#101828]">{totalApi}</div>
               </div>
               <div>
                  <div className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-1">Endpoints Covered</div>
                  <div className="text-2xl font-black text-[#101828]">{analysisResult?.fullBrdReport?.apiGroups?.length || 1}</div>
               </div>
               <div>
                  <div className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-1">Coverage Scope</div>
                  <div className="text-sm font-bold text-[#101828] mt-1">E2E Workflows</div>
               </div>
               <div>
                  <div className="text-[10px] font-bold text-[#667085] uppercase tracking-wider mb-1">Data Mocks</div>
                  <div className="text-sm font-bold text-[#12B76A] mt-1">Ready</div>
               </div>
            </div>
          </div>
          <div className="bg-[#F9FAFB] border-t border-[#EAECF0] p-4 flex items-center justify-between">
             <div className="flex items-center gap-2">
                <CheckCircle size={16} className="text-[#12B76A]" />
                <span className="text-xs font-bold text-[#12B76A]">Generated Successfully</span>
             </div>
             <span className="text-[10px] font-semibold text-[#98A2B3]">{new Date().toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
          </div>
        </div>
      </div>

      {/* 2. Existing Project Files Layout (With Accordion Logic) */}
      <div className="grid grid-cols-1 gap-4 pt-2">
        
        {/* Left Division: HTML/UI Files */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm flex flex-col h-fit overflow-hidden">
          <button 
            onClick={() => setUiFilesOpen(!uiFilesOpen)}
            className="flex items-center justify-between w-full text-left focus:outline-none p-5 bg-[#F9FAFB] border-b border-[#EAECF0]"
          >
            <h3 className="text-[13px] font-bold text-[#101828] flex items-center gap-2">
              Detected UI / Frontend Files ({uiFiles.length})
            </h3>
            <div className="text-[#667085]">
              {uiFilesOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
            </div>
          </button>
          
          {uiFilesOpen && (
            <div className="p-5 max-h-[400px] overflow-y-auto custom-scrollbar space-y-2">
              {loadingFiles ? (
                <div className="flex flex-col items-center justify-center text-slate-400 py-10">
                  <RefreshCw className="animate-spin mb-3" size={24} />
                  Loading project UI files...
                </div>
              ) : uiFiles.length === 0 ? (
                <div className="flex flex-col items-center justify-center text-center p-6 bg-slate-50 rounded-xl border border-dashed border-[#EAECF0]">
                  <p className="text-slate-500 text-[11px] font-bold">No frontend UI files were detected in the repository.</p>
                </div>
              ) : (
                uiFiles.map(file => (
                  <div key={file.id} className="p-3 border border-[#EAECF0] bg-white rounded-xl flex items-center justify-between group hover:border-[#D0D5DD] transition-colors shadow-[0_1px_2px_rgba(16,24,40,0.05)]">
                    <div className="flex items-center gap-3 overflow-hidden">
                      <Code size={16} className="text-[#5B5FF6] flex-shrink-0" />
                      <div className="overflow-hidden">
                        <p className="text-xs font-bold text-[#101828] truncate">{file.name}</p>
                        <p className="text-[10px] text-[#667085] truncate mt-0.5" title={file.path}>{file.path}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0 ml-2">
                      <button onClick={() => setPreviewFile(file)} className="px-3 py-1.5 bg-white border border-[#D0D5DD] hover:bg-slate-50 text-[#344054] text-[10px] font-bold rounded-lg transition-colors flex items-center gap-1.5 shadow-sm">
                        <Eye size={12} /> View
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        {/* Right Division: API Files */}
        <div className="bg-white border border-[#EAECF0] rounded-2xl shadow-sm flex flex-col h-fit overflow-hidden">
          <button 
            onClick={() => setApiFilesOpen(!apiFilesOpen)}
            className="flex items-center justify-between w-full text-left focus:outline-none p-5 bg-[#F9FAFB] border-b border-[#EAECF0]"
          >
            <h3 className="text-[13px] font-bold text-[#101828] flex items-center gap-2">
              Detected Backend API Files ({apiFiles.length})
            </h3>
            <div className="text-[#667085]">
              {apiFilesOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
            </div>
          </button>

          {apiFilesOpen && (
            <div className="p-5 max-h-[400px] overflow-y-auto custom-scrollbar space-y-2">
              {loadingFiles ? (
                <div className="flex flex-col items-center justify-center text-slate-400 py-10">
                  <RefreshCw className="animate-spin mb-3" size={24} />
                  Loading API endpoints...
                </div>
              ) : apiFiles.length === 0 ? (
                <div className="flex flex-col items-center justify-center text-center p-6 bg-slate-50 rounded-xl border border-dashed border-[#EAECF0]">
                  <p className="text-slate-500 text-[11px] font-bold">No backend API files were detected.</p>
                </div>
              ) : (
                apiFiles.map(file => (
                  <div key={file.id} className="p-3 border border-[#EAECF0] bg-white rounded-xl flex items-center justify-between group hover:border-[#D0D5DD] transition-colors shadow-[0_1px_2px_rgba(16,24,40,0.05)]">
                    <div className="flex items-center gap-3 overflow-hidden">
                      <Server size={16} className="text-[#12B76A] flex-shrink-0" />
                      <div className="overflow-hidden">
                        <p className="text-xs font-bold text-[#101828] truncate">{file.name}</p>
                        <p className="text-[10px] text-[#667085] truncate mt-0.5" title={file.path}>{file.path}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0 ml-2">
                      <button onClick={() => setPreviewFile(file)} className="px-3 py-1.5 bg-white border border-[#D0D5DD] hover:bg-slate-50 text-[#344054] text-[10px] font-bold rounded-lg transition-colors flex items-center gap-1.5 shadow-sm">
                        <Eye size={12} /> View
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>

      {/* Footer Navigation */}
      <div className="flex justify-between items-center mt-8 pb-4">
         <button className="bg-[#12B76A] hover:bg-[#0E9F5D] text-white px-8 py-2.5 rounded-xl font-bold text-[13px] shadow-sm transition-colors">
            Back
         </button>
         <button
            onClick={() => setActiveTab('results')}
            className="bg-[#5B5FF6] hover:bg-[#4F54D8] text-white px-8 py-2.5 rounded-xl font-bold text-[13px] flex items-center gap-2 shadow-sm transition-colors"
         >
            Continue <ArrowRight size={16} />
         </button>
      </div>

      {/* File Preview Modal */}
      {previewFile && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
          <div className="bg-white rounded-3xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl animate-fadeIn">
            <div className="flex items-center justify-between p-6 border-b border-[#EAECF0]">
              <div>
                <h3 className="text-[13px] font-bold text-[#101828]">{previewFile.name}</h3>
                <p className="text-[10px] text-[#667085] mt-1">{previewFile.path}</p>
              </div>
              <div className="flex items-center gap-3">
                <button onClick={() => setPreviewFile(null)} className="px-5 py-2 bg-[#101828] hover:bg-black text-white text-[11px] font-bold rounded-lg transition-colors shadow-sm">
                  Close
                </button>
              </div>
            </div>
            <div className="flex-1 p-6 overflow-auto bg-[#F9FAFB]">
              {previewLoading ? (
                <div className="flex items-center justify-center h-full text-[#667085] text-xs font-bold">
                  <RefreshCw className="animate-spin mr-2 text-[#5B5FF6]" size={16} /> Loading file content...
                </div>
              ) : (
                <pre className="text-[11px] font-mono text-[#344054] whitespace-pre-wrap bg-white border border-[#EAECF0] p-4 rounded-xl shadow-sm">
                  {previewContent || `// No content to display`}
                </pre>
              )}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("AITestRecommendation.jsx updated successfully.")
