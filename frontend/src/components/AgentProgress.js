import React from 'react';
import './AgentProgress.css';

const AGENTS = [
  {
    id: 'storage',
    name: 'Storage Agent',
    icon: '📁',
    description: 'Creating project structure'
  },
  {
    id: 'transcript',
    name: 'Transcript Agent',
    icon: '📝',
    description: 'Extracting structured notes'
  },
  {
    id: 'researcher',
    name: 'Researcher Agent',
    icon: '🔍',
    description: 'Gathering industry insights'
  },
  {
    id: 'requirements',
    name: 'Requirements Agent',
    icon: '📋',
    description: 'Generating use cases'
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
    description: 'Assembling PRD document'
  },
  {
    id: 'mockup',
    name: 'Mockup Agent',
    icon: '🎨',
    description: 'Creating HTML mockups'
  },
  {
    id: 'synthetic_data',
    name: 'Synthetic Data Agent',
    icon: '💾',
    description: 'Generating demo data'
  },
  {
    id: 'commercial_proposal',
    name: 'Commercial Proposal Agent',
    icon: '💼',
    description: 'Creating business proposal'
  },
  {
    id: 'bom',
    name: 'BOM Agent',
    icon: '📊',
    description: 'Generating Bill of Materials'
  },
  {
    id: 'architecture_diagram',
    name: 'Architecture Diagram Agent',
    icon: '🏗️',
    description: 'Creating system diagrams'
  },
  {
    id: 'reviewer',
    name: 'Reviewer Agent',
    icon: '✅',
    description: 'Reviewing deliverables'
  }
];

const AgentProgress = ({ currentAgent, agentStatuses = {} }) => {
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

  return (
    <div className="agent-progress-container">
      <h2 className="agent-progress-title">
        <span className="title-icon">🤖</span>
        Multi-Agent Workflow Progress
      </h2>
      
      <div className="agent-timeline">
        {AGENTS.map((agent, index) => {
          const status = getAgentStatus(agent.id);
          const message = getAgentMessage(agent.id);
          
          return (
            <div key={agent.id} className={`agent-card agent-${status}`}>
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
                    <span className="status-text status-completed">Completed</span>
                  )}
                  {status === 'processing' && (
                    <span className="status-text status-processing">Processing...</span>
                  )}
                  {status === 'pending' && (
                    <span className="status-text status-pending">Pending</span>
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

