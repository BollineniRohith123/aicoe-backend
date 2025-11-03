import React, { useState, useEffect, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useWorkflowWebSocket } from "../hooks/useWorkflowWebSocket";
import AgentProgress from "../components/AgentProgress";
import AgentCommunication from "../components/AgentCommunication";
import { API_BASE_URL } from "../const";
import "./ProcessingView.css";

const ProcessingView = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [projectName, setProjectName] = useState("");
  const [workflowId, setWorkflowId] = useState(null);
  const [isRestoring, setIsRestoring] = useState(true);
  const [workflowStatus, setWorkflowStatus] = useState("idle"); // idle, running, completed, failed
  const [showStartButton, setShowStartButton] = useState(false);
  const hasStartedRef = useRef(false); // Track if workflow has been started

  // Use WebSocket hook for real-time updates
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
    restoreState,
  } = useWorkflowWebSocket();

  useEffect(() => {
    const initializeWorkflow = async () => {
      // Get project data from location state
      const { projectName: name, transcript } = location.state || {};

      if (!name || !transcript) {
        navigate("/input");
        return;
      }

      setProjectName(name);

      // Check if there's an existing workflow in localStorage
      const storedWorkflowId = localStorage.getItem(`workflow_${name}`);

      if (storedWorkflowId) {
        console.log("🔄 Found existing workflow ID:", storedWorkflowId);

        // Try to restore workflow state from backend
        try {
          const response = await fetch(
            `${API_BASE_URL}/api/workflow/${storedWorkflowId}/status`,
          );
          const workflowStatus = await response.json();

          if (
            workflowStatus.status === "running" ||
            workflowStatus.status === "completed"
          ) {
            console.log("✅ Restoring workflow state:", workflowStatus);

            // Restore state in WebSocket hook
            restoreState(workflowStatus);

            // Reconnect to WebSocket
            connect(storedWorkflowId, name, transcript, true); // true = reconnecting
            setWorkflowId(storedWorkflowId);
            setIsRestoring(false);
            return;
          } else {
            console.log("⚠️ Workflow not active, starting new workflow");
            localStorage.removeItem(`workflow_${name}`);
          }
        } catch (error) {
          console.error("❌ Error restoring workflow:", error);
          localStorage.removeItem(`workflow_${name}`);
        }
      }

      // No existing workflow - show start button
      console.log("ℹ️ No active workflow found. Waiting for user to start...");
      setShowStartButton(true);
      setWorkflowStatus("idle");
      setIsRestoring(false);
    };

    initializeWorkflow();

    // Cleanup on unmount
    return () => {
      disconnect();
    };
  }, [location, navigate, connect, disconnect, restoreState]);

  // Handle manual workflow start
  const handleStartWorkflow = () => {
    const { projectName: name, transcript } = location.state || {};

    if (!name || !transcript) {
      console.error("Missing project data");
      return;
    }

    // Generate workflow ID
    const wfId = `workflow_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;

    console.log("🚀 User started workflow with ID:", wfId);

    // Store workflow ID in localStorage
    localStorage.setItem(`workflow_${name}`, wfId);
    setWorkflowId(wfId);
    setShowStartButton(false);
    setWorkflowStatus("running");

    // Connect to WebSocket and start workflow
    connect(wfId, name, transcript, false); // false = new workflow
  };

  // Update workflow status based on connection state
  useEffect(() => {
    if (isConnected && !isComplete) {
      setWorkflowStatus("running");
    } else if (isComplete) {
      setWorkflowStatus("completed");
    } else if (error) {
      setWorkflowStatus("failed");
    }
  }, [isConnected, isComplete, error]);

  // Navigate to results when workflow completes
  useEffect(() => {
    if (isComplete && results) {
      // Store results for the results page
      sessionStorage.setItem("lastResult", JSON.stringify(results));

      // Clear workflow ID from localStorage since it's complete
      if (projectName) {
        localStorage.removeItem(`workflow_${projectName}`);
      }

      // Navigate after a short delay
      setTimeout(() => {
        navigate("/results");
      }, 2000);
    }
  }, [isComplete, results, navigate, projectName]);

  return (
    <div className="processing-view">
      {/* Header */}
      <header className="processing-header">
        <div className="container">
          <h1 className="processing-title">
            <span className="title-icon">🚀</span>
            Processing: {projectName}
          </h1>

          {/* Workflow Status Indicator */}
          <div className="workflow-status-container">
            <div className={`workflow-status status-${workflowStatus}`}>
              {workflowStatus === "idle" && "⏸️ Ready to Start"}
              {workflowStatus === "running" && "▶️ Workflow Running"}
              {workflowStatus === "completed" && "✅ Workflow Complete"}
              {workflowStatus === "failed" && "❌ Workflow Failed"}
            </div>
          </div>

          {/* Start Button (only shown when idle) */}
          {showStartButton && (
            <div className="start-button-container">
              <button
                className="start-workflow-button"
                onClick={handleStartWorkflow}
                disabled={workflowStatus === "running"}
              >
                🚀 Start Processing
              </button>
              <p className="start-button-hint">
                Click to begin the AI agent workflow
              </p>
            </div>
          )}

          <p className="processing-subtitle">
            {workflowStatus === "idle" && 'Click "Start Processing" to begin'}
            {workflowStatus === "running" &&
              "AI agents are working on your project..."}
            {workflowStatus === "completed" && "Processing complete!"}
            {workflowStatus === "failed" &&
              "An error occurred during processing"}
          </p>

          {/* Progress Stats (only shown when running or completed) */}
          {(workflowStatus === "running" || workflowStatus === "completed") && (
            <div className="progress-stats">
              <div className="stat-item">
                <span className="stat-label">Progress:</span>
                <span className="stat-value">{progressPercentage}%</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Elapsed:</span>
                <span className="stat-value">{elapsedTime}</span>
              </div>
              {!isComplete && (
                <div className="stat-item">
                  <span className="stat-label">Est. Remaining:</span>
                  <span className="stat-value">{estimatedTimeRemaining}</span>
                </div>
              )}
              <div className="stat-item">
                <span className="stat-label">Connection:</span>
                <span
                  className={`stat-value ${isConnected ? "connected" : "disconnected"}`}
                >
                  {isConnected ? "🟢 Connected" : "🔴 Disconnected"}
                </span>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="processing-main">
        <div className="container">
          {error && (
            <div className="error-banner">
              <span className="error-icon">⚠️</span>
              <p>{error}</p>
            </div>
          )}

          <div className="processing-grid">
            {/* Left Column - Agent Progress */}
            <div className="processing-column">
              <AgentProgress
                currentAgent={currentAgent}
                agentStatuses={agentStatuses}
              />
            </div>

            {/* Right Column - Communication & Folder Tree */}
            <div className="processing-column">
              <AgentCommunication messages={messages} />
              <ProjectFolderTree projectName={projectName} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ProcessingView;
