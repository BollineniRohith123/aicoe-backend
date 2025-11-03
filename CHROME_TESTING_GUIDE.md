# 🌐 Chrome DevTools MCP Testing Guide

## Overview

This guide will help you test the AICOE Platform using Chrome DevTools MCP (Model Context Protocol) to verify that the application loads correctly and functions as expected.

---

## Prerequisites

Before starting, ensure:

1. ✅ Backend server is running on `http://localhost:8000`
2. ✅ Frontend server is running on `http://localhost:3000`
3. ✅ Chrome browser is installed
4. ✅ Chrome DevTools MCP is available

---

## Step-by-Step Testing Process

### Step 1: Start the Servers

You have two options:

#### Option A: Using Startup Script (Recommended)
```bash
cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main
./start.sh
```

#### Option B: Manual Startup

**Terminal 1 - Backend:**
```bash
cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main/backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main/frontend
npm start
```

### Step 2: Verify Server Status

```bash
# Check if both servers are running
./status.sh

# Or manually check
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## Chrome DevTools Testing Checklist

### 1. Initial Page Load Test

**Actions:**
- Open Chrome browser
- Navigate to `http://localhost:3000`
- Open DevTools (F12 or Cmd+Option+I)

**What to Check:**

✅ **Console Tab:**
- No red error messages
- No failed network requests
- React app initialization messages
- WebSocket connection established

✅ **Network Tab:**
- Status 200 for index.html
- Status 200 for main JavaScript bundles
- Status 200 for CSS files
- Status 101 for WebSocket upgrade (if applicable)

✅ **Elements Tab:**
- DOM is fully rendered
- No missing elements
- Styles are applied correctly

### 2. Backend API Connection Test

**Actions in Console:**
```javascript
// Test health endpoint
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(data => console.log('Backend health:', data))
  .catch(err => console.error('Backend error:', err));

// Test projects endpoint
fetch('http://localhost:8000/api/projects')
  .then(r => r.json())
  .then(data => console.log('Projects:', data))
  .catch(err => console.error('Projects error:', err));
```

**Expected Results:**
```javascript
// Backend health response
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z"
}

// Projects response (may be empty array)
{
  "projects": []
}
```

### 3. WebSocket Connection Test

**Actions in Console:**
```javascript
// Test WebSocket connection
const testWorkflowId = 'test-' + Date.now();
const ws = new WebSocket(`ws://localhost:8000/api/ws/${testWorkflowId}`);

ws.onopen = () => {
  console.log('✅ WebSocket connected successfully');
};

ws.onmessage = (event) => {
  console.log('📨 Message received:', JSON.parse(event.data));
};

ws.onerror = (error) => {
  console.error('❌ WebSocket error:', error);
};

ws.onclose = () => {
  console.log('🔌 WebSocket closed');
};
```

**Expected Console Output:**
```
✅ WebSocket connected successfully
```

### 4. UI Interaction Test

**Actions:**
- Click on navigation menu items
- Hover over buttons and cards
- Try to open modals/dialogs
- Test responsive design (resize window)

**What to Check:**
✅ Animations work smoothly
✅ Hover effects are visible
✅ Buttons are clickable
✅ Modals open and close correctly
✅ No layout shifts or jumps
✅ Responsive breakpoints work

### 5. Performance Analysis

**Actions:**
1. Open DevTools Performance tab
2. Click "Record" button
3. Interact with the application
4. Click "Stop" to finish recording

**What to Check:**
✅ First Contentful Paint (FCP) < 1.8s
✅ Largest Contentful Paint (LCP) < 2.5s
✅ Cumulative Layout Shift (CLS) < 0.1
✅ Time to Interactive (TTI) < 3.8s
✅ No long tasks (>50ms)

### 6. Network Performance

**Actions:**
1. Open Network tab
2. Reload page (Cmd+R or Ctrl+R)
3. Review all network requests

**What to Check:**
✅ Total page load time < 3s
✅ No failed requests (status 404, 500)
✅ No CORS errors
✅ API calls complete within 1s
✅ WebSocket upgrade successful
✅ Gzip compression enabled

---

## Common Issues and Solutions

### Issue 1: CORS Errors

**Symptoms:**
```
Access to fetch at 'http://localhost:8000/api/...' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solution:**
- Backend CORS is configured in `server.py`
- Verify `allow_origins=["*"]` in CORS middleware
- Restart backend server

### Issue 2: WebSocket Connection Failed

**Symptoms:**
```
WebSocket connection to 'ws://localhost:8000/api/ws/...' failed
```

**Solution:**
1. Check if backend is running: `curl http://localhost:8000/health`
2. Verify WebSocket endpoint in backend
3. Check firewall/antivirus settings
4. Try using `ws://127.0.0.1:8000` instead

### Issue 3: Failed to Load Resources

**Symptoms:**
```
GET http://localhost:3000/static/... 404 (Not Found)
```

**Solution:**
1. Clear browser cache (Cmd+Shift+Delete)
2. Stop and restart frontend: `npm start`
3. Rebuild: `npm run build`
4. Check `public/` directory for missing files

### Issue 4: React Scripts Not Found

**Symptoms:**
```
sh: react-scripts: command not found
```

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Issue 5: Backend API Not Responding

**Symptoms:**
```
Failed to fetch
TypeError: NetworkError when attempting to fetch resource
```

**Solution:**
1. Verify backend is running: `lsof -i :8000`
2. Check backend logs: `tail -f logs/backend.log`
3. Test health endpoint: `curl http://localhost:8000/health`
4. Restart backend server

---

## Advanced Testing with Chrome DevTools

### 1. Memory Leak Detection

**Actions:**
1. Open DevTools → Memory tab
2. Take heap snapshot (before interaction)
3. Interact with application (upload file, navigate pages)
4. Take another heap snapshot (after interaction)
5. Compare snapshots

**What to Look For:**
- Growing number of detached DOM nodes
- Increasing memory usage without cleanup
- Unreleased event listeners

### 2. Network Throttling

**Actions:**
1. Open DevTools → Network tab
2. Select throttling profile: "Slow 3G" or "Fast 3G"
3. Reload page and test interactions

**What to Check:**
✅ Loading indicators appear
✅ Graceful degradation
✅ No timeouts
✅ User feedback during loading

### 3. JavaScript Coverage

**Actions:**
1. Open DevTools → Sources tab
2. Show Coverage tab (Cmd+Shift+P → "Show Coverage")
3. Click record and interact with app
4. Review unused JavaScript/CSS

**What to Check:**
- Percentage of used vs unused code
- Opportunities for code splitting
- Lazy loading candidates

### 4. Lighthouse Audit

**Actions:**
1. Open DevTools → Lighthouse tab
2. Select categories: Performance, Accessibility, Best Practices, SEO
3. Click "Analyze page load"

**Target Scores:**
- Performance: > 90
- Accessibility: > 90
- Best Practices: > 90
- SEO: > 80

---

## Automated Testing Scripts

### Quick Health Check Script

Save as `check-health.js` and run in browser console:

```javascript
async function checkHealth() {
  console.log('🔍 Starting health checks...\n');
  
  // Check backend
  try {
    const backendRes = await fetch('http://localhost:8000/health');
    const backendData = await backendRes.json();
    console.log('✅ Backend:', backendData);
  } catch (err) {
    console.error('❌ Backend failed:', err.message);
  }
  
  // Check frontend
  try {
    const frontendRes = await fetch('http://localhost:3000');
    if (frontendRes.ok) {
      console.log('✅ Frontend: OK');
    }
  } catch (err) {
    console.error('❌ Frontend failed:', err.message);
  }
  
  // Check WebSocket
  try {
    const ws = new WebSocket(`ws://localhost:8000/api/ws/health-check-${Date.now()}`);
    ws.onopen = () => {
      console.log('✅ WebSocket: Connected');
      ws.close();
    };
    ws.onerror = (err) => {
      console.error('❌ WebSocket failed:', err);
    };
  } catch (err) {
    console.error('❌ WebSocket failed:', err.message);
  }
  
  console.log('\n✅ Health check complete!');
}

checkHealth();
```

### API Endpoint Tester

```javascript
async function testAPIEndpoints() {
  const endpoints = [
    { name: 'Health', url: 'http://localhost:8000/health', method: 'GET' },
    { name: 'Projects', url: 'http://localhost:8000/api/projects', method: 'GET' },
    { name: 'Agents Status', url: 'http://localhost:8000/api/agents/status', method: 'GET' }
  ];
  
  console.log('🧪 Testing API endpoints...\n');
  
  for (const endpoint of endpoints) {
    try {
      const start = Date.now();
      const response = await fetch(endpoint.url, { method: endpoint.method });
      const duration = Date.now() - start;
      
      if (response.ok) {
        console.log(`✅ ${endpoint.name}: ${response.status} (${duration}ms)`);
      } else {
        console.error(`❌ ${endpoint.name}: ${response.status} ${response.statusText}`);
      }
    } catch (err) {
      console.error(`❌ ${endpoint.name}: ${err.message}`);
    }
  }
  
  console.log('\n✅ API test complete!');
}

testAPIEndpoints();
```

---

## Using Chrome DevTools MCP Features

### 1. Take Screenshots

```javascript
// Programmatically take screenshot
// (If using MCP tools)
await chrome.devtools.takeScreenshot();
```

### 2. Monitor Console Messages

```javascript
// Listen to console messages
console.log('Monitoring console...');

// Original console methods
const originalLog = console.log;
const originalError = console.error;

// Override to track
console.log = function(...args) {
  originalLog.apply(console, args);
  // Send to MCP for analysis
};

console.error = function(...args) {
  originalError.apply(console, ['🔴 ERROR:'].concat(args));
  // Send to MCP for analysis
};
```

### 3. Network Request Monitoring

```javascript
// Monitor all fetch requests
const originalFetch = window.fetch;

window.fetch = function(...args) {
  console.log('📡 Fetch request:', args[0]);
  
  return originalFetch.apply(this, args)
    .then(response => {
      console.log('📥 Fetch response:', {
        url: args[0],
        status: response.status,
        ok: response.ok
      });
      return response;
    })
    .catch(error => {
      console.error('📡 Fetch error:', args[0], error);
      throw error;
    });
};
```

---

## Test Scenarios

### Scenario 1: Upload and Process Transcript

1. ✅ Navigate to http://localhost:3000
2. ✅ Click "New Project" button
3. ✅ Upload `test-transcript.txt`
4. ✅ Verify file upload (Network tab shows POST request)
5. ✅ Monitor WebSocket for progress updates
6. ✅ Watch agents execute in sequence
7. ✅ Verify results appear in UI
8. ✅ Download generated files

**Expected Console Messages:**
```
📤 Uploading transcript...
✅ Upload successful
🔌 WebSocket connected
📊 Agent: Intake - Processing transcript...
📊 Agent: Researcher - Gathering insights...
📊 Agent: PRD - Generating document...
✅ Workflow complete!
```

### Scenario 2: View Existing Projects

1. ✅ Navigate to Projects page
2. ✅ Verify API call to `/api/projects`
3. ✅ Check if projects render correctly
4. ✅ Click on a project card
5. ✅ Verify navigation to project details
6. ✅ Check if all deliverables load

### Scenario 3: Real-time Updates

1. ✅ Start a new workflow
2. ✅ Open Network tab → WS filter
3. ✅ Monitor WebSocket messages
4. ✅ Verify progress updates appear in UI
5. ✅ Check animation states
6. ✅ Confirm agent status changes

---

## Success Criteria

Your AICOE Platform is working correctly if:

✅ **Frontend Loads**
- Page loads in < 3 seconds
- No console errors
- All UI elements visible
- Styles applied correctly

✅ **Backend Connected**
- Health endpoint returns 200
- API endpoints accessible
- CORS configured correctly
- No authentication errors

✅ **WebSocket Working**
- Connection established
- Messages received
- Real-time updates work
- Reconnection on disconnect

✅ **Functionality Works**
- File upload succeeds
- Workflows execute
- Results display correctly
- Downloads work

✅ **Performance Acceptable**
- Lighthouse score > 80
- No memory leaks
- Smooth animations
- Fast API responses

---

## Reporting Issues

If you find issues, collect the following information:

1. **Browser Console Logs**
   - Copy all error messages
   - Include stack traces

2. **Network Tab**
   - Screenshot of failed requests
   - Request/response headers
   - Payload data

3. **Backend Logs**
   ```bash
   tail -n 100 logs/backend.log > backend-error.log
   ```

4. **Frontend Logs**
   ```bash
   tail -n 100 logs/frontend.log > frontend-error.log
   ```

5. **System Information**
   - OS version
   - Chrome version
   - Node version
   - Python version

---

## Conclusion

This guide provides comprehensive testing procedures for the AICOE Platform using Chrome DevTools. Follow the checklist to ensure your application is loading and functioning correctly.

**Quick Start Testing:**
```bash
# 1. Start servers
./start.sh

# 2. Check status
./status.sh

# 3. Open browser to http://localhost:3000

# 4. Open DevTools (F12)

# 5. Run health check in console
fetch('http://localhost:8000/health').then(r=>r.json()).then(console.log)
```

**Happy Testing! 🚀**