import React, { useState, useEffect } from 'react';
import { GitBranch, Play, CheckCircle, Search, Layers, Folder, FolderOpen, File, FileText, FileCode, FileImage, FileArchive, ChevronRight, ChevronDown, Check, Activity, ShieldCheck, Box, Server, Database, Loader2, ArrowRight, Layout, X, AlertCircle, Download, AlertTriangle } from 'lucide-react';
import { analyzeRepository, getRepositoryTree, getRepositoryFileContent, API_BASE_URL } from '../api';
import { motion } from 'framer-motion';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const FileIcon = ({ type, extension, expanded }) => {
  if (type === 'folder') {
    return expanded ? <FolderOpen size={16} className="text-blue-500" /> : <Folder size={16} className="text-blue-500" />;
  }
  
  const ext = (extension || '').toLowerCase();
  if (['js', 'jsx', 'ts', 'tsx', 'py', 'java', 'cpp', 'c', 'cs', 'go', 'rs', 'php', 'rb'].includes(ext)) {
    return <FileCode size={16} className="text-emerald-500" />;
  }
  if (['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico'].includes(ext)) {
    return <FileImage size={16} className="text-purple-500" />;
  }
  if (['zip', 'tar', 'gz', 'rar', '7z', 'jar', 'war'].includes(ext)) {
    return <FileArchive size={16} className="text-rose-500" />;
  }
  if (['json', 'xml', 'yaml', 'yml', 'md', 'txt', 'csv'].includes(ext)) {
    return <FileText size={16} className="text-amber-500" />;
  }
  
  return <File size={16} className="text-slate-400" />;
};

const TreeNode = ({ node, level = 0, onSelect, selectedPath, currentPath = '' }) => {
  const [expanded, setExpanded] = useState(level < 1);
  const isFolder = node.type === 'folder';
  const path = node.path || (currentPath ? `${currentPath}/${node.name}` : node.name);
  
  const isSelected = selectedPath === path;

  return (
    <div className="select-none">
      <div 
        onClick={() => {
          if (isFolder) {
            setExpanded(!expanded);
          } else {
            if (onSelect) onSelect(node, path);
          }
        }}
        className={`flex items-center gap-1.5 py-1.5 px-2 rounded-md transition-colors ${
          isSelected ? 'bg-blue-50 text-blue-700' : 'hover:bg-slate-50 text-slate-700'
        } ${isFolder ? 'cursor-pointer' : 'cursor-pointer'}`}
        style={{ paddingLeft: `${level * 16 + 8}px` }}
      >
        <span className="w-4 h-4 flex items-center justify-center shrink-0">
          {isFolder && (
            expanded ? <ChevronDown size={14} className="text-slate-400" /> : <ChevronRight size={14} className="text-slate-400" />
          )}
        </span>
        <FileIcon type={node.type} extension={node.extension} expanded={expanded} />
        <span className="text-sm truncate font-medium">{node.name}</span>
      </div>
      
      {isFolder && expanded && node.children && (
        <div className="flex flex-col">
          {node.children.map((child, idx) => (
            <TreeNode 
              key={idx} 
              node={child} 
              level={level + 1} 
              onSelect={onSelect}
              selectedPath={selectedPath}
              currentPath={path}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default function Discovery({ 
  setActiveTab, 
  repoUrl, 
  loading, 
  setLoading, 
  result, 
  setResult, 
  error, 
  setError, 
  statusText, 
  setStatusText,
  timeTaken,
  setTimeTaken,
  workflowState,
  setWorkflowState,
  sessionId,
  setSessionId
}) {
  const [treeData, setTreeData] = useState(null);
  const [treeLoading, setTreeLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState(null);
  const [loadingContent, setLoadingContent] = useState(false);
  const [activeRightTab, setActiveRightTab] = useState('business');

  const fetchTreeData = async (repositoryId) => {
    setTreeLoading(true);
    try {
      const data = await getRepositoryTree(repositoryId);
      setTreeData({
        type: 'folder',
        name: repositoryId,
        children: data.nodes || []
      });
    } catch (err) {
      console.error('Failed to load repository tree.', err);
    } finally {
      setTreeLoading(false);
    }
  };

  const handleFileSelect = async (node, path) => {
    setSelectedFile({ node, path });
    setLoadingContent(true);
    try {
      const repositoryId = repoUrl.split('/').pop().replace('.git', '');
      const content = await getRepositoryFileContent(repositoryId, path);
      setFileContent(content?.content || '');
    } catch(err) {
      setFileContent('Error loading file content.');
    } finally {
      setLoadingContent(false);
    }
  };

  const handleAnalyze = async () => {
    if (!repoUrl) return;
    setLoading(true);
    setError(null);
    setStatusText('Initializing repository...');
    
    try {
      const startTime = Date.now();
      const payload = await analyzeRepository(repoUrl, (status) => {
        setStatusText(status);
      });
      const endTime = Date.now();
      
      setResult(payload.analysis);
      setSessionId(payload.sessionId);
      setTimeTaken(((endTime - startTime) / 1000).toFixed(1));
      
      if (typeof setWorkflowState === 'function') {
        setWorkflowState(prev => ({ ...prev, analysisCompleted: true }));
      }
      
      const repositoryId = repoUrl.split('/').pop().replace('.git', '');
      fetchTreeData(repositoryId);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Analysis failed');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (repoUrl && !result && !loading && !error) {
      handleAnalyze();
    } else if (result && !treeData && !treeLoading) {
       const repositoryId = repoUrl.split('/').pop().replace('.git', '');
       fetchTreeData(repositoryId);
    }
  }, [repoUrl, result]);

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center h-full min-h-[60vh] relative overflow-hidden">
        {/* Ambient Glow */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="w-[500px] h-[500px] bg-[#5B5FF6]/10 rounded-full blur-[120px] animate-pulse"></div>
        </div>

        <div className="relative flex flex-col items-center z-10">
          <div className="relative w-40 h-40 mb-12 flex items-center justify-center">
            
            {/* Outer Spinning Ring - Dash */}
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ duration: 12, repeat: Infinity, ease: "linear" }}
              className="absolute inset-0 rounded-full border-[1.5px] border-dashed border-[#5B5FF6]/30"
            ></motion.div>
            
            {/* Middle Spinning Ring - Solid with Gradient */}
            <motion.div 
              animate={{ rotate: -360 }}
              transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
              className="absolute inset-4 rounded-full border-[3px] border-transparent border-t-[#5B5FF6] border-r-indigo-300"
            ></motion.div>
            
            {/* Inner Pulsing Core Glow */}
            <motion.div 
              animate={{ scale: [1, 1.25, 1], opacity: [0.4, 0.8, 0.4] }}
              transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
              className="absolute inset-8 bg-gradient-to-br from-[#5B5FF6] to-[#7B61FF] rounded-full blur-md"
            ></motion.div>
            
            {/* Center Orb */}
            <motion.div 
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
              className="absolute inset-10 bg-white rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(91,95,246,0.4)] z-20"
            >
              <Search size={34} className="text-[#5B5FF6]" strokeWidth={2.5} />
            </motion.div>

            {/* Orbiting Satellite 1 */}
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
              className="absolute inset-0"
            >
              <div className="w-3.5 h-3.5 bg-indigo-400 rounded-full shadow-[0_0_12px_rgba(99,102,241,0.9)] absolute -top-1.5 left-1/2 -translate-x-1/2"></div>
            </motion.div>

            {/* Orbiting Satellite 2 */}
            <motion.div 
              animate={{ rotate: -360 }}
              transition={{ duration: 5, repeat: Infinity, ease: "linear" }}
              className="absolute inset-[-12px]"
            >
              <div className="w-2 h-2 bg-blue-400 rounded-full shadow-[0_0_10px_rgba(96,165,250,0.9)] absolute top-1/2 -right-1 -translate-y-1/2"></div>
            </motion.div>
          </div>

          <motion.h2 
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-3xl font-black text-[#101828] mb-6 text-center tracking-tight drop-shadow-sm"
          >
            Analyzing Repository
          </motion.h2>
          
          <div className="relative overflow-hidden rounded-full px-8 py-3 bg-indigo-50/80 backdrop-blur-sm border border-indigo-100 shadow-inner min-w-[300px]">
            <motion.p 
              key={statusText}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-[#5B5FF6] font-bold text-center text-sm uppercase tracking-wider"
            >
              {statusText || 'Mapping business logic...'}
            </motion.p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center h-full">
        <div className="w-16 h-16 rounded-full bg-red-100 flex items-center justify-center mb-6">
          <AlertTriangle size={32} className="text-red-500" />
        </div>
        <h2 className="text-2xl font-bold text-[#101828] mb-3">Analysis Failed</h2>
        <p className="text-red-500 mb-8 max-w-lg text-center bg-red-50 p-4 rounded-xl border border-red-100 font-medium">
          {error}
        </p>
        <button 
          onClick={handleAnalyze} 
          className="px-8 py-3 bg-[#5B5FF6] text-white rounded-xl font-bold shadow-sm hover:bg-[#4a4fcc] transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (!result) return null;

  const repoName = repoUrl.split('/').pop().replace('.git', '');
  const appPurpose = result.fullBrdReport?.appPurposeDesc || result.description || 'Application purpose mapped successfully.';
  const bizComponents = result.fullBrdReport?.bizComponents || result.detectedComponents || ['Authentication', 'User Management', 'Data Processing'];
  const techStack = result.fullBrdReport?.techStackSummary || result.dependencies || ['Java', 'Spring', 'Maven', 'JUnit'];
  
  const testMetrics = result.testMetrics || { total: 0, passed: 0, failed: 0, type: 'Not Detected' };
  
  const uiComponents = result.fullBrdReport?.uiComponents || [];
  const testSuites = uiComponents.length > 0 
    ? uiComponents.map(ui => ({ name: typeof ui === 'string' ? ui : ui.name || 'Component Suite', desc: 'UI Functional Tests' }))
    : [
        { name: 'Authentication Suite', desc: 'Login, Registration, Password Reset, JWT validation' },
        { name: 'Dashboard Analytics', desc: 'Chart rendering, Data aggregation, Data filtering' },
        { name: 'Settings Configuration', desc: 'User preferences, Role assignments, API keys' },
        { name: 'Data Report Engine', desc: 'CSV/PDF generation, Background jobs, Email delivery' }
      ];

  const getDynamicWorkflowSteps = () => {
    const brd = result.fullBrdReport;
    if (!brd) return null;
    
    const extractName = (obj) => {
      if (typeof obj === 'string') return obj;
      return obj?.title || obj?.name || obj?.screen || obj?.step || obj?.process || obj?.program || obj?.code || 'Business Step';
    };

    const extractDesc = (obj, defaultDesc) => {
      if (typeof obj === 'string') return defaultDesc;
      return obj?.description || obj?.desc || obj?.actor ? `Actor: ${obj?.actor}` : defaultDesc;
    };

    if (brd.keyScreenFlows && brd.keyScreenFlows.length > 0) {
      return brd.keyScreenFlows.map(flow => ({ title: extractName(flow), desc: extractDesc(flow, 'Screen Flow') }));
    }
    if (brd.activityFlows && brd.activityFlows.length > 0) {
      return brd.activityFlows.map(flow => ({ title: extractName(flow), desc: extractDesc(flow, 'Activity Flow') }));
    }
    if (brd.useCases && brd.useCases.length > 0) {
      return brd.useCases.map(uc => ({ title: extractName(uc), desc: extractDesc(uc, 'Use Case') }));
    }
    if (brd.keyTransactions && brd.keyTransactions.length > 0) {
      return brd.keyTransactions.map(t => ({ title: extractName(t), desc: extractDesc(t, 'Transaction') }));
    }
    if (brd.onlineTransactions && brd.onlineTransactions.length > 0) {
      return brd.onlineTransactions.map(t => ({ title: extractName(t), desc: extractDesc(t, 'Process') }));
    }
    
    // Fallback to synthesizing from UI components
    const uic = brd.uiComponents || [];
    if (uic.length > 0) {
      return uic.map(c => ({ title: extractName(c), desc: 'Application View' }));
    }
    return null;
  };
  
  const dynamicSteps = getDynamicWorkflowSteps();
  const workflowSteps = dynamicSteps && dynamicSteps.length > 0 ? dynamicSteps : [
      { title: 'Login', desc: 'Authenticate User' },
      { title: 'Dashboard', desc: 'View Summary & Analytics' },
      { title: 'Student Management', desc: 'Add / Update Students' },
      { title: 'Course Management', desc: 'Manage Courses & Subjects' },
      { title: 'Attendance', desc: 'Track Student Attendance' },
      { title: 'Reports', desc: 'Generate Reports' }
  ];

  const stepStyles = [
    { bg: 'bg-indigo-50', text: 'text-[#5B5FF6]', icon: <ShieldCheck size={20} /> },
    { bg: 'bg-blue-50', text: 'text-blue-500', icon: <Layout size={20} /> },
    { bg: 'bg-emerald-50', text: 'text-emerald-500', icon: <Server size={20} /> },
    { bg: 'bg-orange-50', text: 'text-orange-500', icon: <FileText size={20} /> },
    { bg: 'bg-rose-50', text: 'text-rose-500', icon: <CheckCircle size={20} /> },
    { bg: 'bg-purple-50', text: 'text-purple-500', icon: <File size={20} /> }
  ];

  const handleDownload = (type) => {
    let url = '';
    if (type === 'brd') {
      url = `${API_BASE_URL}/brd/download/${encodeURIComponent(repoName)}`;
    } else if (type === 'test-plan') {
      url = `${API_BASE_URL}/reports/ui-functional-test/download/${encodeURIComponent(repoName)}`;
    }
    
    if (url) {
      window.open(url, '_blank');
    }
  };
  
  return (
    <div className="flex flex-col gap-6 animate-fadeIn w-full max-w-7xl mx-auto pb-10">
      
      <div className="mb-6 mt-4">
        <h2 className="text-lg font-bold text-[#101828] mb-4 flex items-center gap-2 tracking-tight">
          <Activity className="text-[#5B5FF6]" size={20} /> Existing Test Coverage Analysis
        </h2>
        <div className="grid grid-cols-4 gap-5">
          <div className="bg-white rounded-2xl p-5 border border-slate-100 shadow-[0_2px_10px_rgba(0,0,0,0.02)] hover:shadow-[0_8px_30px_rgba(0,0,0,0.06)] hover:-translate-y-1 transition-all duration-300 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-slate-100 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-slate-200 transition-all"></div>
            <div className="text-xs uppercase font-bold text-[#98A2B3] tracking-wider mb-2">Total Tests</div>
            <div className="text-3xl font-black text-[#101828]">{testMetrics.total}</div>
          </div>
          <div className="bg-gradient-to-br from-emerald-50/50 to-emerald-50 rounded-2xl p-5 border border-emerald-100/50 shadow-[0_2px_10px_rgba(16,185,129,0.05)] hover:shadow-[0_8px_30px_rgba(16,185,129,0.15)] hover:-translate-y-1 transition-all duration-300 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-200/40 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-emerald-300/40 transition-all"></div>
            <div className="text-xs uppercase font-bold text-emerald-600 tracking-wider mb-2">Passed</div>
            <div className="text-3xl font-black text-emerald-600">{testMetrics.passed}</div>
          </div>
          <div className="bg-gradient-to-br from-rose-50/50 to-rose-50 rounded-2xl p-5 border border-rose-100/50 shadow-[0_2px_10px_rgba(244,63,94,0.05)] hover:shadow-[0_8px_30px_rgba(244,63,94,0.15)] hover:-translate-y-1 transition-all duration-300 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-rose-200/40 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-rose-300/40 transition-all"></div>
            <div className="text-xs uppercase font-bold text-rose-600 tracking-wider mb-2">Failed</div>
            <div className="text-3xl font-black text-rose-600">{testMetrics.failed}</div>
          </div>
          <div className="bg-gradient-to-br from-indigo-50/50 to-indigo-50 rounded-2xl p-5 border border-indigo-100/50 shadow-[0_2px_10px_rgba(91,95,246,0.05)] hover:shadow-[0_8px_30px_rgba(91,95,246,0.15)] hover:-translate-y-1 transition-all duration-300 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-200/40 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-indigo-300/40 transition-all"></div>
            <div className="text-xs uppercase font-bold text-[#5B5FF6] tracking-wider mb-2">Testing Types</div>
            <div className="text-lg font-black text-[#5B5FF6]">{testMetrics.type}</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
        <div className="lg:col-span-6 bg-white rounded-3xl shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col overflow-hidden h-[480px]">
          <div className="p-5 border-b border-slate-100 shrink-0 bg-gradient-to-r from-white to-slate-50/50">
            <h2 className="text-lg font-bold text-[#101828] flex items-center gap-2">
              <Folder size={20} className="text-[#5B5FF6]" /> Repository Explorer
            </h2>
            <p className="text-xs text-[#667085] mt-1 font-medium">Browse and inspect project files.</p>
          </div>
          
          <div className="flex-1 flex overflow-hidden relative">
            <div className={`flex-1 overflow-y-auto p-4 custom-scrollbar ${selectedFile ? 'hidden md:block w-1/3 border-r border-slate-100 bg-slate-50/30' : 'w-full bg-slate-50/30'}`}>
              {treeLoading ? (
                 <div className="flex items-center justify-center h-full text-[#667085] text-sm font-medium gap-2">
                   <Loader2 size={16} className="animate-spin text-[#5B5FF6]" /> Loading structure...
                 </div>
               ) : treeData && treeData.children ? (
                 <TreeNode node={treeData} onSelect={handleFileSelect} selectedPath={selectedFile?.path} />
               ) : (
                 <div className="flex items-center justify-center h-full text-[#667085] text-sm">
                   Structure not available
                 </div>
               )}
            </div>

            {selectedFile && (
              <div className="flex-[2] flex flex-col overflow-hidden bg-[#0d1117]">
                <div className="flex items-center justify-between px-4 py-3 bg-[#161b22] border-b border-[#30363d] shadow-sm">
                  <div className="flex items-center gap-2 text-slate-200 text-xs font-medium tracking-wide">
                     <FileCode size={16} className="text-emerald-400" /> {selectedFile.node.name}
                  </div>
                  <button onClick={() => setSelectedFile(null)} className="text-slate-400 hover:text-white transition-colors bg-[#21262d] p-1 rounded-md border border-[#30363d]">
                    <X size={14} />
                  </button>
                </div>
                <div className="flex-1 overflow-auto text-sm custom-scrollbar">
                  {loadingContent ? (
                     <div className="flex items-center justify-center h-full text-slate-400 text-sm gap-2">
                       <Loader2 size={16} className="animate-spin text-[#5B5FF6]" /> Loading file...
                     </div>
                  ) : (
                    <SyntaxHighlighter
                      language={selectedFile.node.extension || 'javascript'}
                      style={vscDarkPlus}
                      customStyle={{ margin: 0, background: 'transparent', fontSize: '13px', padding: '16px' }}
                      showLineNumbers={true}
                    >
                      {fileContent || '// Empty file'}
                    </SyntaxHighlighter>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="lg:col-span-6 bg-white rounded-3xl shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col h-[480px]">
          <div className="flex border-b border-slate-100 bg-slate-50/50 rounded-t-3xl p-1">
            <button 
              onClick={() => setActiveRightTab('business')}
              className={`flex-1 py-3 text-sm font-bold rounded-2xl transition-all duration-300 ${activeRightTab === 'business' ? 'bg-white shadow-sm text-[#5B5FF6]' : 'text-[#667085] hover:text-[#101828] hover:bg-white/50'}`}
            >
              Business Report Summary
            </button>
            <button 
              onClick={() => setActiveRightTab('functional')}
              className={`flex-1 py-3 text-sm font-bold rounded-2xl transition-all duration-300 ${activeRightTab === 'functional' ? 'bg-white shadow-sm text-[#5B5FF6]' : 'text-[#667085] hover:text-[#101828] hover:bg-white/50'}`}
            >
              Functional Testing Summary
            </button>
          </div>
          
          <div className="flex-1 overflow-y-auto p-6 custom-scrollbar">
            {activeRightTab === 'business' ? (
              <div className="flex flex-col h-full animate-fadeIn">
                 <div className="mb-6">
                   <h3 className="text-[11px] uppercase tracking-wider font-bold text-[#5B5FF6] flex items-center gap-2 mb-3">
                     <ShieldCheck size={16} /> EXECUTIVE SUMMARY
                   </h3>
                   <div className="bg-gradient-to-r from-indigo-50/50 to-blue-50/30 border border-indigo-100 rounded-2xl p-5 shadow-sm">
                     <p className="text-[#344054] text-[13px] leading-relaxed font-medium">
                       {appPurpose}
                     </p>
                   </div>
                 </div>
                 
                 <div className="flex-1">
                   <h3 className="text-[11px] uppercase tracking-wider font-bold text-[#5B5FF6] flex items-center gap-2 mb-3">
                     <Layers size={16} /> CORE BUSINESS MODULES
                   </h3>
                   <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                     {bizComponents.slice(0, 4).map((module, idx) => (
                       <div key={idx} className="border border-slate-200 rounded-2xl p-4 bg-white shadow-[0_2px_10px_rgba(0,0,0,0.02)] hover:shadow-md hover:border-indigo-200 hover:-translate-y-0.5 transition-all duration-300 flex items-start gap-3 group">
                         <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0 group-hover:scale-110 group-hover:bg-blue-100 transition-transform">
                           <Box size={18} />
                         </div>
                         <div>
                           <div className="text-sm font-bold text-[#101828] group-hover:text-blue-700 transition-colors">{typeof module === 'string' ? module : module.name}</div>
                           <div className="text-[11px] text-[#667085] mt-1 leading-snug">Critical business capability identified from codebase structure.</div>
                         </div>
                       </div>
                     ))}
                   </div>
                 </div>
                 
                 <div className="pt-5 flex items-center justify-between border-t border-slate-100 mt-6">
                    <span className="text-xs text-[#667085] font-medium">Ready to review the complete documentation?</span>
                    <button onClick={() => handleDownload('brd')} className="px-5 py-2.5 bg-gradient-to-r from-[#5B5FF6] to-[#7B61FF] text-white text-sm font-bold rounded-xl shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all flex items-center gap-2">
                      <Download size={16} /> Download BRD Report
                    </button>
                 </div>
              </div>
            ) : (
              <div className="flex flex-col h-full animate-fadeIn">
                 <div className="mb-6">
                   <h3 className="text-[11px] uppercase tracking-wider font-bold text-[#5B5FF6] flex items-center gap-2 mb-3">
                     <Search size={16} /> GENERATED TESTING SCOPE
                   </h3>
                   <p className="text-[#344054] text-[13px] leading-relaxed font-medium">
                     The AI has formulated a comprehensive end-to-end testing strategy encompassing UI functional workflows, backend API contract verification, integration handshakes, and database transaction consistency checks.
                   </p>
                 </div>
                 
                 <div className="mb-6 flex-1">
                   <h3 className="text-[11px] uppercase tracking-wider font-bold text-[#5B5FF6] flex items-center gap-2 mb-3">
                     <CheckCircle size={16} /> IDENTIFIED TEST SUITES
                   </h3>
                   <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {testSuites.slice(0, 4).map((suite, idx) => (
                        <div key={idx} className="border border-slate-200 rounded-2xl p-4 bg-white shadow-[0_2px_10px_rgba(0,0,0,0.02)] hover:shadow-md hover:border-indigo-200 hover:-translate-y-0.5 transition-all duration-300">
                          <div className="text-sm font-bold text-[#101828] mb-1.5">{suite.name}</div>
                          <div className="text-[11px] text-[#667085] leading-snug">{suite.desc}</div>
                        </div>
                      ))}
                   </div>
                 </div>
                 
                 <div className="mb-6">
                   <div className="bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200/60 rounded-2xl p-4 flex items-start gap-3 shadow-sm">
                     <AlertCircle size={18} className="text-orange-500 shrink-0 mt-0.5" />
                     <div>
                       <div className="text-sm font-bold text-orange-800 tracking-tight">Testing Recommendations</div>
                       <div className="text-[12px] text-orange-700/90 mt-1 font-medium leading-snug">Due to complex data structures, we highly recommend executing the API functional test suite first before proceeding to UI automation.</div>
                     </div>
                   </div>
                 </div>
                 
                 <div className="pt-5 flex items-center justify-between border-t border-slate-100">
                    <span className="text-xs text-[#667085] font-medium">Ready to review the complete documentation?</span>
                    <button onClick={() => handleDownload('test-plan')} className="px-5 py-2.5 bg-gradient-to-r from-[#5B5FF6] to-[#7B61FF] text-white text-sm font-bold rounded-xl shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all flex items-center gap-2">
                      <Download size={16} /> Download Test Plan
                    </button>
                 </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-lg font-bold text-[#101828] mb-4 flex items-center gap-2 tracking-tight">
           <Layers className="text-[#5B5FF6]" size={20} /> Project Overview
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
          <div className="bg-white rounded-2xl p-4 shadow-[0_2px_10px_rgba(0,0,0,0.02)] hover:shadow-md hover:-translate-y-1 transition-all border border-slate-100 flex flex-col justify-center gap-2">
             <div className="flex items-center gap-2">
               <span className="w-7 h-7 rounded-lg bg-slate-100 flex items-center justify-center shrink-0">
                 <FileCode size={14} className="text-slate-600" />
               </span>
               <div className="text-[10px] uppercase font-bold text-[#98A2B3] tracking-wider">Language</div>
             </div>
             <div className="text-sm font-black text-[#101828] pl-1">{result.language || 'Java 17'}</div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-[0_2px_10px_rgba(0,0,0,0.02)] hover:shadow-md hover:-translate-y-1 transition-all border border-slate-100 flex flex-col justify-center gap-2 col-span-2">
             <div className="flex items-center gap-2">
               <span className="w-7 h-7 rounded-lg bg-emerald-50 flex items-center justify-center shrink-0">
                 <ShieldCheck size={14} className="text-emerald-600" />
               </span>
               <div className="text-[10px] uppercase font-bold text-[#98A2B3] tracking-wider">Framework</div>
             </div>
             <div className="text-sm font-black text-[#101828] pl-1">{result.framework || 'Spring Boot / Thymeleaf'}</div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-[0_2px_10px_rgba(0,0,0,0.02)] hover:shadow-md hover:-translate-y-1 transition-all border border-slate-100 flex flex-col justify-center gap-2">
             <div className="flex items-center gap-2">
               <span className="w-7 h-7 rounded-lg bg-orange-50 flex items-center justify-center shrink-0">
                 <Database size={14} className="text-orange-600" />
               </span>
               <div className="text-[10px] uppercase font-bold text-[#98A2B3] tracking-wider">Build Tool</div>
             </div>
             <div className="text-sm font-black text-[#101828] pl-1">{techStack.find(t => ['Maven', 'Gradle', 'npm', 'yarn'].includes(t)) || 'Maven'}</div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-[0_2px_10px_rgba(0,0,0,0.02)] hover:shadow-md hover:-translate-y-1 transition-all border border-slate-100 flex flex-col justify-center gap-2">
             <div className="flex items-center gap-2">
               <span className="w-7 h-7 rounded-lg bg-indigo-50 flex items-center justify-center shrink-0">
                 <Server size={14} className="text-[#5B5FF6]" />
               </span>
               <div className="text-[10px] uppercase font-bold text-[#98A2B3] tracking-wider">App Name</div>
             </div>
             <div className="text-sm font-black text-[#101828] pl-1 truncate w-full" title={repoName.replace(/_/g, ' ')}>{repoName.replace(/_/g, ' ')}</div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-[0_2px_10px_rgba(0,0,0,0.02)] hover:shadow-md hover:-translate-y-1 transition-all border border-slate-100 flex flex-col justify-center gap-2">
             <div className="flex items-center gap-2">
               <span className="w-7 h-7 rounded-lg bg-purple-50 flex items-center justify-center shrink-0">
                 <Box size={14} className="text-purple-600" />
               </span>
               <div className="text-[10px] uppercase font-bold text-[#98A2B3] tracking-wider">Packaging</div>
             </div>
             <div className="text-sm font-black text-[#101828] pl-1">{result.packagingType || 'jar'}</div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-[0_2px_10px_rgba(0,0,0,0.02)] hover:shadow-md hover:-translate-y-1 transition-all border border-slate-100 flex flex-col justify-center gap-2">
             <div className="flex items-center gap-2">
               <span className="w-7 h-7 rounded-lg bg-blue-50 flex items-center justify-center shrink-0">
                 <Layout size={14} className="text-blue-600" />
               </span>
               <div className="text-[10px] uppercase font-bold text-[#98A2B3] tracking-wider">Module Type</div>
             </div>
             <div className="text-sm font-black text-[#101828] pl-1">{result.isMultiModule ? 'Multi Module' : 'Single'}</div>
          </div>
        </div>
      </div>

      <div className="mb-10">
        <h2 className="text-lg font-bold text-[#101828] mb-4 flex items-center gap-2 tracking-tight">
          <Activity className="text-[#5B5FF6]" size={20} /> Business Workflow
        </h2>
        <div className="bg-gradient-to-br from-white to-slate-50 rounded-3xl p-8 shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 flex items-center justify-between overflow-x-auto custom-scrollbar relative">
          {/* Subtle background connecting line */}
          <div className="absolute left-10 right-10 top-1/2 h-0.5 bg-gradient-to-r from-transparent via-slate-200 to-transparent -translate-y-6 z-0 pointer-events-none hidden md:block"></div>
          
          {workflowSteps.slice(0, 6).map((step, idx) => {
             const style = stepStyles[idx % stepStyles.length];
             return (
               <React.Fragment key={idx}>
                 <div className="flex flex-col items-center min-w-[120px] shrink-0 relative z-10 group cursor-default hover:-translate-y-1 transition-transform">
                    <div className={`w-14 h-14 ${style.bg} ${style.text} rounded-2xl flex items-center justify-center mb-4 shadow-sm group-hover:shadow-md transition-all border border-white`}>
                      {style.icon}
                    </div>
                    <div className="text-[13px] font-bold text-[#101828] text-center">{step.title}</div>
                    <div className="text-[11px] text-[#667085] text-center px-2 truncate max-w-[140px] mt-1 font-medium" title={step.desc}>{step.desc}</div>
                 </div>
                 {idx < Math.min(workflowSteps.length, 6) - 1 && (
                   <ChevronRight size={24} className="text-[#D0D5DD] shrink-0 mx-2 relative z-10 hidden md:block" />
                 )}
               </React.Fragment>
             );
          })}
        </div>
      </div>

      <div className="flex items-center justify-between pb-10">
        <button 
          onClick={() => setActiveTab('connect')}
          className="px-6 py-3 bg-white text-slate-700 font-bold rounded-xl shadow-sm border border-slate-200 hover:bg-slate-50 hover:shadow transition-all"
        >
          Back
        </button>
        <button 
          onClick={() => setActiveTab('test-recommendation')}
          className="px-8 py-3 bg-gradient-to-r from-[#5B5FF6] to-[#7B61FF] text-white font-bold rounded-xl shadow-[0_4px_14px_rgba(91,95,246,0.4)] hover:shadow-[0_6px_20px_rgba(91,95,246,0.6)] hover:-translate-y-0.5 transition-all flex items-center gap-2"
        >
          Continue <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
}
