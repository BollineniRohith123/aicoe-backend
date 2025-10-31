import React, { useEffect, useRef } from 'react';
import './AgentCommunication.css';

const AgentCommunication = ({ messages = [] }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getAgentIcon = (agentName) => {
    const icons = {
      'StorageAgent': '📁',
      'TranscriptAgent': '📝',
      'RequirementsAgent': '📋',
      'KnowledgeBaseAgent': '🧠',
      'PRDAgent': '📄',
      'MockupAgent': '🎨',
      'SyntheticDataAgent': '💾',
      'ReviewerAgent': '✅',
      'Orchestrator': '🎯'
    };
    return icons[agentName] || '🤖';
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    });
  };

  return (
    <div className="agent-communication-container">
      <h2 className="communication-title">
        <span className="title-icon">💬</span>
        Agent Communication Log
      </h2>
      
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="no-messages">
            <span className="no-messages-icon">📭</span>
            <p>No agent communications yet. Start a workflow to see real-time messages.</p>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <div key={index} className="message-item">
                <div className="message-header">
                  <div className="message-agent">
                    <span className="message-icon">{getAgentIcon(message.from)}</span>
                    <span className="message-from">{message.from}</span>
                    {message.to && (
                      <>
                        <span className="message-arrow">→</span>
                        <span className="message-icon">{getAgentIcon(message.to)}</span>
                        <span className="message-to">{message.to}</span>
                      </>
                    )}
                  </div>
                  <span className="message-timestamp">
                    {formatTimestamp(message.timestamp)}
                  </span>
                </div>
                
                <div className="message-content">
                  {message.content}
                </div>
                
                {message.type && (
                  <div className={`message-type message-type-${message.type}`}>
                    {message.type}
                  </div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>
    </div>
  );
};

export default AgentCommunication;

