import os

app_jsx_path = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\frontend\src\App.jsx"
dashboard_jsx_path = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\frontend\src\pages\Dashboard.jsx"

app_jsx_content = """import React, { useState, useEffect } from 'react';
import { 
  Home, RefreshCw, Box, Search, Play, FileText, CheckCircle, Clock, Database, Layers, ArrowRight,
  Shield, Code, Link, Cpu, BarChart, ExternalLink, Moon, Sun, 
  Settings as SettingsIcon, LogOut, Check, ChevronDown, Download, AlertCircle, X, CheckSquare, Sparkles, Server, Map, GitMerge, List, BookOpen, Key, Eye, Layout, File, Target, FlaskConical, HelpCircle, Bell 
} from 'lucide-react';
import { getStatus, getWorkflowStatus, getSession } from './api';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { motion } from 'framer-motion';

// Import Pages
import Dashboard from './pages/Dashboard';
import Discovery from './pages/Discovery';
import ProjectRunner from './pages/ProjectRunner';
import FunctionalTesting from './pages/FunctionalTesting';
import Settings from './pages/Settings';
import ChatbotWidget from './components/ChatbotWidget';
import Login from './pages/Login';
import AITestRecommendation from './pages/AITestRecommendation';
import Summary from './pages/Summary';

// Design Tokens for App
const T = {
  bg:        '#F7F8FC',
  card:      '#FFFFFF',
  primary:   '#5B5FF6',
  secondary: '#7B61FF',
  success:   '#12B76A',
  danger:    '#F04438',
  textPri:   '#101828',
  textSec:   '#667085',
  border:    '#EAECF0',
  radius:    '24px',
  shadow:    '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
};

const Card = ({ children, style, className = '', ...props }) => (
  <motion.div
    initial={{ opacity: 0, y: 16 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.4, ease: 'easeOut' }}
    style={{
      background: T.card,
      borderRadius: T.radius,
      boxShadow: T.shadow,
      border: `1px solid ${T.border}`,
      ...style,
    }}
    className={className}
    {...props}
  >
    {children}
  </motion.div>
);

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState('');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [darkMode, setDarkMode] = useState(true);

  const [sessionId, setSessionId] = useState(null);
  const [sessionData, setSessionData] = useState(null);

  // Repository Analysis Page states
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisRepoUrl, setAnalysisRepoUrl] = useState('');
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState(null);
  const [analysisStatusText, setAnalysisStatusText] = useState('');
  const [analysisElapsedTime, setAnalysisElapsedTime] = useState(0);
  const [analysisTimeTaken, setAnalysisTimeTaken] = useState(null);

  // Migration Center Page states
  const [migrationResult, setMigrationResult] = useState(null);
  const [migrationRepoUrl, setMigrationRepoUrl] = useState('');
  const [migrationTargetVersion, setMigrationTargetVersion] = useState('21');
  const [migrationLoading, setMigrationLoading] = useState(false);
  const [migrationError, setMigrationError] = useState(null);
  const [migrationStatusText, setMigrationStatusText] = useState('');
  const [migrationHistory, setMigrationHistory] = useState([]);
  const [migrationElapsedTime, setMigrationElapsedTime] = useState(0);
  const [migrationTimeTaken, setMigrationTimeTaken] = useState(null);

  // Ticking effect for migration loading timer
  useEffect(() => {
    let intervalId;
    if (migrationLoading) {
      const startTime = Date.now();
      setMigrationElapsedTime(0);
      intervalId = setInterval(() => {
        setMigrationElapsedTime(((Date.now() - startTime) / 1000).toFixed(1));
      }, 100);
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [migrationLoading]);


  // Auto sync migration details when analysis result updates
  useEffect(() => {
    if (analysisResult && analysisResult.repoUrl) {
      setAnalysisRepoUrl(analysisResult.repoUrl);
      setMigrationRepoUrl(analysisResult.repoUrl);
      if (analysisResult.migrationRecommendation) {
        if (analysisResult.migrationRecommendation.includes('21')) {
          setMigrationTargetVersion('21');
        } else if (analysisResult.migrationRecommendation.includes('17')) {
          setMigrationTargetVersion('17');
        }
      }
    }
  }, [analysisResult]);

  // KPI STATE for persistent cards
  const [status, setStatus] = useState({ ragInitialized: false, ragMessage: '', provider: '' });
  const [stats, setStats] = useState({ reposAnalyzed: 0, migrationsRun: 0, filesConverted: 0 });
  const [migrations, setMigrations] = useState([]);

  const [workflowState, setWorkflowState] = useState({ analysisCompleted: false, runnerCompleted: false });

  // Session Hydration
  useEffect(() => {
    if (!sessionId) return;
    getSession(sessionId).then(data => {
      if (data) {
        setSessionData(data);
        if (data.analysisResult) setAnalysisResult(data.analysisResult);
        if (data.repoUrl) {
          setAnalysisRepoUrl(data.repoUrl);
          setMigrationRepoUrl(data.repoUrl);
        }
        if (data.workflowState) {
          setWorkflowState(prev => ({
             ...prev, 
             analysisCompleted: data.workflowState.analysisCompleted || prev.analysisCompleted,
             runnerCompleted: data.workflowState.runnerCompleted || prev.runnerCompleted
          }));
        }
        if (data.migrationResult) setMigrationResult(data.migrationResult);
        if (data.stats) setStats(data.stats);
        if (data.migrations) setMigrations(data.migrations);
      }
    }).catch(console.error);
  }, [sessionId, activeTab]);

  useEffect(() => {
    const fetchStatus = () => {
      getStatus()
        .then(data => setStatus(data))
        .catch(() => setStatus({ ragInitialized: false, ragMessage: 'Disconnected', provider: '' }));
    };
    
    const fetchWorkflow = async () => {
      if (analysisRepoUrl) {
        const repoName = analysisRepoUrl.split('/').pop().replace('.git', '');
        try {
          const ws = await getWorkflowStatus(repoName);
          setWorkflowState(prev => ({
            ...prev,
            analysisCompleted: ws.analysisCompleted || prev.analysisCompleted,
            runnerCompleted: ws.runnerCompleted || prev.runnerCompleted
          }));
        } catch (e) {
          // Ignore
        }
      }
    };

    fetchStatus();
    fetchWorkflow();
    const interval = setInterval(() => {
      fetchStatus();
      fetchWorkflow();
    }, 5000);
    return () => clearInterval(interval);
  }, [analysisRepoUrl, activeTab]);

  // Wizard Nodes mapped for Sidebar
  const wizardNodes = [
    { id: 'dashboard', label: 'Connect Repository', shortLabel: 'Connect Repository' },
    { id: 'discovery', label: 'Project Discovery', shortLabel: 'Project Discovery' },
    { id: 'test-recommendation', label: 'Generate Test Cases', shortLabel: 'Generate Test Cases' },
    { id: 'execute-tests', label: 'Execute Tests', shortLabel: 'Execute Tests' },
    { id: 'results', label: 'Test Results', shortLabel: 'View Results' },
    { id: 'summary', label: 'Reports & Downloads', shortLabel: 'Download Reports' }
  ];

  const renderContent = () => {
    return (
      <>
        <div className={activeTab === 'dashboard' ? 'block h-full w-full' : 'hidden'}>
          <Dashboard 
            setActiveTab={setActiveTab} 
            setAnalysisRepoUrl={setAnalysisRepoUrl}
            setAnalysisResult={setAnalysisResult}
            sessionId={sessionId}
            setSessionId={setSessionId}
          />
        </div>
        <div className={activeTab === 'settings' ? 'block h-full w-full' : 'hidden'}>
          <Settings />
        </div>
        <div className={activeTab === 'discovery' ? 'block h-full w-full' : 'hidden'}>
          <Discovery
            setActiveTab={setActiveTab}
            repoUrl={analysisRepoUrl}
            setRepoUrl={setAnalysisRepoUrl}
            loading={analysisLoading}
            setLoading={setAnalysisLoading}
            result={analysisResult}
            setResult={setAnalysisResult}
            error={analysisError}
            setError={setAnalysisError}
            statusText={analysisStatusText}
            setStatusText={setAnalysisStatusText}
            elapsedTime={analysisElapsedTime}
            timeTaken={analysisTimeTaken}
            setTimeTaken={setAnalysisTimeTaken}
            workflowState={workflowState}
            setWorkflowState={setWorkflowState}
            sessionId={sessionId}
            setSessionId={setSessionId}
          />
        </div>
        <div className={activeTab === 'test-recommendation' ? 'block h-full w-full' : 'hidden'}>
          <AITestRecommendation
            setActiveTab={setActiveTab}
            repoUrl={migrationRepoUrl}
            workflowState={workflowState}
            setWorkflowState={setWorkflowState}
            analysisResult={analysisResult}
            sessionId={sessionId}
          />
        </div>
        <div className={(activeTab === 'results' || activeTab === 'testing' || activeTab === 'execute-tests') ? 'block h-full w-full' : 'hidden'}>
          <FunctionalTesting
            setActiveTab={setActiveTab}
            repoUrl={migrationRepoUrl}
            analysisResult={analysisResult}
            result={migrationResult}
            workflowState={workflowState}
            setWorkflowState={setWorkflowState}
            sessionId={sessionId}
          />
        </div>
        <div className={activeTab === 'summary' ? 'block h-full w-full' : 'hidden'}>
          <Summary repoUrl={analysisRepoUrl || migrationRepoUrl} sessionId={sessionId} />
        </div>
      </>
    );
  };

  if (!isLoggedIn) {
    return <Login onLogin={(user) => { setIsLoggedIn(true); setCurrentUser(user); }} />;
  }

  const currentIndex = wizardNodes.findIndex(n => n.id === activeTab);
  const currentStep = currentIndex >= 0 ? currentIndex + 1 : 0;
  const currentTitle = currentIndex >= 0 ? wizardNodes[currentIndex].label.toUpperCase() : 'SETTINGS';

  return (
    <div className="flex h-screen bg-[#F7F8FC] font-sans text-[#101828] overflow-hidden">
      
      {/* ── SIDEBAR ── */}
      <div className="w-[280px] bg-white border-r border-[#EAECF0] flex flex-col h-full z-20 flex-shrink-0">
        <div className="p-6 flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-[#5B5FF6] to-[#7B61FF] rounded-xl text-white shadow-soft">
            <Sparkles size={24} />
          </div>
          <div>
            <h1 className="font-extrabold text-xl text-[#101828] leading-tight tracking-tight">PROVA</h1>
            <p className="text-[10px] text-[#667085] uppercase tracking-wider font-semibold">AI Testing Platform</p>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-2">
          {wizardNodes.map((node, index) => {
            const isActive = activeTab === node.id;
            const isCompleted = index < currentIndex;
            
            let isLocked = false;
            let lockedReason = '';
            if ((node.id === 'test-recommendation' || node.id === 'results' || node.id === 'execute-tests') && !workflowState.analysisCompleted) {
              isLocked = true;
              lockedReason = 'Complete Repository Analysis first.';
            }

            return (
              <button
                key={node.id}
                onClick={() => {
                  if (isLocked) {
                    alert(lockedReason);
                    return;
                  }
                  setActiveTab(node.id);
                }}
                title={isLocked ? lockedReason : ''}
                className={`flex items-center gap-4 px-4 py-3 rounded-2xl transition-all text-left w-full
                  ${isLocked ? 'cursor-not-allowed opacity-60' : 'cursor-pointer hover:bg-[#F9FAFB]'}
                  ${isActive ? 'bg-[#F4F5FF] hover:bg-[#F4F5FF]' : ''}
                `}
              >
                <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-colors
                  ${isActive ? 'bg-[#5B5FF6] text-white' : (isCompleted ? 'bg-[#12B76A] text-white' : 'bg-[#F2F4F7] text-[#667085]')}
                `}>
                  {index + 1}
                </div>
                <span className={`text-sm font-semibold ${isActive ? 'text-[#5B5FF6]' : 'text-[#344054]'}`}>
                  {node.label}
                </span>
              </button>
            );
          })}
        </div>

        {/* Need Help Widget */}
        <div className="p-6 mt-auto">
          <div className="bg-[#F7F8FC] p-5 rounded-2xl border border-[#EAECF0]">
            <h4 className="text-sm font-bold text-[#101828] mb-1">Need Help?</h4>
            <p className="text-xs text-[#667085] mb-4 leading-relaxed">We're here to help you at every step.</p>
            <button className="w-full bg-white border border-[#EAECF0] hover:bg-gray-50 text-[#101828] text-sm font-bold py-2.5 px-4 rounded-xl shadow-sm transition-colors">
              Contact Support
            </button>
          </div>
        </div>
      </div>

      {/* ── MAIN CONTENT AREA ── */}
      <div className="flex flex-col flex-1 h-full overflow-hidden">
        
        {/* Top Header */}
        <header className="h-[80px] bg-[#F7F8FC] flex items-center justify-between px-8 flex-shrink-0 z-10">
          <div className="flex items-center gap-3">
            {currentStep > 0 && (
              <div className="w-8 h-8 rounded bg-[#5B5FF6] text-white flex items-center justify-center font-bold text-sm shadow-sm">
                {currentStep}
              </div>
            )}
            <h2 className="text-xl font-extrabold text-[#101828] uppercase tracking-wide">{currentTitle}</h2>
          </div>
          
          <div className="flex items-center gap-5">
            <button className="text-[#667085] hover:text-[#101828] transition-colors"><HelpCircle size={22} /></button>
            <button className="text-[#667085] hover:text-[#101828] transition-colors relative">
              <Bell size={22} />
              <span className="absolute top-0 right-0 w-2.5 h-2.5 bg-[#F04438] border-2 border-[#F7F8FC] rounded-full"></span>
            </button>
            
            <div className="h-8 w-px bg-[#D0D5DD] mx-2"></div>
            
            <div className="flex items-center gap-3 cursor-pointer">
              <div className="w-9 h-9 rounded-full bg-gradient-to-r from-[#A5B4FC] to-[#818CF8] flex items-center justify-center text-white font-bold text-sm shadow-sm uppercase">
                {currentUser ? currentUser.substring(0, 2) : 'A'}
              </div>
              <div className="hidden md:block">
                <p className="text-sm font-semibold text-[#101828] leading-tight capitalize">{currentUser || 'Admin'}</p>
                <p className="text-xs text-[#667085]">Administrator</p>
              </div>
              <ChevronDown size={16} className="text-[#667085]" />
            </div>
          </div>
        </header>

        {/* Dynamic Content */}
        <main className="flex-1 overflow-y-auto px-8 pb-8">
          <div className="max-w-6xl mx-auto h-full">
            {renderContent()}
          </div>
        </main>

      </div>
      <ChatbotWidget />
    </div>
  );
}
"""

dashboard_jsx_content = """import React, { useState } from 'react';
import { GitBranch, ShieldAlert, CheckCircle, AlertTriangle, ArrowRight, Server, Play, Code, Lock, Eye, Link as LinkIcon, Search, FileText, BarChart, Download, Check } from 'lucide-react';
import { validateRepository } from '../api';
import { motion } from 'framer-motion';

export default function Dashboard({ setActiveTab, setAnalysisRepoUrl, setAnalysisResult, sessionId, setSessionId }) {
  const [repoUrl, setRepoUrl] = useState('');
  const [patToken, setPatToken] = useState('');
  const [validationState, setValidationState] = useState('initial'); // 'initial' | 'loading' | 'success' | 'error' | 'requires_auth'
  const [validationMessage, setValidationMessage] = useState('');
  const [isValidated, setIsValidated] = useState(false);

  const handleValidate = async (e) => {
    if (e) e.preventDefault();
    if (isValidated) {
      handleContinue();
      return;
    }
    if (!repoUrl.trim()) return;

    setValidationState('loading');
    setValidationMessage('');
    setIsValidated(false);

    try {
      const data = await validateRepository(repoUrl, patToken || null);
      
      if (data.requiresPat && !patToken) {
        setValidationState('requires_auth');
        setValidationMessage('This repository is private or requires authentication. Please provide a PAT token to continue.');
      } else if (data.isValid) {
        setValidationState('success');
        setValidationMessage(data.message || 'Repository successfully validated.');
        setIsValidated(true);
      } else {
        setValidationState('error');
        setValidationMessage(data.message || 'Failed to validate repository.');
      }
    } catch (err) {
      setValidationState('error');
      setValidationMessage('Network error or unable to connect to validation service.');
    }
  };

  const handleUrlChange = (e) => {
    setRepoUrl(e.target.value);
    setValidationState('initial');
    setValidationMessage('');
    setPatToken('');
    setIsValidated(false);
  };

  const handleContinue = () => {
    if (isValidated) {
      if (setAnalysisRepoUrl) setAnalysisRepoUrl(repoUrl);
      if (setAnalysisResult) setAnalysisResult(null);
      if (setSessionId) setSessionId(null);
      setActiveTab('discovery');
    }
  };

  return (
    <div className="flex flex-col animate-fadeIn w-full py-4">
      
      {/* Hero Section */}
      <div className="flex justify-between items-center mb-10">
        <div className="max-w-2xl">
          <h1 className="text-[40px] font-extrabold text-[#101828] mb-4 leading-tight">AI Functional Testing Platform</h1>
          <p className="text-[17px] text-[#667085] leading-relaxed pr-8">
            Let PROVA analyze your application, generate smart test cases automatically and deliver professional test reports.
          </p>
        </div>
        <div className="hidden lg:block relative mr-8">
            <div className="w-40 h-40 bg-gradient-to-br from-[#5B5FF6] to-[#818CF8] rounded-3xl shadow-2xl flex items-center justify-center transform rotate-6">
                <Code className="text-white w-20 h-20" strokeWidth={1.5} />
            </div>
            <div className="absolute -bottom-4 -right-4 w-16 h-16 bg-white rounded-full shadow-lg flex items-center justify-center">
                <svg className="w-9 h-9 text-[#101828]" viewBox="0 0 24 24" fill="currentColor">
                    <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.416 22 12c0-5.523-4.477-10-10-10z" />
                </svg>
            </div>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: 'easeOut' }}
        className="bg-white rounded-[24px] p-8 shadow-sm border border-[#EAECF0] mb-8"
      >
        <h2 className="text-xl font-bold text-[#101828] mb-2">Connect Your GitHub Repository</h2>
        <p className="text-sm text-[#667085] mb-6">
          Start by connecting your repository. PROVA will analyze your project and understand the codebase.
        </p>
        
        <form onSubmit={handleValidate} className="space-y-6">
          <div className="relative flex items-center">
            <div className="absolute left-5 text-[#98A2B3]">
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                 <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.416 22 12c0-5.523-4.477-10-10-10z" />
              </svg>
            </div>
            <input
              type="url"
              value={repoUrl}
              onChange={handleUrlChange}
              placeholder="https://github.com/username/repository"
              required
              disabled={validationState === 'loading'}
              className="w-full pl-14 pr-48 py-4 rounded-xl border border-[#EAECF0] bg-white focus:ring-2 focus:ring-[#5B5FF6] focus:border-[#5B5FF6] outline-none transition-all text-sm font-medium shadow-[inset_0_2px_4px_rgba(0,0,0,0.02)]"
            />
            
            {validationState !== 'requires_auth' && (
              <div className="absolute right-2">
                <button
                  type="submit"
                  disabled={!repoUrl.trim() || validationState === 'loading'}
                  className="bg-[#5B5FF6] hover:bg-[#4F51E5] text-white px-6 py-2.5 rounded-lg font-bold text-sm transition-colors disabled:opacity-70 flex items-center gap-2 shadow-sm"
                >
                  {validationState === 'loading' ? 'Connecting...' : (isValidated ? 'Continue' : 'Connect Repository')}
                  {isValidated && <ArrowRight size={16} />}
                </button>
              </div>
            )}
          </div>
          
          {validationState === 'requires_auth' && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="pt-2"
            >
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-4 flex items-start gap-3">
                <AlertTriangle className="text-amber-500 flex-shrink-0 mt-0.5" size={18} />
                <div>
                  <h4 className="text-sm font-bold text-amber-800">Authentication Required</h4>
                  <p className="text-xs text-amber-700 mt-1">{validationMessage}</p>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-3">
                <input
                  type="password"
                  value={patToken}
                  onChange={(e) => setPatToken(e.target.value)}
                  placeholder="Personal Access Token (ghp_...)"
                  required
                  className="flex-1 px-4 py-3 rounded-xl border border-[#EAECF0] bg-[#F7F8FC] focus:ring-2 focus:ring-[#5B5FF6] focus:outline-none transition-all font-mono text-sm"
                />
                <button
                  type="submit"
                  disabled={!patToken.trim() || validationState === 'loading'}
                  className="bg-[#5B5FF6] hover:bg-[#4F51E5] text-white px-6 py-3 rounded-xl font-bold text-sm transition-colors disabled:opacity-70"
                >
                  {validationState === 'loading' ? 'Validating...' : 'Validate Token'}
                </button>
              </div>
            </motion.div>
          )}

          {validationState === 'error' && (
            <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 flex items-start gap-3 mt-4">
              <ShieldAlert className="text-rose-500 flex-shrink-0 mt-0.5" size={18} />
              <p className="text-sm font-medium text-rose-700">{validationMessage}</p>
            </div>
          )}

          {validationState === 'success' && (
            <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 flex items-center gap-3 mt-4">
              <CheckCircle className="text-emerald-500 flex-shrink-0" size={20} />
              <p className="text-sm font-bold text-emerald-800">{validationMessage}</p>
            </div>
          )}
          
          <div className="flex flex-wrap items-center gap-4 pt-2">
            <div className="flex items-center gap-2 bg-[#F9FAFB] px-4 py-2 rounded-full border border-[#EAECF0]">
               <div className="w-5 h-5 rounded-full bg-[#ECFDF3] flex items-center justify-center">
                  <ShieldAlert size={12} className="text-[#12B76A]" />
               </div>
               <span className="text-xs font-bold text-[#344054]">Public & Private Repositories</span>
            </div>
            <div className="flex items-center gap-2 bg-[#F9FAFB] px-4 py-2 rounded-full border border-[#EAECF0]">
               <div className="w-5 h-5 rounded-full bg-[#EFF8FF] flex items-center justify-center">
                  <Lock size={12} className="text-[#2E90FA]" />
               </div>
               <span className="text-xs font-bold text-[#344054]">Secure Connection</span>
            </div>
            <div className="flex items-center gap-2 bg-[#F9FAFB] px-4 py-2 rounded-full border border-[#EAECF0]">
               <div className="w-5 h-5 rounded-full bg-[#FFFAEB] flex items-center justify-center">
                  <Eye size={12} className="text-[#F79009]" />
               </div>
               <span className="text-xs font-bold text-[#344054]">Read-Only Access</span>
            </div>
          </div>
        </form>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: 'easeOut', delay: 0.1 }}
        className="bg-white rounded-[24px] p-8 shadow-sm border border-[#EAECF0]"
      >
        <h3 className="text-lg font-bold text-[#101828] mb-12">How PROVA Works (Step-by-Step)</h3>
        
        <div className="flex justify-between items-start relative px-4 max-w-5xl mx-auto">
          <div className="absolute top-7 left-16 right-16 h-[2px] bg-[#F2F4F7] z-0"></div>
          
          {[
            { step: 1, icon: <LinkIcon />, title: "Connect\\nRepository", desc: "Link your GitHub\\nrepository", color: "text-[#5B5FF6]", bg: "bg-[#F4F5FF]", numberColor: "bg-[#5B5FF6]" },
            { step: 2, icon: <Search />, title: "Project\\nDiscovery", desc: "AI analyzes your\\nproject", color: "text-[#0284C7]", bg: "bg-[#F0F9FF]", numberColor: "bg-[#0284C7]" },
            { step: 3, icon: <FileText />, title: "Generate\\nTest Cases", desc: "Create UI & API\\ntest cases", color: "text-[#F59E0B]", bg: "bg-[#FEF3C7]", numberColor: "bg-[#F59E0B]" },
            { step: 4, icon: <Play />, title: "Execute\\nTests", desc: "Run tests in live\\nenvironment", color: "text-[#10B981]", bg: "bg-[#D1FAE5]", numberColor: "bg-[#10B981]" },
            { step: 5, icon: <BarChart />, title: "View\\nResults", desc: "Get pass/fail status\\n& analytics", color: "text-[#EF4444]", bg: "bg-[#FEE2E2]", numberColor: "bg-[#EF4444]" },
            { step: 6, icon: <Download />, title: "Download\\nReports", desc: "Share professional\\nreports", color: "text-[#8B5CF6]", bg: "bg-[#EDE9FE]", numberColor: "bg-[#8B5CF6]" }
          ].map((item, i) => (
            <div key={i} className="flex flex-col items-center text-center max-w-[140px] z-10">
              <div className="relative mb-5 group cursor-default">
                 <div className={`absolute -top-2.5 -right-2.5 w-6 h-6 rounded-full ${item.numberColor} text-white flex items-center justify-center text-[11px] font-bold z-20 shadow-sm border-2 border-white`}>
                   {item.step}
                 </div>
                 <div className={`w-14 h-14 rounded-full ${item.bg} flex items-center justify-center shadow-[0_2px_8px_rgba(0,0,0,0.04)]`}>
                   {React.cloneElement(item.icon, { className: item.color, size: 24, strokeWidth: 2 })}
                 </div>
                 
                 {i < 5 && (
                   <div className="absolute top-7 left-full w-full h-[2px] -translate-y-1/2 flex items-center justify-center pointer-events-none z-10 pl-4 pr-2 opacity-60">
                     <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#D0D5DD" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                       <path d="M5 12h14M12 5l7 7-7 7"/>
                     </svg>
                   </div>
                 )}
              </div>
              <h4 className="text-[13px] font-extrabold text-[#101828] leading-tight mb-2 whitespace-pre-line">{item.title}</h4>
              <p className="text-[11px] font-medium text-[#667085] leading-snug whitespace-pre-line">{item.desc}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
"""

with open(app_jsx_path, "w", encoding="utf-8") as f:
    f.write(app_jsx_content)

with open(dashboard_jsx_path, "w", encoding="utf-8") as f:
    f.write(dashboard_jsx_content)

print("Files updated successfully.")
