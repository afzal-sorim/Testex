import React, { useState, useEffect } from 'react';
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
import TestResults from './pages/TestResults';
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
        <div className={(activeTab === 'testing' || activeTab === 'execute-tests') ? 'block h-full w-full' : 'hidden'}>
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
        <div className={activeTab === 'results' ? 'block h-full w-full' : 'hidden'}>
          <TestResults repoUrl={migrationRepoUrl} analysisResult={analysisResult} />
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
        <header className="h-[60px] bg-[#F7F8FC] flex items-center justify-end px-6 flex-shrink-0 z-10">

          
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
          <div className="w-full h-full">
            {renderContent()}
          </div>
        </main>

      </div>
      <ChatbotWidget />
    </div>
  );
}
