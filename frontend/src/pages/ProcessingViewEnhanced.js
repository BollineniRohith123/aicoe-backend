import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useWorkflowWebSocket } from '../hooks/useWorkflowWebSocket';
import AgentProgress from '../components/AgentProgress';
import AgentCommunication from '../components/AgentCommunication';
import ProjectFolderTree from '../components/ProjectFolderTree';
import { Button } from "@/components/ui/button";
import { Eye, Code, Download, Lock, Unlock, ChevronLeft, PlayCircle } from "lucide-react";
import './ProcessingView.css';
import './ProcessingViewEnhanced.css';

const ProcessingViewEnhanced = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [projectName, setProjectName] = useState('');
  const [workflowId, setWorkflowId] = useState(null);
  const [isRestoring, setIsRestoring] = useState(true);
  const [workflowStatus, setWorkflowStatus] = useState('idle');
  const [showStartButton, setShowStartButton] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [viewMode, setViewMode] = useState('preview');
  const hasStartedRef = useRef(false);

  const {
    connect,
    disconnect,
    isConnected,
    currentAgent,
    agentStatuses,
    messages,
    error,
    isComplete,
    results,
    elapsedTime,
    progressPercentage,
    estimatedTimeRemaining,
    restoreState
  } = useWorkflowWebSocket();

  useEffect(() => {
    const initializeWorkflow = async () => {
      const { projectName: name, transcript } = location.state || {};

      if (!name || !transcript) {
        navigate('/input');
        return;
      }

      setProjectName(name);

      const storedWorkflowId = localStorage.getItem(`workflow_${name}`);

      if (storedWorkflowId) {
        try {
          const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/workflow/${storedWorkflowId}/status`);
          const workflowStatus = await response.json();

          if (workflowStatus.status === 'running' || workflowStatus.status === 'completed') {
            restoreState(workflowStatus);
            connect(storedWorkflowId, name, transcript, true);
            setWorkflowId(storedWorkflowId);
            setIsRestoring(false);
            return;
          } else {
            localStorage.removeItem(`workflow_${name}`);
          }
        } catch (error) {
          console.error('Error restoring workflow:', error);
          localStorage.removeItem(`workflow_${name}`);
        }
      }

      setShowStartButton(true);
      setWorkflowStatus('idle');
      setIsRestoring(false);
    };

    initializeWorkflow();

    return () => {
      disconnect();
    };
  }, [location, navigate, connect, disconnect, restoreState]);

  const handleStartWorkflow = () => {
    const { projectName: name, transcript } = location.state || {};

    if (!name || !transcript) {
      console.error('Missing project data');
      return;
    }

    const wfId = `workflow_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;

    localStorage.setItem(`workflow_${name}`, wfId);
    setWorkflowId(wfId);
    setShowStartButton(false);
    setWorkflowStatus('running');

    connect(wfId, name, transcript, false);
  };

  useEffect(() => {
    if (isConnected && !isComplete) {
      setWorkflowStatus('running');
    } else if (isComplete) {
      setWorkflowStatus('completed');
    } else if (error) {
      setWorkflowStatus('failed');
    }
  }, [isConnected, isComplete, error]);

  // Build file structure from results
  const buildFileStructure = (data) => {
    if (!data || !data.results) return {};
    
    const structure = {};
    const res = data.results;

    if (res.prd) {
      structure['📄 PRD'] = {
        content: typeof res.prd === 'string' ? res.prd : JSON.stringify(res.prd, null, 2),
        type: 'html',
        path: 'prd/PRD_v1.html',
        name: 'PRD_v1.html'
      };
    }

    if (res.mockup && res.mockup.mockup_pages) {
      Object.entries(res.mockup.mockup_pages).forEach(([filename, content]) => {
        structure[`🎨 ${filename}`] = {
          content,
          type: 'html',
          path: `mockup/${filename}`,
          name: filename
        };
      });
    }

    if (res.commercial_proposal) {
      structure['💼 Proposal'] = {
        content: typeof res.commercial_proposal === 'string' ? res.commercial_proposal : JSON.stringify(res.commercial_proposal, null, 2),
        type: 'html',
        path: 'proposal/proposal_v1.html',
        name: 'proposal_v1.html'
      };
    }

    if (res.bom) {
      structure['📦 BOM'] = {
        content: typeof res.bom === 'string' ? res.bom : JSON.stringify(res.bom, null, 2),
        type: 'html',
        path: 'bom/bom_v1.html',
        name: 'bom_v1.html'
      };
    }

    if (res.architecture_diagram) {
      structure['🏗️ Architecture'] = {
        content: typeof res.architecture_diagram === 'string' ? res.architecture_diagram : JSON.stringify(res.architecture_diagram, null, 2),
        type: 'html',
        path: 'architecture/architecture_v1.html',
        name: 'architecture_v1.html'
      };
    }

    return structure;
  };

  const fileStructure = results ? buildFileStructure(results) : {};
  const fileList = Object.entries(fileStructure);

  // Auto-select first file when results become available
  useEffect(() => {
    if (isComplete && fileList.length > 0 && !selectedFile) {
      setSelectedFile(fileList[0][1]);
    }
  }, [isComplete, fileList.length]);

  const isPlaygroundLocked = workflowStatus === 'running' || workflowStatus === 'idle';

  return (
    <div className="processing-view-enhanced">
      {/* Header */}
      <header className="enhanced-header">
        <div className="header-content">
          <div className="header-left">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/')}
              className="gap-2"
            >
              <ChevronLeft className="w-4 h-4" />
              Home
            </Button>
            <div className="header-title-section">
              <h1 className="header-title">
                <span className="title-icon">🚀</span>
                {projectName}
              </h1>
              <div className={`workflow-status-badge status-${workflowStatus}`}>
                {workflowStatus === 'idle' && '⏸️ Ready'}
                {workflowStatus === 'running' && '▶️ Processing'}
                {workflowStatus === 'completed' && '✅ Complete'}
                {workflowStatus === 'failed' && '❌ Failed'}
              </div>
            </div>
          </div>
          
          {(workflowStatus === 'running' || workflowStatus === 'completed') && (
            <div className="header-stats">
              <div className="stat-badge">
                <span className="stat-label">Progress</span>
                <span className="stat-value">{progressPercentage}%</span>
              </div>
              <div className="stat-badge">
                <span className="stat-label">Time</span>
                <span className="stat-value">{elapsedTime}</span>
              </div>
              {!isComplete && (
                <div className="stat-badge">
                  <span className="stat-label">Remaining</span>
                  <span className="stat-value">{estimatedTimeRemaining}</span>
                </div>
              )}
            </div>
          )}
        </div>
      </header>

      {/* Start Button Overlay */}
      {showStartButton && (
        <div className="start-overlay">
          <div className="start-card">
            <div className="start-icon">🚀</div>
            <h2 className="start-title">Ready to Process</h2>
            <p className="start-description">
              Click below to start the AI agent workflow for <strong>{projectName}</strong>
            </p>
            <button
              className="start-button"
              onClick={handleStartWorkflow}
            >
              Start Processing
            </button>
          </div>
        </div>
      )}

      {/* Main Content - Split View */}
      <div className="enhanced-main">
        {/* Left Side - Agent Progress */}
        <div className="left-panel">
          <div className="panel-content">
            <AgentProgress
              currentAgent={currentAgent}
              agentStatuses={agentStatuses}
            />
            <AgentCommunication messages={messages} />
          </div>
        </div>

        {/* Right Side - Playground */}
        <div className="right-panel">
          <div className={`playground-container ${isPlaygroundLocked ? 'locked' : 'unlocked'}`}>
            {/* Playground Header */}
            <div className="playground-header">
              <div className="playground-title-section">
                <h3 className="playground-title">
                  {isPlaygroundLocked ? <Lock className="w-5 h-5" /> : <Unlock className="w-5 h-5" />}
                  Results Playground
                </h3>
                <span className="playground-status">
                  {isPlaygroundLocked ? 'Locked - Processing in progress' : 'Unlocked - Ready to explore'}
                </span>
              </div>
              
              {!isPlaygroundLocked && selectedFile && (
                <div className="playground-controls">
                  <Button
                    size="sm"
                    variant={viewMode === 'preview' ? 'default' : 'outline'}
                    onClick={() => setViewMode('preview')}
                  >
                    <Eye className="w-4 h-4 mr-2" />
                    Preview
                  </Button>
                  <Button
                    size="sm"
                    variant={viewMode === 'code' ? 'default' : 'outline'}
                    onClick={() => setViewMode('code')}
                  >
                    <Code className="w-4 h-4 mr-2" />
                    Code
                  </Button>
                </div>
              )}
            </div>

            {/* Playground Content */}
            <div className="playground-content">
              {isPlaygroundLocked ? (
                <div className="playground-locked-state">
                  <Lock className="locked-icon" />
                  <h4 className="locked-title">Playground Locked</h4>
                  <p className="locked-description">
                    The playground will unlock automatically when the workflow completes.
                    You can watch the agent progress in real-time on the left.
                  </p>
                  <div className="locked-progress">
                    <div className="locked-progress-bar">
                      <div 
                        className="locked-progress-fill" 
                        style={{ width: `${progressPercentage}%` }}
                      />
                    </div>
                    <span className="locked-progress-text">{progressPercentage}% Complete</span>
                  </div>
                </div>
              ) : fileList.length === 0 ? (
                <div className="playground-empty-state">
                  <PlayCircle className="empty-icon" />
                  <h4 className="empty-title">No Results Yet</h4>
                  <p className="empty-description">
                    Results will appear here once the workflow completes.
                  </p>
                </div>
              ) : (
                <>
                  {/* File Selector */}
                  <div className="file-selector">
                    {fileList.map(([name, file]) => (
                      <button
                        key={file.path}
                        className={`file-tab ${selectedFile?.path === file.path ? 'active' : ''}`}
                        onClick={() => setSelectedFile(file)}
                      >
                        {name}
                      </button>
                    ))}
                  </div>

                  {/* File Preview */}
                  {selectedFile && (
                    <div className="file-preview">
                      {viewMode === 'preview' && selectedFile.type === 'html' ? (
                        <iframe
                          srcDoc={selectedFile.content}
                          className="preview-iframe"
                          title={selectedFile.name}
                          sandbox="allow-scripts allow-same-origin"
                        />
                      ) : (
                        <pre className="code-preview">
                          <code>{selectedFile.content}</code>
                        </pre>
                      )}
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProcessingViewEnhanced;

