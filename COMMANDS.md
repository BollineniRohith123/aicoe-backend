# 🎯 AICOE Platform - Quick Command Reference

## 🚀 Starting the Platform

### Quick Start (Recommended)
```bash
# Start both frontend and backend
./start.sh

# Check status
./status.sh

# Stop all servers
./stop.sh
```

### Manual Start - Backend
```bash
cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main/backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### Manual Start - Frontend
```bash
cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main/frontend
npm start
```

---

## 🔍 Status Checks

### Check if Servers are Running
```bash
./status.sh
```

### Check Backend Health
```bash
curl http://localhost:8000/health
```

### Check Frontend
```bash
curl http://localhost:3000
```

### Check Ports
```bash
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
```

### Check Processes
```bash
ps aux | grep uvicorn
ps aux | grep react-scripts
```

---

## 📊 View Logs

### Backend Logs
```bash
# Real-time logs (if using start.sh)
tail -f logs/backend.log

# Last 50 lines
tail -n 50 logs/backend.log

# Search for errors
grep -i error logs/backend.log
```

### Frontend Logs
```bash
# Real-time logs (if using start.sh)
tail -f logs/frontend.log

# Last 50 lines
tail -n 50 logs/frontend.log

# Search for errors
grep -i error logs/frontend.log
```

---

## 🛑 Stopping Servers

### Using Script
```bash
./stop.sh
```

### Kill Backend Port
```bash
lsof -ti :8000 | xargs kill -9
```

### Kill Frontend Port
```bash
lsof -ti :3000 | xargs kill -9
```

### Kill All Related Processes
```bash
pkill -f "uvicorn server:app"
pkill -f "react-scripts start"
```

---

## 🔧 Troubleshooting

### Restart Everything
```bash
./stop.sh
sleep 2
./start.sh
```

### Reinstall Backend Dependencies
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Reinstall Frontend Dependencies
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Clear Frontend Cache
```bash
cd frontend
rm -rf node_modules/.cache
npm start
```

### Recreate Virtual Environment
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 Access URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |

---

## 🧪 Testing Commands

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test Backend API
```bash
curl http://localhost:8000/api/projects
curl http://localhost:8000/api/agents/status
```

### Test Frontend Loading
```bash
curl -I http://localhost:3000
```

### Run Backend Tests
```bash
cd backend
source venv/bin/activate
pytest tests/
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

---

## 📦 Build Commands

### Build Frontend for Production
```bash
cd frontend
npm run build
```

### Check Build Size
```bash
cd frontend
npm run build
du -sh build/
```

---

## 🔐 Environment Setup

### Check Environment Variables
```bash
# Backend
cat backend/.env

# Frontend (if exists)
cat frontend/.env
```

### Create Backend .env
```bash
cat > backend/.env << EOF
OPENROUTER_API_KEY=your_api_key_here
EOF
```

---

## 📈 Performance Commands

### Check Memory Usage
```bash
ps aux | grep -E "uvicorn|react-scripts" | awk '{print $2, $3, $4, $11}'
```

### Monitor System Resources
```bash
top -pid $(lsof -ti :8000)  # Backend
top -pid $(lsof -ti :3000)  # Frontend
```

---

## 🗂️ File Operations

### Find Files
```bash
# Find Python files
find . -name "*.py" -type f

# Find JavaScript files
find frontend/src -name "*.js" -type f

# Find configuration files
find . -name "*.json" -type f
```

### Search in Files
```bash
# Search for API calls
grep -r "fetch(" frontend/src/

# Search for API endpoints
grep -r "@app" backend/

# Search for console errors
grep -r "console.error" frontend/src/
```

---

## 🐛 Debug Commands

### Enable Debug Mode (Backend)
```bash
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### Check Network Connectivity
```bash
# Test localhost
ping localhost

# Test specific ports
nc -zv localhost 8000
nc -zv localhost 3000
```

### View All Open Files
```bash
lsof -p $(lsof -ti :8000)  # Backend
lsof -p $(lsof -ti :3000)  # Frontend
```

---

## 📊 Git Commands

### Check Status
```bash
git status
```

### View Recent Changes
```bash
git log --oneline -10
```

### Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### Commit Changes
```bash
git add .
git commit -m "Your commit message"
```

---

## 💻 Chrome DevTools Testing

### Open DevTools
- Press `F12`
- Or `Cmd+Option+I` (Mac)
- Or `Ctrl+Shift+I` (Windows/Linux)

### Run in Browser Console
```javascript
// Test backend connection
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log);

// Test WebSocket
const ws = new WebSocket('ws://localhost:8000/api/ws/test-' + Date.now());
ws.onopen = () => console.log('WebSocket connected!');

// Test API endpoints
fetch('http://localhost:8000/api/projects')
  .then(r => r.json())
  .then(console.log);
```

---

## 📝 Useful Aliases (Optional)

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# AICOE shortcuts
alias aicoe-start='cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main && ./start.sh'
alias aicoe-stop='cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main && ./stop.sh'
alias aicoe-status='cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main && ./status.sh'
alias aicoe-logs-backend='tail -f /Users/rohithbollineni/Downloads/AICOE/AICOE-Main/logs/backend.log'
alias aicoe-logs-frontend='tail -f /Users/rohithbollineni/Downloads/AICOE/AICOE-Main/logs/frontend.log'
```

Then reload:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

---

## 🎯 Common Workflows

### Full Restart
```bash
./stop.sh && sleep 2 && ./start.sh
```

### Check Everything
```bash
./status.sh && curl http://localhost:8000/health && curl -I http://localhost:3000
```

### View All Logs
```bash
tail -f logs/backend.log logs/frontend.log
```

### Clean and Restart
```bash
./stop.sh
cd backend && rm -rf __pycache__ && cd ..
cd frontend && rm -rf node_modules/.cache && cd ..
./start.sh
```

---

## 📞 Quick Help

**Problem: Port already in use**
```bash
lsof -ti :8000 | xargs kill -9
lsof -ti :3000 | xargs kill -9
```

**Problem: Module not found**
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

**Problem: Can't connect to backend**
```bash
# Check backend is running
lsof -i :8000

# Check logs
tail -n 50 logs/backend.log

# Restart backend
./stop.sh && ./start.sh
```

**Problem: Frontend not loading**
```bash
# Clear cache and restart
cd frontend
rm -rf node_modules/.cache
npm start
```

---

## 🚀 Production Deployment (Future)

### Build for Production
```bash
# Frontend
cd frontend
npm run build

# Backend (no build needed, but ensure dependencies installed)
cd backend
pip install -r requirements.txt
```

### Run Production Server
```bash
# Backend with production settings
uvicorn server:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend (serve build folder with nginx or similar)
# See deployment documentation
```

---

## 📚 Documentation Links

- Full README: `README.md`
- Startup Guide: `STARTUP_GUIDE.md`
- Chrome Testing: `CHROME_TESTING_GUIDE.md`
- API Docs (when running): http://localhost:8000/docs

---

## 💡 Pro Tips

1. **Always check status first**: `./status.sh`
2. **Use logs for debugging**: `tail -f logs/backend.log`
3. **Keep terminals organized**: One for backend, one for frontend
4. **Use browser DevTools**: Press F12 for instant debugging
5. **Restart when in doubt**: `./stop.sh && ./start.sh`

---

**Quick Start Reminder:**
```bash
./start.sh        # Start everything
./status.sh       # Check status
./stop.sh         # Stop everything
```

**That's it! Happy coding! 🎉**