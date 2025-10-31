# AICOE Platform - Infinite Loop Fix Summary

## Problem Identified

The AICOE platform was experiencing an infinite reconnection loop where the WebSocket connection would continuously reconnect without starting the workflow. After thorough investigation, TWO root causes were identified:

### Root Cause #1: Incorrect Reconnection Detection (Frontend)
**Frontend sending "reconnect" on first connection instead of "start"**

1. The `reconnectAttemptsRef.current` counter was not being reset for new workflows
2. When a new workflow started, the counter might still be > 0 from a previous workflow
3. This caused the frontend to think it was reconnecting when it was actually a new workflow
4. Frontend sent "reconnect" instead of "start" on the first connection
5. Backend responded with "reconnect_ack" but no workflow was started
6. Connection closed, frontend reconnected, sent "reconnect" again
7. **Infinite reconnection loop with no workflow execution**

### Root Cause #2: Premature Counter Reset (Frontend)
**Reconnection counter reset too early, causing inconsistent behavior**

1. After successful reconnection, the counter was reset to 0 immediately
2. If the connection dropped again, the counter would be 1
3. But the workflow_id was the same, so it should still be a reconnection
4. This caused confusion between "new workflow" and "reconnection"
5. Led to sending wrong action type ("start" vs "reconnect")

## Fixes Implemented

### 1. Backend Server Fixes (`backend/server.py`)

#### Added Workflow State Tracking
- Added `active_workflows = {}` dictionary (line 50) to track running workflows
- Stores workflow status, project name, start time, end time, and errors

#### Modified WebSocket Endpoint
- **Reconnection Handler**: Added "reconnect" action handler that:
  - Checks if workflow is still running
  - Sends reconnection acknowledgment without restarting workflow
  - Allows client to receive progress updates from existing workflow

- **Duplicate Execution Prevention**: Modified "start" action handler to:
  - Check if workflow_id already exists in `active_workflows`
  - If status is "running", reject the duplicate start request
  - Return error message to client

- **Workflow State Management**:
  - Set workflow status to "running" when starting (line 249-253)
  - Update status to "completed" when workflow finishes successfully (lines 271-274)
  - Update status to "failed" on errors (lines 399-402, 425-428)

#### Added Workflow Status API Endpoint
- New endpoint: `GET /workflow/{workflow_id}/status`
- Returns current workflow status, project name, start/end times, and errors
- Checks both in-memory `active_workflows` and database for completed workflows

### 2. Frontend Fixes (`frontend/src/hooks/useWorkflowWebSocket.js`)

#### Fixed Reconnection Detection Logic (Lines 77-92)
- **Proper Detection of New Workflow vs Reconnection**:
  - Check if `workflow_id` matches previous workflow to determine reconnection
  - Reset `reconnectAttemptsRef.current = 0` for NEW workflows
  - Only consider it a reconnection if counter > 0 AND workflow_id matches
  - This ensures "start" is sent on first connection, "reconnect" on subsequent

#### Removed Premature Counter Reset (Line 124)
- **Don't Reset Counter After Reconnection**:
  - Removed `reconnectAttemptsRef.current = 0` after successful reconnection
  - Counter should only reset when workflow completes or fails
  - This ensures subsequent disconnections continue sending "reconnect"

#### Added Counter Reset on Workflow Completion (Lines 253, 268)
- **Reset Counter When Workflow Ends**:
  - Reset `reconnectAttemptsRef.current = 0` in `handleComplete()`
  - Reset `reconnectAttemptsRef.current = 0` in `handleError()`
  - Prepares for next workflow to start fresh with counter at 0

#### Reconnect Message Handler
- **Added handling for "reconnect_ack" message type**:
  - Displays reconnection status to user
  - Continues receiving progress updates from existing workflow

### 3. Orchestrator Safeguards (`backend/agents/orchestrator.py`)

#### Duplicate Execution Prevention
- Added `active_executions` set to track currently executing workflow IDs
- Check if workflow is already executing before starting (lines 106-115)
- Return error if duplicate execution detected
- Remove workflow from active executions when completed or failed (lines 270-271, 290-291)

#### Maximum Workflow Execution Time
- Added `max_workflow_time` parameter (default: 3600 seconds = 1 hour)
- Track workflow start time
- Check elapsed time before each agent execution (lines 143-148)
- Raise `TimeoutError` if workflow exceeds maximum time

#### Per-Agent Timeout
- Wrap each agent execution in `asyncio.wait_for()` with 600-second timeout (10 minutes)
- Catch `asyncio.TimeoutError` and return failure result
- Prevents individual agents from hanging indefinitely (lines 151-165)

#### Enhanced Logging
- Log workflow start with active execution count
- Log workflow completion/failure with updated active execution count
- Helps track and debug workflow execution issues

## Workflow Execution Flow (After Fixes)

### Initial Connection
1. User starts workflow → Frontend connects to WebSocket
2. Frontend sends `{"action": "start", "project_name": "...", "transcript": "..."}`
3. Backend checks if workflow is already running
4. If not running, backend marks workflow as "running" in `active_workflows`
5. Backend starts workflow execution with orchestrator
6. Orchestrator checks if workflow_id is in `active_executions`
7. If not, adds to `active_executions` and proceeds
8. Workflow executes with timeout safeguards

### Reconnection Scenario
1. WebSocket connection drops during workflow execution
2. Frontend detects disconnection and attempts reconnection
3. Frontend sends `{"action": "reconnect", "workflow_id": "..."}`
4. Backend checks `active_workflows` for workflow status
5. Backend sends `{"type": "reconnect_ack", "status": "running", ...}`
6. Frontend continues receiving progress updates from existing workflow
7. **No duplicate workflow execution occurs**

### Workflow Completion
1. All agents complete successfully
2. Orchestrator removes workflow from `active_executions`
3. Backend updates workflow status to "completed" in `active_workflows`
4. Results sent to frontend
5. Workflow data stored in database

### Timeout Scenarios
1. **Workflow Timeout**: If workflow exceeds 1 hour, `TimeoutError` raised
2. **Agent Timeout**: If individual agent exceeds 10 minutes, agent marked as failed
3. Both cases update workflow status to "failed" and clean up active executions

## Safeguards Summary

| Level | Safeguard | Implementation |
|-------|-----------|----------------|
| **Server** | Duplicate execution prevention | Check `active_workflows` before starting |
| **Server** | Reconnection handling | "reconnect" action handler |
| **Server** | Workflow state tracking | `active_workflows` dictionary |
| **Frontend** | Smart reconnection | Send "reconnect" instead of "start" |
| **Orchestrator** | Duplicate execution prevention | `active_executions` set |
| **Orchestrator** | Maximum workflow time | 1-hour timeout with elapsed time checking |
| **Orchestrator** | Per-agent timeout | 10-minute timeout per agent |
| **Orchestrator** | Cleanup on completion/failure | Remove from `active_executions` |

## Testing Recommendations

1. **Normal Workflow Execution**:
   - Start a workflow and verify it completes successfully
   - Check that workflow is tracked in `active_workflows`
   - Verify workflow is removed from tracking after completion

2. **Reconnection Testing**:
   - Start a workflow
   - Manually disconnect WebSocket during execution
   - Verify frontend reconnects and sends "reconnect" message
   - Verify no duplicate workflow execution occurs
   - Verify progress updates continue after reconnection

3. **Duplicate Start Prevention**:
   - Start a workflow
   - Attempt to start the same workflow again (same workflow_id)
   - Verify second start request is rejected with error message

4. **Timeout Testing**:
   - Test workflow timeout by creating a workflow that exceeds 1 hour
   - Test agent timeout by creating an agent that hangs for >10 minutes
   - Verify proper error handling and cleanup

5. **Status API Testing**:
   - Query `/workflow/{workflow_id}/status` during execution
   - Verify status is "running"
   - Query after completion, verify status is "completed"

## Files Modified

1. `backend/server.py` - WebSocket endpoint and workflow state management
2. `frontend/src/hooks/useWorkflowWebSocket.js` - Reconnection logic
3. `backend/agents/orchestrator.py` - Timeout safeguards and duplicate prevention

## Conclusion

The infinite loop issue has been comprehensively addressed through multiple layers of safeguards:
- **Prevention**: Duplicate execution checks at both server and orchestrator levels
- **Recovery**: Smart reconnection handling that doesn't restart workflows
- **Safety**: Timeout mechanisms to prevent indefinite execution
- **Visibility**: State tracking and status API for monitoring

These fixes ensure that workflows execute exactly once, can recover from connection issues, and have proper timeout safeguards to prevent infinite loops.

