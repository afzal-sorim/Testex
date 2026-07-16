import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Folder, FolderOpen, FileCode, FileImage, FileArchive, FileText, File, 
  ChevronRight, ChevronDown, Download, X, Copy, Check, FileSearch, Code, 
  Layout, Database, Server, MonitorSmartphone, Layers, Search, Zap, CheckCircle2, ShieldCheck,
  Briefcase, Users, GitBranch, Target, AlertTriangle, ArrowRight
} from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { getRepositoryTree, getRepositoryFileContent, analyzeRepository, startProject } from '../api';

// Reusable File Icon Component
const FileIcon = ({ type, extension, expanded }) => {
  if (type === 'folder') {
    return expanded ? <FolderOpen size={16} className="text-[#3B82F6]" /> : <Folder size={16} className="text-[#3B82F6]" />;
  }
  const ext = (extension || '').toLowerCase();
  if (['js', 'jsx', 'ts', 'tsx', 'py', 'java', 'cpp', 'c', 'cs', 'go', 'rs', 'php', 'rb'].includes(ext)) {
    return <FileCode size={16} className="text-[#10B981]" />;
  }
  if (['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico'].includes(ext)) {
    return <FileImage size={16} className="text-[#8B5CF6]" />;
  }
  if (['zip', 'tar', 'gz', 'rar', '7z', 'jar', 'war'].includes(ext)) {
    return <FileArchive size={16} className="text-[#F43F5E]" />;
  }
  if (['json', 'xml', 'yaml', 'yml', 'md', 'txt', 'csv'].includes(ext)) {
    return <FileText size={16} className="text-[#F59E0B]" />;
  }
  return <File size={16} className="text-[#9CA3AF]" />;
};

// Recursive Tree Node Component
const TreeNode = ({ node, level = 0, onSelectFile, selectedPath }) => {
  const [expanded, setExpanded] = useState(false);
  const isFolder = node.type === 'folder';
  const isSelected = selectedPath === node.path;

  const handleClick = (e) => {
    e.stopPropagation();
    if (isFolder) {
      setExpanded(!expanded);
    } else {
      onSelectFile(node);
    }
  };

  return (
    <div className="select-none">
      <div 
        onClick={handleClick}
        className={`flex items-center gap-2 py-1.5 px-2 rounded-lg cursor-pointer transition-colors ${isSelected ? 'bg-[#F5F3FF] text-[#5C36E0] font-semibold' : 'hover:bg-[#F9FAFB] text-[#4B5563]'}`}
        style={{ paddingLeft: `${level * 16 + 8}px` }}
      >
        <span className="w-4 h-4 flex items-center justify-center shrink-0">
          {isFolder && (
            expanded ? <ChevronDown size={14} className="text-[#9CA3AF]" /> : <ChevronRight size={14} className="text-[#9CA3AF]" />
          )}
        </span>
        <FileIcon type={node.type} extension={node.extension} expanded={expanded} />
        <span className="text-[13px] truncate">{node.name}</span>
      </div>
      
      {isFolder && expanded && node.children && (
        <div className="flex flex-col mt-0.5">
          {node.children.map((child, idx) => (
            <TreeNode 
              key={idx} 
              node={child} 
              level={level + 1} 
              onSelectFile={onSelectFile}
              selectedPath={selectedPath}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default function Discovery({ 
  setActiveTab: setGlobalTab,
  repoUrl, 
  result, 
  setResult,
  loading, 
  setLoading,
  error, 
  setError,
  sessionId,
  setSessionId
}) {
  const hasAutoTriggeredRef = React.useRef(false);
  
  const [activeTab, setActiveTab] = useState('business');
  
  const [treeData, setTreeData] = useState(null);
  const [treeLoading, setTreeLoading] = useState(false);
  
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState(null);
  const [fileLoading, setFileLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  
  const [isDownloading, setIsDownloading] = useState(false);

  const [loadingMessage, setLoadingMessage] = useState('Cloning repository files...');

  useEffect(() => {
    if (loading) {
      const timer1 = setTimeout(() => setLoadingMessage('Detecting project properties and files...'), 3000);
      const timer2 = setTimeout(() => setLoadingMessage('Extracting dependency tree...'), 6000);
      const timer3 = setTimeout(() => setLoadingMessage('Querying local RAG knowledge base & consulting AI...'), 9000);
      const timer4 = setTimeout(() => setLoadingMessage('Generating Business & Testing Reports...'), 13000);
      return () => { clearTimeout(timer1); clearTimeout(timer2); clearTimeout(timer3); clearTimeout(timer4); };
    }
  }, [loading]);

  useEffect(() => {
    if (result && repoUrl) {
      const repoNameExtracted = repoUrl.split('/').pop().replace('.git', '');
      fetchTreeData(repoNameExtracted);
    }
  }, [result, repoUrl]);

  useEffect(() => {
    const runAnalysis = async () => {
      if (!repoUrl) return;
      if (setLoading) setLoading(true);
      if (setError) setError(null);
      if (setResult) setResult(null);

      try {
        const data = await analyzeRepository(repoUrl, '', '', sessionId);
        if (data.errorMessage) {
          if (setError) setError(data.errorMessage);
        } else {
          if (setResult) setResult(data);
          if (setSessionId && data.sessionId) setSessionId(data.sessionId);
          
          // Automatically run the project in the backend silently
          const repoNameExtracted = repoUrl.split('/').pop().replace('.git', '');
          try {
            await startProject(repoNameExtracted);
          } catch(e) {
            console.error("Auto-start project failed", e);
          }
        }
      } catch (err) {
        if (setError) setError(err.response?.data?.message || err.message || 'An error occurred during repository analysis.');
      } finally {
        if (setLoading) setLoading(false);
      }
    };

    if (repoUrl && !result && !loading && !error && !hasAutoTriggeredRef.current) {
      hasAutoTriggeredRef.current = true;
      runAnalysis();
    }
  }, [repoUrl, result, loading, error, setResult, setLoading, setError, sessionId, setSessionId]);

  const fetchTreeData = async (repositoryId) => {
    setTreeLoading(true);
    try {
      const data = await getRepositoryTree(repositoryId);
      setTreeData(data.nodes || []);
    } catch (err) {
      console.error('Failed to load tree:', err);
    } finally {
      setTreeLoading(false);
    }
  };

  const handleSelectFile = async (node) => {
    setSelectedFile(node);
    setFileLoading(true);
    setFileContent(null);
    
    try {
      const repositoryId = repoUrl.split('/').pop().replace('.git', '');
      const data = await getRepositoryFileContent(repositoryId, node.path);
      if (data.previewSupported) {
        setFileContent(data.content);
      } else {
        setFileContent('// Preview not supported for this file type.');
      }
    } catch (err) {
      setFileContent('// Failed to load file content.');
    } finally {
      setFileLoading(false);
    }
  };

  const handleCopy = () => {
    if (fileContent) {
      navigator.clipboard.writeText(fileContent);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = async () => {
    setIsDownloading(true);
    try {
      const repoName = repoUrl.split('/').pop().replace('.git', '');
      let endpoint = '';
      let defaultFilename = '';
      
      if (activeTab === 'business') {
        endpoint = `/api/brd/download/${encodeURIComponent(repoUrl)}`;
        defaultFilename = `BRD_${repoName}.pdf`;
      } else {
        endpoint = `/api/reports/api-test-cases/download/${encodeURIComponent(repoName)}`;
        defaultFilename = `functional-test-plan-${repoName}.html`;
      }
      
      const response = await fetch(endpoint);
      if (!response.ok) {
        throw new Error('Failed to download report');
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = defaultFilename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error(err);
      alert('Error downloading report. Ensure the backend server is running and the endpoint exists.');
    } finally {
      setIsDownloading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] space-y-6">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-[#F5F3FF] border-t-[#5C36E0] rounded-full animate-spin"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <Zap size={20} className="text-[#5C36E0] animate-pulse" />
          </div>
        </div>
        <div className="text-center space-y-2">
          <h2 className="text-lg font-bold text-[#111827]">Analyzing Project</h2>
          <p className="text-[#6B7280] font-medium animate-pulse">{loadingMessage}</p>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh]">
        <div className="text-center space-y-4">
          <Search size={48} className="mx-auto text-[#9CA3AF]" />
          <h2 className="text-xl font-bold text-[#111827]">No Analysis Data</h2>
          <p className="text-[#6B7280]">Please connect a repository first to view discovery insights.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full animate-fadeIn space-y-6 relative pb-24">
      
      {/* ── TOP SECTION: EXISTING TEST COVERAGE ── */}
      <div className="bg-white rounded-[24px] shadow-[0_4px_24px_rgb(0,0,0,0.03)] border border-[#F3F4F6] p-6">
        <h3 className="text-[16px] font-extrabold text-[#111827] mb-6">Existing Test Coverage Analysis</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl text-center">
            <p className="text-[11px] font-extrabold text-[#64748B] uppercase tracking-wider mb-1">Total Tests</p>
            <p className="text-[24px] font-black text-[#0F172A]">{result.testCasesCount || 0}</p>
          </div>
          <div className="p-4 bg-[#F0FDF4] border border-[#BBF7D0] rounded-2xl text-center">
            <p className="text-[11px] font-extrabold text-[#166534] uppercase tracking-wider mb-1">Passed</p>
            <p className="text-[24px] font-black text-[#15803D]">{result.testCasesPassed || 0}</p>
          </div>
          <div className="p-4 bg-[#FEF2F2] border border-[#FECACA] rounded-2xl text-center">
            <p className="text-[11px] font-extrabold text-[#991B1B] uppercase tracking-wider mb-1">Failed</p>
            <p className="text-[24px] font-black text-[#B91C1C]">{result.testCasesFailed || 0}</p>
          </div>
          <div className="p-4 bg-[#F5F3FF] border border-[#DDD6FE] rounded-2xl text-center flex flex-col justify-center">
            <p className="text-[11px] font-extrabold text-[#5C36E0] uppercase tracking-wider mb-1">Testing Types</p>
            <p className="text-[13px] font-black text-[#4C1D95] leading-tight">
              {(Array.isArray(result.testingTypes) && result.testingTypes.length > 0) ? result.testingTypes.join(', ') : 'Not Detected'}
            </p>
          </div>
        </div>
      </div>

      {/* ── TOP SECTION: SPLIT LAYOUT ── */}
      <div className="flex flex-col lg:flex-row gap-6 h-[550px]">
        
        {/* LEFT: Repository Explorer */}
        <div className="w-full lg:w-[45%] bg-white rounded-[24px] shadow-[0_4px_24px_rgb(0,0,0,0.03)] border border-[#F3F4F6] flex flex-col overflow-hidden transition-all duration-300">
          <div className="p-5 border-b border-[#F3F4F6] flex items-center justify-between bg-white z-10 shrink-0">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#F5F3FF] flex items-center justify-center shrink-0">
                <FileSearch size={20} className="text-[#5C36E0]" />
              </div>
              <div>
                <h2 className="text-[16px] font-extrabold text-[#111827]">Repository Explorer</h2>
                <p className="text-[12px] text-[#6B7280]">Browse and inspect project files</p>
              </div>
            </div>
          </div>
          
          <div className="flex flex-1 overflow-hidden relative">
            {/* Tree View (Left Side or Full Width) */}
            <div className={`h-full overflow-y-auto p-4 bg-[#F9FAFB] transition-all duration-300 border-r border-[#F3F4F6] ${selectedFile ? 'w-[30%] shrink-0' : 'w-full'}`}>
              {treeLoading ? (
                <div className="h-full flex items-center justify-center">
                  <span className="text-[#6B7280] text-sm">Loading repository structure...</span>
                </div>
              ) : treeData ? (
                <div className="bg-white border border-[#F3F4F6] rounded-xl p-2 shadow-sm min-h-full">
                  {treeData.map((node, idx) => (
                    <TreeNode 
                      key={idx} 
                      node={node} 
                      onSelectFile={handleSelectFile} 
                      selectedPath={selectedFile?.path} 
                    />
                  ))}
                </div>
              ) : (
                <div className="h-full flex items-center justify-center">
                  <span className="text-[#9CA3AF] text-sm">No files found.</span>
                </div>
              )}
            </div>
            
            {/* Code Viewer (Right Side, takes 70% when file is selected) */}
            {selectedFile && (
              <div className="w-[70%] h-full flex flex-col bg-[#1E1E1E]">
                <div className="flex items-center justify-between px-4 py-3 border-b border-gray-800 bg-[#252526] shrink-0">
                  <div className="flex items-center gap-2 overflow-hidden">
                    <FileCode size={16} className="text-[#5C36E0] shrink-0" />
                    <h3 className="text-[13px] font-semibold text-gray-200 truncate">{selectedFile.name}</h3>
                  </div>
                  <div className="flex items-center gap-1 shrink-0">
                    <button 
                      onClick={handleCopy}
                      className="p-1.5 text-gray-400 hover:text-white hover:bg-gray-700 rounded-md transition-colors"
                      title="Copy Code"
                    >
                      {copied ? <Check size={16} className="text-[#10B981]" /> : <Copy size={16} />}
                    </button>
                    <button 
                      onClick={() => setSelectedFile(null)}
                      className="p-1.5 text-gray-400 hover:text-red-400 hover:bg-gray-700 rounded-md transition-colors"
                      title="Close File"
                    >
                      <X size={16} />
                    </button>
                  </div>
                </div>
                <div className="flex-1 overflow-auto">
                  {fileLoading ? (
                    <div className="h-full flex flex-col items-center justify-center space-y-4">
                      <div className="animate-spin text-[#A5B4FC]"><Zap size={24} /></div>
                      <span className="text-[#9CA3AF] text-sm">Loading source code...</span>
                    </div>
                  ) : (
                    <SyntaxHighlighter
                      language={selectedFile.extension || 'javascript'}
                      style={vscDarkPlus}
                      customStyle={{ margin: 0, padding: '1rem', background: 'transparent', fontSize: '12px' }}
                      showLineNumbers={true}
                      wrapLines={true}
                    >
                      {fileContent || '// Empty file'}
                    </SyntaxHighlighter>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* RIGHT: Analysis Workspace */}
        <div className="w-full lg:w-[55%] bg-white rounded-[24px] shadow-[0_4px_24px_rgb(0,0,0,0.03)] border border-[#F3F4F6] flex flex-col overflow-hidden relative">
          
          {/* Tabs */}
          <div className="flex p-2 bg-[#F9FAFB] border-b border-[#F3F4F6] shrink-0">
            <button 
              onClick={() => setActiveTab('business')}
              className={`flex-1 py-3 text-[14px] font-bold rounded-xl transition-all ${activeTab === 'business' ? 'bg-white text-[#5C36E0] shadow-sm' : 'text-[#6B7280] hover:text-[#111827]'}`}
            >
              Business Report Summary
            </button>
            <button 
              onClick={() => setActiveTab('functional')}
              className={`flex-1 py-3 text-[14px] font-bold rounded-xl transition-all ${activeTab === 'functional' ? 'bg-white text-[#5C36E0] shadow-sm' : 'text-[#6B7280] hover:text-[#111827]'}`}
            >
              Functional Testing Summary
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-6 relative bg-white">
            <AnimatePresence mode="wait">
              {activeTab === 'business' ? (
                <motion.div 
                  key="business"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 10 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-8"
                >
                  {/* Executive Summary */}
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <Target size={18} className="text-[#5C36E0]" />
                      <h3 className="text-[13px] font-extrabold text-[#111827] uppercase tracking-widest">Executive Summary</h3>
                    </div>
                    <div className="p-4 bg-[#F5F3FF] border border-[#DDD6FE] rounded-2xl">
                      <p className="text-[14px] text-[#4C1D95] leading-relaxed font-medium">
                        {result.fullBrdReport?.appPurposeDesc || result.appPurpose || 'Enterprise application built for secure data processing and core business workflows.'}
                      </p>
                    </div>
                  </div>

                  {/* Core Business Modules */}
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <Layers size={18} className="text-[#3B82F6]" />
                      <h3 className="text-[13px] font-extrabold text-[#111827] uppercase tracking-widest">Core Business Modules</h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {(Array.isArray(result.fullBrdReport?.bizComponents) && result.fullBrdReport.bizComponents.length > 0 ? result.fullBrdReport.bizComponents : 
                       (Array.isArray(result.modules) && result.modules.length > 0 ? result.modules : ['Authentication & Identity', 'Data Processing Engine'])).slice(0, 4).map((mod, i) => (
                        <div key={i} className="flex items-start gap-3 p-4 bg-white border border-[#E5E7EB] rounded-2xl hover:shadow-md transition-shadow">
                          <div className="w-8 h-8 rounded-lg bg-[#EFF6FF] flex items-center justify-center shrink-0">
                            <Briefcase size={16} className="text-[#3B82F6]" />
                          </div>
                          <div>
                            <h4 className="text-[14px] font-bold text-[#111827] mb-1">{typeof mod === 'object' ? (mod.name || mod.title || 'Business Component') : mod}</h4>
                            <p className="text-[12px] text-[#6B7280] leading-tight">Critical business capability identified from codebase structure.</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* API Groups and Tech Stack */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <div className="flex items-center gap-2 mb-3">
                        <GitBranch size={18} className="text-[#10B981]" />
                        <h3 className="text-[13px] font-extrabold text-[#111827] uppercase tracking-widest">Detected API Groups</h3>
                      </div>
                      <div className="space-y-3">
                        {(Array.isArray(result.fullBrdReport?.apiGroups) && result.fullBrdReport.apiGroups.length > 0 ? result.fullBrdReport.apiGroups : ['Core Logic APIs']).slice(0, 4).map((flow, i) => (
                          <div key={i} className="flex items-center gap-3 p-3 bg-[#F9FAFB] rounded-xl border border-[#F3F4F6]">
                            <CheckCircle2 size={16} className="text-[#10B981]" />
                            <span className="text-[13px] text-[#374151] font-semibold">{typeof flow === 'object' ? (flow.name || flow.title || 'API Endpoints') : flow}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <div className="flex items-center gap-2 mb-3">
                        <Users size={18} className="text-[#F59E0B]" />
                        <h3 className="text-[13px] font-extrabold text-[#111827] uppercase tracking-widest">Tech Stack Profile</h3>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {(Array.isArray(result.fullBrdReport?.techStackSummary) && result.fullBrdReport.techStackSummary.length > 0 ? result.fullBrdReport.techStackSummary : [result.projectType, result.database]).slice(0, 6).map((role, i) => (
                          <span key={i} className="px-3 py-1.5 bg-white text-[#4B5563] text-[12px] font-bold rounded-lg border border-[#E5E7EB] shadow-sm flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-[#F59E0B]" />
                            {typeof role === 'object' ? (role.name || role.technology || role.tool || role.language || 'Technology') : role}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ) : (
                <motion.div 
                  key="functional"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 10 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-8"
                >
                  {/* Functional Metrics Removed */}

                  {/* Testing Scope */}
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <Search size={18} className="text-[#3B82F6]" />
                      <h3 className="text-[13px] font-extrabold text-[#111827] uppercase tracking-widest">Generated Testing Scope</h3>
                    </div>
                    <p className="text-[14px] text-[#4B5563] leading-relaxed font-medium bg-white p-0">
                      The AI has formulated a comprehensive end-to-end testing strategy encompassing UI functional workflows, backend API contract verification, integration handshakes, and database transaction consistency checks.
                    </p>
                  </div>

                  {/* Functional Areas */}
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <ShieldCheck size={18} className="text-[#10B981]" />
                      <h3 className="text-[13px] font-extrabold text-[#111827] uppercase tracking-widest">Identified Test Suites</h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {[
                        { title: 'Authentication Suite', desc: 'Login, Registration, Password Reset, JWT validation' },
                        { title: 'Dashboard Analytics', desc: 'Chart rendering, Data aggregation, Date filtering' },
                        { title: 'Settings Configuration', desc: 'User preferences, Role assignments, API keys' },
                        { title: 'Data Export Engine', desc: 'CSV/PDF generation, Background jobs, Email delivery' }
                      ].map((area, i) => (
                        <div key={i} className="p-4 border border-[#E5E7EB] rounded-2xl bg-white shadow-sm hover:border-[#10B981] transition-colors group">
                          <h4 className="text-[14px] font-bold text-[#111827] mb-1 group-hover:text-[#10B981] transition-colors">{area.title}</h4>
                          <p className="text-[12px] text-[#6B7280]">{area.desc}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {/* High Risk */}
                  <div className="p-4 bg-[#FFF7ED] border border-[#FFEDD5] rounded-2xl flex gap-3 items-start">
                    <AlertTriangle size={20} className="text-[#EA580C] shrink-0 mt-0.5" />
                    <div>
                      <h4 className="text-[14px] font-bold text-[#9A3412] mb-1">Testing Recommendations</h4>
                      <p className="text-[13px] text-[#C2410C]">Due to complex data structures, we highly recommend executing the API functional test suite first before proceeding to UI automation.</p>
                    </div>
                  </div>
                  
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <div className="p-5 bg-[#F9FAFB] border-t border-[#F3F4F6] mt-auto shrink-0 flex items-center justify-between">
            <p className="text-xs text-[#6B7280] font-medium">Ready to review the complete documentation?</p>
            <button 
              onClick={handleDownload}
              disabled={isDownloading}
              className="flex items-center justify-center gap-2 px-6 py-2.5 bg-[#5C36E0] hover:bg-[#4C28CA] text-white font-bold rounded-xl transition-all shadow-sm disabled:opacity-70"
            >
              {isDownloading ? (
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <Download size={16} />
              )}
              {activeTab === 'business' ? 'Download BRD Report' : 'Download Test Plan'}
            </button>
          </div>
        </div>
      </div>

      {/* ── BOTTOM SECTION: APPLICATION OVERVIEW ── */}
      <div className="bg-white rounded-[24px] shadow-[0_4px_24px_rgb(0,0,0,0.03)] border border-[#F3F4F6] p-8">
        
        {/* Heading */}
        <h3 className="text-[16px] font-extrabold text-[#111827] mb-6">Overview</h3>

        {/* 1st Image Content: Metrics Grid */}
        <div className="flex flex-wrap gap-4 mb-10">
          
          <div className="flex items-center gap-3 p-4 bg-white border border-[#F3F4F6] rounded-2xl shadow-sm min-w-[200px] flex-1">
            <div className="w-10 h-10 flex items-center justify-center">
              {/* Fake Java Logo SVG */}
              <svg viewBox="0 0 128 128" className="w-8 h-8">
                <path fill="#5382A1" d="M75.2 60.1c-12.8-5.9-29.3-5-39 1.1-1.3.8-3.4 3.7-2 4.4 1.7.8 7.2-2 9-2.5 12.1-3.6 28.5-3.3 40.5 2.1 2.5 1.1 6.5 4 8.2 2.3 1.8-1.7-5-5-16.7-7.4z"/>
                <path fill="#5382A1" d="M78.6 69.8c-14.7-5.5-35-5-46.7 1.1-1.5.8-3.9 4.3-2.3 5 1.9.9 8.2-2.3 10.3-2.9 14.1-4.2 33.3-3.8 47.4 2.4 3 1.3 7.6 4.7 9.5 2.7 2.1-2.1-5.8-5.8-18.2-8.3z"/>
                <path fill="#F8981D" d="M85 81c-16.5-5-40-5-53.5.5-1.7.7-4.5 4.5-2.6 5.3 2.1.8 9.5-2.6 11.8-3.3 16-4.5 38.3-4.5 54.5 1.7 3.5 1.4 8.7 5 11 2.8 2.2-2.4-6.5-6-21.2-7z"/>
                <path fill="#5382A1" d="M109.8 71.9c-1.5-1.9-4.8-2.6-8.2-3.1.2.7.3 1.4.3 2.2 0 1.2-.3 2.3-.9 3.2 4.6.6 8 2.5 8 4.7 0 3-6.6 5.6-16.6 6.5 2.4 1.4 4.1 3 5 4.8 11.8-1.5 19.3-4.9 19.3-8.8.1-4.6-6.9-9.5-6.9-9.5z"/>
                <path fill="#5382A1" d="M60.4 40.5c.3-4.9 3.9-9.9 6.2-13.8-5.3 4-11.2 10.3-10.4 17.5.3 2.5 2 4.5 2.4 7 .4 2.7-1.1 4.7-2.7 6.6 3.1-1.9 6.2-5 6-8.7-.3-3.5-1.8-5.7-1.5-8.6z"/>
                <path fill="#5382A1" d="M48.1 43.1c.3-4.5 3.5-9 5.7-12.6-4.8 3.7-10.1 9.4-9.4 16 .3 2.3 1.8 4.1 2.2 6.4.4 2.4-1 4.3-2.5 6 2.8-1.7 5.7-4.5 5.4-7.9-.1-3.2-1.6-5.2-1.4-7.9z"/>
                <path fill="#5382A1" d="M72.9 36.6c.3-4.9 3.9-9.9 6.2-13.8-5.3 4-11.2 10.3-10.4 17.5.3 2.5 2 4.5 2.4 7 .4 2.7-1.1 4.7-2.7 6.6 3.1-1.9 6.2-5 6-8.7-.2-3.5-1.7-5.7-1.5-8.6z"/>
              </svg>
            </div>
            <div>
              <p className="text-[12px] font-bold text-[#6B7280] mb-0.5">Language</p>
              <p className="text-[15px] font-extrabold text-[#111827]">{result.projectType || 'Java'} {result.detectedJavaVersion || ''}</p>
            </div>
          </div>

          <div className="flex items-center gap-3 p-4 bg-white border border-[#F3F4F6] rounded-2xl shadow-sm min-w-[200px] flex-1">
            <div className="w-10 h-10 flex items-center justify-center">
              <svg viewBox="0 0 24 24" className="w-7 h-7 text-[#6DB33F]" fill="currentColor">
                <path d="M22 12c0 5.523-4.477 10-10 10S2 17.523 2 12 6.477 2 12 2s10 4.477 10 10zm-3.228-3.088c-.02-.12-.047-.234-.078-.344a6.452 6.452 0 0 0-4.072-4.148 5.772 5.772 0 0 0-3.32-.236c-1.397.351-2.57 1.196-3.393 2.378-.445.642-.772 1.353-.96 2.083a6.837 6.837 0 0 0-.17 1.545c.01.691.135 1.365.372 2.008a6.51 6.51 0 0 0 2.227 2.871 6.368 6.368 0 0 0 3.167 1.11 6.53 6.53 0 0 0 3.325-.436A6.67 6.67 0 0 0 18.23 13.5c.34-.648.55-1.353.618-2.066.027-.3.023-.6 0-.9l-.076-.622zM12.5 16.5c-2.485 0-4.5-2.015-4.5-4.5s2.015-4.5 4.5-4.5 4.5 2.015 4.5 4.5-2.015 4.5-4.5 4.5z"/>
              </svg>
            </div>
            <div>
              <p className="text-[12px] font-bold text-[#6B7280] mb-0.5">Framework</p>
              <p className="text-[15px] font-extrabold text-[#111827]">
                {result.frameworkType || 'Spring Boot'} {result.frameworkVersions && typeof result.frameworkVersions === 'object' ? Object.values(result.frameworkVersions).join(', ') : ''}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 p-4 bg-white border border-[#F3F4F6] rounded-2xl shadow-sm min-w-[200px] flex-1">
            <div className="w-10 h-10 flex items-center justify-center">
              <svg viewBox="0 0 24 24" className="w-7 h-7" fill="none">
                <path d="M12 22C12 22 17 19 19 12C20.5 6 18 2 18 2C18 2 13 4 12 7C11 4 6 2 6 2C6 2 3.5 6 5 12C7 19 12 22 12 22Z" fill="#C71A22"/>
                <path d="M12 22C12 22 17 19 19 12C20.5 6 18 2 18 2C18 2 15 2 12 6" fill="#F05A28"/>
                <path d="M12 22C12 22 17 19 19 12C20.5 6 18 2 18 2" fill="#ECA72C"/>
              </svg>
            </div>
            <div>
              <p className="text-[12px] font-bold text-[#6B7280] mb-0.5">Build Tool</p>
              <p className="text-[15px] font-extrabold text-[#111827]">{result.buildTool || 'Maven'}</p>
            </div>
          </div>
          
          <div className="w-full h-0"></div> {/* Line break */}

          <div className="flex items-center gap-3 p-4 bg-white border border-[#F3F4F6] rounded-2xl shadow-sm min-w-[160px] flex-1">
            <div className="w-10 h-10 flex items-center justify-center shrink-0">
              <FileText size={24} className="text-[#9CA3AF]" strokeWidth={1.5} />
            </div>
            <div>
              <p className="text-[12px] font-bold text-[#6B7280] mb-0.5">App Name</p>
              <p className="text-[14px] font-extrabold text-[#111827] break-words">{result.fullBrdReport?.appName || result.projectName || 'Application'}</p>
            </div>
          </div>

          <div className="flex items-center gap-3 p-4 bg-white border border-[#F3F4F6] rounded-2xl shadow-sm min-w-[160px] flex-1">
            <div className="w-10 h-10 flex items-center justify-center shrink-0">
              <Users size={24} className="text-[#5C36E0]" strokeWidth={1.5} />
            </div>
            <div>
              <p className="text-[12px] font-bold text-[#6B7280] mb-0.5">Packaging</p>
              <p className="text-[15px] font-extrabold text-[#111827]">{result.packagingType || 'Jar'}</p>
            </div>
          </div>

          <div className="flex items-center gap-3 p-4 bg-white border border-[#F3F4F6] rounded-2xl shadow-sm min-w-[160px] flex-1">
            <div className="w-10 h-10 flex items-center justify-center shrink-0">
              <Layout size={24} className="text-[#5C36E0]" strokeWidth={1.5} />
            </div>
            <div>
              <p className="text-[12px] font-bold text-[#6B7280] mb-0.5">Module Type</p>
              <p className="text-[15px] font-extrabold text-[#111827]">{result.isMultiModule ? 'Multi-Module' : 'Single Module'}</p>
            </div>
          </div>

          <div className="flex items-center gap-3 p-4 bg-white border border-[#F3F4F6] rounded-2xl shadow-sm min-w-[160px] flex-1">
            <div className="w-10 h-10 flex items-center justify-center shrink-0">
              <ShieldCheck size={24} className="text-[#10B981]" strokeWidth={1.5} />
            </div>
            <div>
              <p className="text-[12px] font-bold text-[#6B7280] mb-0.5">Risk Level</p>
              <p className="text-[15px] font-extrabold text-[#111827]">{result.riskLevel || 'Low'}</p>
            </div>
          </div>
        </div>

        {/* 2nd Image Content: Business Workflow */}
        <h3 className="text-[16px] font-extrabold text-[#111827] mb-6">Business Workflow (High Level)</h3>
        
        <div className="flex flex-nowrap items-center gap-3 overflow-x-auto pb-4 hide-scrollbar">
          
          {[
            { title: 'Login', desc: 'Authenticate User', icon: <Users size={20} className="text-[#5C36E0]" />, bg: 'bg-[#F5F3FF]', text: 'text-[#5C36E0]' },
            { title: 'Dashboard', desc: 'View Summary & Analytics', icon: <Layout size={20} className="text-[#2563EB]" />, bg: 'bg-[#EFF6FF]', text: 'text-[#2563EB]' },
            { title: 'Student Management', desc: 'Add / Update Students', icon: <Users size={20} className="text-[#16A34A]" />, bg: 'bg-[#F0FDF4]', text: 'text-[#16A34A]' },
            { title: 'Course Management', desc: 'Manage Courses & Subjects', icon: <FileText size={20} className="text-[#D97706]" />, bg: 'bg-[#FFFBEB]', text: 'text-[#D97706]' },
            { title: 'Attendance', desc: 'Track Student Attendance', icon: <CheckCircle2 size={20} className="text-[#E11D48]" />, bg: 'bg-[#FFF1F2]', text: 'text-[#E11D48]' },
            { title: 'Reports', desc: 'Generate Reports', icon: <FileText size={20} className="text-[#5C36E0]" />, bg: 'bg-[#F5F3FF]', text: 'text-[#5C36E0]' },
          ].map((step, idx, arr) => (
            <React.Fragment key={idx}>
              <div className="flex flex-col items-center justify-center text-center p-5 bg-white border border-[#F3F4F6] rounded-2xl shadow-sm min-w-[160px] h-[160px] shrink-0">
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-3 ${step.bg}`}>
                  {step.icon}
                </div>
                <h4 className="text-[14px] font-extrabold text-[#111827] mb-1">{step.title}</h4>
                <p className="text-[11px] text-[#6B7280] font-medium leading-tight px-2">{step.desc}</p>
              </div>
              
              {idx < arr.length - 1 && (
                <div className="shrink-0 text-[#9CA3AF]">
                  <ArrowRight size={20} />
                </div>
              )}
            </React.Fragment>
          ))}

        </div>
      </div>

      {/* ── BOTTOM NAVIGATION ── */}
      <div className="flex justify-between items-center mt-8">
        <button
          type="button"
          onClick={(e) => {
            e.preventDefault();
            if (setGlobalTab) setGlobalTab('dashboard');
            setTimeout(() => {
              const mainEl = document.querySelector('main');
              if (mainEl) mainEl.scrollTop = 0;
            }, 50);
          }}
          className="px-8 py-3 bg-[#10B981] hover:bg-[#059669] text-white text-[15px] font-bold rounded-xl transition-all shadow-md z-50 relative pointer-events-auto"
        >
          Back
        </button>
        <button
          type="button"
          onClick={(e) => {
            e.preventDefault();
            if (setGlobalTab) setGlobalTab('test-recommendation');
            setTimeout(() => {
              const mainEl = document.querySelector('main');
              if (mainEl) mainEl.scrollTop = 0;
            }, 50);
          }}
          className="px-8 py-3 bg-[#5C36E0] hover:bg-[#4C28CA] text-white text-[15px] font-bold rounded-xl transition-all shadow-md flex items-center gap-2 z-50 relative pointer-events-auto"
        >
          Continue <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
}