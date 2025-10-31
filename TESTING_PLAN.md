# AICOE Platform - Infinite Loop Fix Testing Plan

## Overview
This document outlines the comprehensive testing plan to verify that the infinite loop issue has been resolved and that all safeguards are working correctly.

## Test Environment Setup

### Prerequisites
1. Backend server running on `http://localhost:8000`
2. Frontend application running on `http://localhost:3000`
3. MongoDB instance running and accessible
4. OpenRouter API key configured in `.env`

### Test Data
- **Project Name**: "Test Project - Loop Fix Verification"
- **Sample Transcript**: Use a short transcript (50-100 words) for quick testing
- **Long Transcript**: Use a longer transcript (500+ words) for timeout testing

## Test Cases

### 1. Normal Workflow Execution Test

**Objective**: Verify that a workflow executes successfully from start to finish without any loops.

**Steps**:
1. Start the backend server and frontend application
2. Navigate to the workflow creation page
3. Enter project name and transcript
4. Click "Start Workflow"
5. Observe the workflow progress in real-time

**Expected Results**:
- ✅ Workflow starts successfully
- ✅ All 12 agents execute in sequence: Storage → Transcript → Researcher → Requirements → Knowledge Base → PRD → Mockup → Synthetic Data → Commercial Proposal → BOM → Architecture Diagram → Reviewer
- ✅ Progress updates appear in real-time
- ✅ Workflow completes with status "success"
- ✅ Results are displayed correctly
- ✅ No duplicate agent executions
- ✅ Workflow is tracked in `active_workflows` during execution
- ✅ Workflow is removed from `active_workflows` after completion

**Verification**:
- Check backend logs for workflow start and completion messages
- Verify `active_executions` count increases and decreases correctly
- Check database for stored workflow results

---

### 2. WebSocket Reconnection Test

**Objective**: Verify that WebSocket reconnection does not trigger duplicate workflow execution.

**Steps**:
1. Start a workflow
2. Wait for 2-3 agents to complete (check progress updates)
3. Manually disconnect WebSocket (use browser DevTools → Network → WS → Close connection)
4. Wait for automatic reconnection (should happen within 5 seconds)
5. Observe workflow progress continues

**Expected Results**:
- ✅ WebSocket disconnects successfully
- ✅ Frontend detects disconnection and attempts reconnection
- ✅ Frontend sends `{"action": "reconnect", "workflow_id": "..."}` message
- ✅ Backend responds with `{"type": "reconnect_ack", "status": "running"}`
- ✅ Progress updates resume from where they left off
- ✅ **No duplicate workflow execution occurs**
- ✅ Workflow completes successfully with all agents executed exactly once
- ✅ "Connection restored successfully" message appears in UI

**Verification**:
- Check backend logs for "Client reconnecting to workflow" message
- Verify no "Starting workflow" message appears after reconnection
- Check `active_executions` count remains at 1 (not 2)
- Verify each agent executes exactly once (check agent output counts)

---

### 3. Duplicate Start Request Prevention Test

**Objective**: Verify that attempting to start the same workflow twice is prevented.

**Steps**:
1. Start a workflow
2. While workflow is running, attempt to start the same workflow again using the same workflow_id
   - Option A: Use browser DevTools → Network → WS → Send custom message: `{"action": "start", "project_name": "...", "transcript": "..."}`
   - Option B: Open a second browser tab and try to start the same workflow
3. Observe the response

**Expected Results**:
- ✅ First workflow starts successfully
- ✅ Second start request is rejected
- ✅ Error message received: "Workflow is already running. Please wait for it to complete."
- ✅ Only one workflow execution occurs
- ✅ First workflow continues and completes successfully

**Verification**:
- Check backend logs for "Workflow {workflow_id} is already running. Ignoring duplicate start request."
- Verify `active_workflows` contains only one entry for the workflow_id
- Verify `active_executions` count is 1 (not 2)

---

### 4. Workflow Timeout Test

**Objective**: Verify that workflows exceeding the maximum execution time (1 hour) are terminated.

**Steps**:
1. Modify `max_workflow_time` parameter in orchestrator to a shorter duration (e.g., 60 seconds) for testing
2. Create a workflow that will take longer than 60 seconds
   - Option A: Use a very long transcript
   - Option B: Temporarily add a `time.sleep(70)` in one of the agents
3. Start the workflow
4. Wait for timeout to occur

**Expected Results**:
- ✅ Workflow starts successfully
- ✅ After 60 seconds, workflow is terminated
- ✅ Error message: "Workflow exceeded maximum execution time of 60 seconds"
- ✅ Workflow status updated to "failed"
- ✅ Workflow removed from `active_executions`
- ✅ Error displayed in frontend

**Verification**:
- Check backend logs for timeout error message
- Verify workflow status in database is "failed"
- Verify `active_executions` is empty after timeout

**Cleanup**:
- Restore `max_workflow_time` to default value (3600 seconds)

---

### 5. Per-Agent Timeout Test

**Objective**: Verify that individual agents exceeding 10 minutes are terminated.

**Steps**:
1. Temporarily modify one agent (e.g., TranscriptAgent) to include a long delay:
   ```python
   async def execute(self, input_data, context):
       await asyncio.sleep(700)  # 11+ minutes
       # ... rest of code
   ```
2. Start a workflow
3. Wait for the modified agent to execute
4. Observe timeout behavior

**Expected Results**:
- ✅ Workflow starts successfully
- ✅ Agents before the modified agent complete successfully
- ✅ Modified agent times out after 10 minutes (600 seconds)
- ✅ Agent marked as failed with timeout error
- ✅ Workflow continues or fails based on error handling
- ✅ Timeout error logged

**Verification**:
- Check backend logs for "Agent {agent_name} exceeded maximum execution time of 600 seconds"
- Verify agent result contains timeout error
- Verify workflow handles agent failure appropriately

**Cleanup**:
- Remove the artificial delay from the agent

---

### 6. Workflow Status API Test

**Objective**: Verify that the workflow status API endpoint returns correct information.

**Steps**:
1. Start a workflow
2. While workflow is running, call: `GET /api/workflow/{workflow_id}/status`
3. Wait for workflow to complete
4. Call the status endpoint again
5. Try calling status for a non-existent workflow

**Expected Results**:

**During Execution**:
```json
{
  "workflow_id": "workflow_20250129_123456",
  "status": "running",
  "project_name": "Test Project",
  "start_time": "2025-01-29T12:34:56",
  "end_time": null,
  "error": null
}
```

**After Completion**:
```json
{
  "workflow_id": "workflow_20250129_123456",
  "status": "completed",
  "project_name": "Test Project",
  "start_time": "2025-01-29T12:34:56",
  "end_time": "2025-01-29T12:45:30",
  "error": null
}
```

**Non-existent Workflow**:
```json
{
  "detail": "Workflow not found"
}
```
Status Code: 404

**Verification**:
- Verify status changes from "running" to "completed"
- Verify timestamps are correct
- Verify 404 error for non-existent workflows

---

### 7. Multiple Concurrent Workflows Test

**Objective**: Verify that multiple different workflows can run concurrently without interference.

**Steps**:
1. Start Workflow A with project name "Project A"
2. Immediately start Workflow B with project name "Project B" (different workflow_id)
3. Observe both workflows execute concurrently
4. Wait for both to complete

**Expected Results**:
- ✅ Both workflows start successfully
- ✅ Both workflows execute concurrently
- ✅ `active_workflows` contains two entries
- ✅ `active_executions` count is 2
- ✅ Both workflows complete successfully
- ✅ No interference between workflows
- ✅ Results are stored separately for each workflow

**Verification**:
- Check backend logs for both workflow IDs
- Verify both workflows appear in `active_workflows` during execution
- Verify both workflows complete with correct results
- Check database for two separate workflow records

---

### 8. Reconnection After Workflow Completion Test

**Objective**: Verify behavior when reconnecting after workflow has already completed.

**Steps**:
1. Start a workflow and wait for it to complete
2. Disconnect WebSocket
3. Reconnect to the same workflow_id
4. Send reconnect message

**Expected Results**:
- ✅ Reconnection succeeds
- ✅ Backend responds with `{"type": "reconnect_ack", "status": "unknown", "message": "Workflow not found in active workflows. It may have completed."}`
- ✅ No workflow restart occurs
- ✅ Frontend displays appropriate message

**Verification**:
- Check backend logs for reconnection message
- Verify no new workflow execution starts
- Verify `active_executions` remains empty

---

## Performance Testing

### 9. Stress Test - Rapid Reconnections

**Objective**: Verify system stability under rapid reconnection scenarios.

**Steps**:
1. Start a workflow
2. Rapidly disconnect and reconnect WebSocket 10 times during execution
3. Observe workflow behavior

**Expected Results**:
- ✅ Workflow continues executing despite reconnections
- ✅ No duplicate executions occur
- ✅ Workflow completes successfully
- ✅ All agents execute exactly once

---

### 10. Load Test - Multiple Users

**Objective**: Verify system handles multiple users starting workflows simultaneously.

**Steps**:
1. Simulate 5-10 users starting different workflows simultaneously
2. Monitor system resources and workflow execution
3. Verify all workflows complete successfully

**Expected Results**:
- ✅ All workflows start successfully
- ✅ All workflows execute concurrently
- ✅ All workflows complete successfully
- ✅ No interference between workflows
- ✅ System remains stable

---

## Regression Testing

### 11. End-to-End Workflow Verification

**Objective**: Verify complete workflow produces correct outputs for all agents.

**Steps**:
1. Use a known good transcript
2. Execute complete workflow
3. Verify outputs from all 12 agents

**Expected Agent Outputs**:
- ✅ **Storage Agent**: Stores transcript successfully
- ✅ **Transcript Agent**: Produces cleaned and structured transcript
- ✅ **Researcher Agent**: Generates research insights
- ✅ **Requirements Agent**: Extracts functional and non-functional requirements
- ✅ **Knowledge Base Agent**: Creates knowledge base entries
- ✅ **PRD Agent**: Generates Product Requirements Document
- ✅ **Mockup Agent**: Creates UI/UX mockups
- ✅ **Synthetic Data Agent**: Generates test data
- ✅ **Commercial Proposal Agent**: Creates business proposal
- ✅ **BOM Agent**: Generates Bill of Materials
- ✅ **Architecture Diagram Agent**: Creates system architecture
- ✅ **Reviewer Agent**: Provides review and recommendations

---

## Test Execution Checklist

- [ ] Test 1: Normal Workflow Execution
- [ ] Test 2: WebSocket Reconnection
- [ ] Test 3: Duplicate Start Request Prevention
- [ ] Test 4: Workflow Timeout
- [ ] Test 5: Per-Agent Timeout
- [ ] Test 6: Workflow Status API
- [ ] Test 7: Multiple Concurrent Workflows
- [ ] Test 8: Reconnection After Completion
- [ ] Test 9: Stress Test - Rapid Reconnections
- [ ] Test 10: Load Test - Multiple Users
- [ ] Test 11: End-to-End Workflow Verification

## Success Criteria

All tests must pass with the following criteria:
1. ✅ No infinite loops occur in any scenario
2. ✅ No duplicate workflow executions occur
3. ✅ Reconnection works correctly without restarting workflows
4. ✅ Timeouts work as expected
5. ✅ All agents execute exactly once per workflow
6. ✅ Workflow state is tracked correctly
7. ✅ Error handling works properly
8. ✅ System remains stable under load

## Reporting

For each test, document:
- Test name and number
- Date and time executed
- Pass/Fail status
- Actual results vs expected results
- Screenshots or logs (if applicable)
- Any issues discovered
- Notes or observations

