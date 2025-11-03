import React, { useEffect, useState } from 'react';
import './AgentProgress.css';

const AGENTS = [
  {
    id: 'storage',
    name: 'Storage Agent',
    icon: '📁',
    description: 'Creating project structure'
  },
  {
    id: 'intake',
    name: 'Intake Agent',
    icon: '📝',
    description: 'Processing meeting transcripts'
  },
  {
    id: 'researcher',
    name: 'Researcher Agent',
    icon: '🔍',
    description: 'Gathering industry insights'
  },
  {
    id: 'blueprint',
    name: 'Blueprint Agent',
    icon: '📋',
    description: 'Generating use cases & requirements'
  },
  {
    id: 'data',
    name: 'Data Agent',
    icon: '💾',
    description: 'Creating synthetic demo data'
  },
  {
    id: 'knowledge_base',
    name: 'Knowledge Base Agent',
    icon: '🧠',
    description: 'Enriching with domain knowledge'
  },
  {
    id: 'prd',
    name: 'PRD Agent',
    icon: '📄',
    description: 'Assembling Product Requirements Document'
  },
  {
    id: 'architecture',
    name: 'Architecture Agent',
    icon: '🏗️',
    description: 'Designing system architecture'
  },
  {
    id: 'bom',
    name: 'BOM Agent',
    icon: '📊',
    description: 'Generating Bill of Materials'
  },
  {
    id: 'proposal',
    name: 'Proposal Agent',
    icon: '💼',
    description: 'Creating commercial proposal'
  },
  {
    id: 'mockup',
    name: 'Mockup Agent',
    icon: '🎨',
    description: 'Building interactive HTML prototypes'
  },
  {
    id: 'reviewer',
    name: 'Reviewer Agent',
    icon: '✅',
    description: 'Quality assurance & validation'
  }
];

const AgentProgress = ({ currentAgent, agentStatuses = {} }) => {
  const [completedAgents, setCompletedAgents] = useState(new Set());

  const getAgentStatus = (agentId) => {
    const status = agentStatuses[agentId];
    if (!status) {
      return 'pending';
    }

    // Map backend status to frontend status
    if (status.status === 'completed') {
      return 'completed';
    } else if (status.status === 'running' || currentAgent === agentId) {
      return 'processing';
    } else if (status.status === 'failed') {
      return 'failed';
    } else {
      return 'pending';
    }
  };

  const getAgentMessage = (agentId) => {
    const status = agentStatuses[agentId];
    if (!status) {
      return 'Pending';
    }
    return status.message || status.status;
  };

  // Track newly completed agents for celebration effects
  useEffect(() => {
    Object.keys(agentStatuses).forEach(agentId => {
      if (agentStatuses[agentId].status === 'completed' && !completedAgents.has(agentId)) {
        setCompletedAgents(prev => new Set([...prev, agentId]));
        // Trigger celebration effect
        setTimeout(() => {
          const element = document.getElementById(`agent-${agentId}`);
          if (element) {
            element.classList.add('celebrate');
            setTimeout(() => element.classList.remove('celebrate'), 1000);
          }
        }, 100);
      }
    });
  }, [agentStatuses, completedAgents]);

  // Calculate overall progress
  const completedCount = Object.values(agentStatuses).filter(s => s.status === 'completed').length;
  const totalAgents = AGENTS.length;
  const overallProgress = Math.round((completedCount / totalAgents) * 100);

  return (
    <div className="agent-progress-container">
      <div className="agent-progress-header">
        <h2 className="agent-progress-title">
          <span className="title-icon">🤖</span>
          Multi-Agent Workflow Progress
        </h2>
        <div className="overall-progress-badge">
          <span className="progress-count">{completedCount}/{totalAgents}</span>
          <span className="progress-percentage">{overallProgress}%</span>
        </div>
      </div>

      <div className="agent-timeline">
        {AGENTS.map((agent, index) => {
          const status = getAgentStatus(agent.id);
          const message = getAgentMessage(agent.id);

          return (
            <div
              key={agent.id}
              id={`agent-${agent.id}`}
              className={`agent-card agent-${status}`}
              style={{animationDelay: `${index * 0.08}s`}}
            >
              <div className="agent-card-header">
                <div className="agent-icon-wrapper">
                  <span className="agent-icon">{agent.icon}</span>
                  {status === 'completed' && (
                    <span className="status-badge status-completed">✓</span>
                  )}
                  {status === 'processing' && (
                    <span className="status-badge status-processing">
                      <span className="spinner"></span>
                    </span>
                  )}
                  {status === 'failed' && (
                    <span className="status-badge status-failed">✕</span>
                  )}
                </div>
                
                <div className="agent-info">
                  <h3 className="agent-name">{agent.name}</h3>
                  <p className="agent-description">{agent.description}</p>
                  {message && (
                    <p className="agent-message">{message}</p>
                  )}
                </div>
                
                <div className="agent-status-indicator">
                  {status === 'completed' && (
                    <span className="status-text status-completed">
                      <span className="status-icon">✓</span>
                      <span className="status-label">Complete</span>
                    </span>
                  )}
                  {status === 'processing' && (
                    <span className="status-text status-processing">
                      <span className="status-icon">⚡</span>
                      <span className="status-label">Processing</span>
                    </span>
                  )}
                  {status === 'pending' && (
                    <span className="status-text status-pending">
                      <span className="status-icon">⏳</span>
                      <span className="status-label">Waiting</span>
                    </span>
                  )}
                  {status === 'failed' && (
                    <span className="status-text status-failed">
                      <span className="status-icon">❌</span>
                      <span className="status-label">Failed</span>
                    </span>
                  )}
                </div>
              </div>
              
              {status === 'processing' && (
                <div className="progress-bar">
                  <div className="progress-bar-fill"></div>
                </div>
              )}
              
              {index < AGENTS.length - 1 && (
                <div className={`agent-connector ${status === 'completed' ? 'connector-completed' : ''}`}></div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AgentProgress;

