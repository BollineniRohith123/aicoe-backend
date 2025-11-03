# 🚀 AICOE Platform Startup Guide

## Quick Start (Recommended)

### Option 1: Using Startup Scripts (Easiest)

We've created convenient scripts to start and manage your servers:

```bash
# Start both backend and frontend
./start.sh

# Check server status
./status.sh

# Stop all servers
./stop.sh
```

The `start.sh` script will:
- ✅ Check if ports 8000 and 3000 are available
- ✅ Verify virtual environment and dependencies
- ✅ Start backend on port 8000
- ✅ Start frontend on port 3000
- ✅ Create log files for debugging
- ✅ Display all server URLs

---

## Option 2: Manual Startup (For Development)

If you prefer to start servers manually or need to see live logs:

### Terminal 1: Backend Server

```bash
cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main/backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Terminal 2: Frontend Server

```bash
cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main/frontend
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.

webpack compiled successfully
```

---

## 🌐 Access Points

Once both servers are running:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application UI |
| **Backend API** | http://localhost:8000 | REST API endpoints |
| **API Documentation** | http://localhost:8000/docs | Interactive Swagger UI |
| **API Redoc** | http://localhost:8000/redoc | Alternative API docs |
| **Health Check** | http://localhost:8000/health | Server health status |

---

## ✅ Verification Steps

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 2. Check Frontend Loading

Open http://localhost:3000 in your browser. You should see:
- ✅ AICOE Platform landing page
- ✅ Navigation menu
- ✅ No console errors (check DevTools)

### 3. Check WebSocket Connection

In the browser console (F12), you should see:
```
WebSocket connection established
Connected to backend at ws://localhost:8000
```

---

## 🔍 Using Chrome DevTools to Verify

### Open Chrome DevTools

1. Open Chrome browser
2. Navigate to http://localhost:3000
3. Press `F12` or `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows)

### Check Console Tab

✅ **Good signs:**
- "React App started successfully"
- No red error messages
- WebSocket connection messages

❌ **Bad signs:**
- Red error messages about failed API calls
- "Failed to fetch" errors
- CORS errors

### Check Network Tab

1. Click "Network" tab in DevTools
2. Reload the page (`Cmd+R` or `Ctrl+R`)
3. Look for:
   - ✅ Status 200 for main HTML file
   - ✅ Status 200 for JavaScript bundles
   - ✅ Status 200 for API calls to localhost:8000
   - ✅ Status 101 for WebSocket upgrade

### Check Application Tab

1. Click "Application" tab
2. Look at "Local Storage" → http://localhost:3000
3. Verify any stored workflow IDs or user preferences

---

## 🐛 Troubleshooting

### Backend Issues

#### "Port 8000 already in use"

```bash
# Find and kill process on port 8000
lsof -ti :8000 | xargs kill -9

# Or use the stop script
./stop.sh
```

#### "ModuleNotFoundError"

```bash
# Reinstall dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### "OPENROUTER_API_KEY not found"

```bash
# Check if .env file exists
cat backend/.env

# Should contain:
OPENROUTER_API_KEY=your_key_here
```

### Frontend Issues

#### "Port 3000 already in use"

```bash
# Find and kill process on port 3000
lsof -ti :3000 | xargs kill -9

# Or use the stop script
./stop.sh
```

#### "Module not found" errors

```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### "Cannot connect to backend"

1. Verify backend is running on port 8000
2. Check browser console for CORS errors
3. Verify `REACT_APP_BACKEND_URL` in frontend/.env (if it exists)

### WebSocket Issues

#### "WebSocket connection failed"

1. Check if backend is running
2. Try accessing http://localhost:8000/docs
3. Look for firewall/antivirus blocking WebSocket connections
4. Check browser console for specific error messages

---

## 📊 Monitoring Logs

### View Backend Logs

```bash
# If using start.sh script
tail -f logs/backend.log

# If running manually, check the terminal where uvicorn is running
```

### View Frontend Logs

```bash
# If using start.sh script
tail -f logs/frontend.log

# If running manually, check the terminal where npm start is running
```

### Check for Errors

```bash
# Search for errors in backend logs
grep -i error logs/backend.log

# Search for errors in frontend logs
grep -i error logs/frontend.log
```

---

## 🧪 Testing the Platform

### 1. Upload a Test Transcript

1. Navigate to http://localhost:3000
2. Click "New Project" or "Upload Transcript"
3. Upload `test-transcript.txt` from the root directory
4. Watch the real-time progress as agents process the transcript

### 2. Monitor Agent Progress

In the browser:
- Watch the progress indicators animate
- See which agent is currently active
- View status messages in real-time

### 3. Check Results

Once complete:
- Navigate to the Results Playground
- View generated PRD, mockups, proposals, etc.
- Download individual files or entire project

---

## 🔧 Development Mode Features

### Backend Hot Reload

The `--reload` flag enables automatic server restart when code changes:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

Changes to these files will trigger reload:
- `backend/server.py`
- `backend/agents/*.py`
- Any Python file in the backend directory

### Frontend Hot Reload

React development server automatically refreshes on code changes:

```bash
npm start
```

Changes to these files will trigger reload:
- `frontend/src/**/*.js`
- `frontend/src/**/*.jsx`
- `frontend/src/**/*.css`

---

## 🎯 Next Steps After Startup

1. **✅ Verify Both Servers Running**
   ```bash
   ./status.sh
   ```

2. **✅ Open Browser**
   - Navigate to http://localhost:3000
   - Open DevTools (F12)

3. **✅ Check Backend API**
   - Visit http://localhost:8000/docs
   - Try the `/health` endpoint

4. **✅ Test Upload Feature**
   - Upload a test transcript
   - Monitor progress in real-time

5. **✅ Explore Results**
   - View generated deliverables
   - Download files
   - Share project

---

## 🚦 System Status Commands

```bash
# Check if servers are running
./status.sh

# View live backend logs
tail -f logs/backend.log

# View live frontend logs
tail -f logs/frontend.log

# Check backend health
curl http://localhost:8000/health

# Check frontend accessibility
curl http://localhost:3000

# List all running processes
ps aux | grep -E "uvicorn|react-scripts"

# Check port usage
lsof -i :8000
lsof -i :3000
```

---

## 💡 Tips for Chrome DevTools Debugging

### Console Debugging

```javascript
// In browser console, check backend connection
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)

// Check WebSocket connection
const ws = new WebSocket('ws://localhost:8000/api/ws/test-workflow')
ws.onopen = () => console.log('WebSocket connected!')
ws.onerror = (err) => console.error('WebSocket error:', err)
```

### Network Tab Filters

- Filter by type: `is:websocket` to see WebSocket connections
- Filter by status: `status-code:404` to find missing resources
- Filter by domain: `domain:localhost:8000` for backend calls

### Performance Monitoring

1. Click "Performance" tab
2. Click "Record" button
3. Interact with the application
4. Click "Stop" to see performance report
5. Look for long tasks, layout shifts, and slow API calls

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Logs First**
   ```bash
   ./status.sh
   tail -n 50 logs/backend.log
   tail -n 50 logs/frontend.log
   ```

2. **Verify Environment**
   ```bash
   # Check Python version
   python3 --version  # Should be 3.8+
   
   # Check Node version
   node --version     # Should be 14+
   
   # Check npm version
   npm --version      # Should be 6+
   ```

3. **Check Dependencies**
   ```bash
   # Backend
   cd backend
   source venv/bin/activate
   pip list | grep -E "fastapi|uvicorn|openai"
   
   # Frontend
   cd frontend
   npm list --depth=0 | grep -E "react|axios"
   ```

4. **Clean Restart**
   ```bash
   ./stop.sh
   sleep 2
   ./start.sh
   ```

---

## 📝 Summary

**To start the platform:**
```bash
./start.sh
```

**To verify it's working:**
- ✅ Backend: http://localhost:8000/docs
- ✅ Frontend: http://localhost:3000
- ✅ Status: `./status.sh`

**To stop the platform:**
```bash
./stop.sh
```

**Happy coding! 🚀**