# Testing the Reconnection Loop Fix

## Changes Made

### Frontend (`frontend/src/hooks/useWorkflowWebSocket.js`)

1. **Fixed reconnection detection logic** (lines 77-79):
   - Now checks if workflow_id matches to determine if it's a reconnection
   - Resets `reconnectAttemptsRef.current = 0` for new workflows
   - This prevents sending "reconnect" on the first connection

2. **Removed premature reset of reconnect counter** (line 124):
   - No longer resets counter after successful reconnection
   - Counter only resets when workflow completes or fails
   - This ensures subsequent disconnections continue sending "reconnect"

3. **Added counter reset on workflow completion** (lines 253, 268):
   - Resets `reconnectAttemptsRef.current = 0` in `handleComplete()`
   - Resets `reconnectAttemptsRef.current = 0` in `handleError()`
   - Prepares for next workflow to start fresh

### Backend (`backend/server.py`)

No changes needed - the backend already handles both "start" and "reconnect" actions correctly and falls through to the "Keep connection alive" loop.

## Expected Behavior After Fix

### Scenario 1: Normal Workflow Start
1. User starts workflow
2. Frontend generates new workflow_id
3. `reconnectAttemptsRef.current = 0` (new workflow)
4. Frontend sends `{"action": "start", ...}`
5. Backend starts workflow
6. Connection stays alive for progress updates

### Scenario 2: WebSocket Disconnection During Workflow
1. Workflow is running
2. WebSocket disconnects
3. `reconnectAttemptsRef.current` increments to 1
4. Frontend reconnects
5. Frontend sends `{"action": "reconnect", "workflow_id": "..."}`
6. Backend sends `{"type": "reconnect_ack", ...}`
7. Connection stays alive
8. Progress updates continue
9. **No duplicate workflow execution**

### Scenario 3: Multiple Disconnections
1. Workflow is running
2. First disconnection → reconnect (counter = 1)
3. Second disconnection → reconnect (counter = 2)
4. Third disconnection → reconnect (counter = 3)
5. Each time sends "reconnect", not "start"
6. Workflow continues without restart

### Scenario 4: Workflow Completion
1. Workflow completes
2. `handleComplete()` resets counter to 0
3. User starts new workflow
4. Counter is 0, so sends "start"

## Testing Steps

1. **Start the backend** (if not already running):
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn server:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start the frontend** (if not already running):
   ```bash
   cd frontend
   npm start
   ```

3. **Test normal workflow**:
   - Navigate to http://localhost:3000
   - Enter project name and transcript
   - Click "Start Workflow"
   - Verify workflow starts (check backend logs for "Starting workflow")
   - Verify no "reconnect" messages on first connection

4. **Test reconnection** (manual):
   - Start a workflow
   - Open browser DevTools → Network tab → WS
   - Find the WebSocket connection
   - Right-click → Close connection
   - Wait for automatic reconnection
   - Verify "reconnect" message is sent (not "start")
   - Verify workflow continues without restart

5. **Check backend logs**:
   - Should see "Starting workflow" only once
   - Should see "Client reconnecting" on reconnections
   - Should NOT see multiple "Starting workflow" messages
   - Should NOT see infinite reconnection loop

## Success Criteria

✅ First connection sends "start" action
✅ Reconnections send "reconnect" action  
✅ No infinite reconnection loop
✅ Workflow executes only once
✅ Progress updates continue after reconnection
✅ Workflow completes successfully

## Troubleshooting

If you still see issues:

1. **Clear browser cache and reload**
2. **Check React Strict Mode** - it may cause double mounting in development
3. **Check browser console** for WebSocket errors
4. **Check backend logs** for the exact sequence of messages
5. **Verify workflow_id** is consistent across reconnections

## Additional Notes

- The fix addresses the root cause: incorrect detection of reconnection vs new workflow
- The backend code was already correct - it properly handles both "start" and "reconnect"
- The frontend now correctly identifies when to send each action type
- The reconnection counter is managed properly throughout the workflow lifecycle

