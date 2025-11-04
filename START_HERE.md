# 🎯 START HERE - AICOE Platform Quick Start

## ✅ What's Been Set Up For You

Your AICOE Platform is ready to launch! Here's what has been prepared:

### 📁 New Files Created

1. **`start.sh`** - Automated startup script for both servers
2. **`stop.sh`** - Gracefully stops all running servers
3. **`status.sh`** - Checks the health of your servers
4. **`STARTUP_GUIDE.md`** - Comprehensive startup documentation
5. **`CHROME_TESTING_GUIDE.md`** - Chrome DevTools testing procedures
6. **`COMMANDS.md`** - Quick command reference cheat sheet
7. **`START_HERE.md`** - This file (your starting point)

### ✅ Pre-flight Checks Completed

- ✅ Python 3.13.7 installed
- ✅ Node.js v24.10.0 installed
- ✅ npm 11.6.0 installed
- ✅ Backend virtual environment exists
- ✅ Frontend node_modules installed
- ✅ Backend .env file exists
- ✅ All scripts are executable

---

## 🚀 STEP 1: Start Your Servers

You have **TWO OPTIONS** to start the platform:

### Option A: Automatic Start (Recommended) ⭐

Open a terminal and run:

```bash
cd /Users/rohithbollineni/Downloads/AICOE/AICOE-Main
./start.sh
```

**What this does:**
- ✅ Checks if ports 8000 and 3000 are available
- ✅ Starts backend server on port 8000
- ✅ Starts frontend server on port 3000
- ✅ Creates log files for debugging
- ✅ Shows you all access URLs

**Expected Output:**
```
🚀 Starting AICOE Platform...
================================
✅ Pre-flight checks complete!
================================

🔧 Starting Backend Server (Port 8000)...
✅ Backend server started successfully (PID: 12345)
   🌐 Backend URL: http://localhost:8000
   📚 API Docs: http://localhost:8000/docs

⚛️  Starting Frontend Server (Port 3000)...
⏳ Waiting for frontend to start (this may take 30-60 seconds)...
✅ Frontend server started successfully (PID: 12346)
   🌐 Frontend URL: http://localhost:3000

================================
🎉 AICOE Platform is running!
================================

📱 Frontend: http://localhost:3000
🔧 Backend:  http://localhost:8000
📚 API Docs: http://localhost:8000/docs
```

---

### Option B: Manual Start (For Development)

If you want to see live logs in separate terminals:

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

---

## 🔍 STEP 2: Verify Everything is Running

### Quick Status Check

```bash
./status.sh
```

**Expected Output:**
```
🔍 AICOE Platform Status Check
================================

🔧 Backend Server (Port 8000)
----------------------------
Status: ✅ RUNNING
Health Check: ✅ HEALTHY
URL: http://localhost:8000

⚛️  Frontend Server (Port 3000)
----------------------------
Status: ✅ RUNNING
Health Check: ✅ HEALTHY
URL: http://localhost:3000

================================
✅ All systems operational!
```

### Manual Verification

```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl -I http://localhost:3000

# Check if ports are listening
lsof -i :8000
lsof -i :3000
```

---

## 🌐 STEP 3: Open in Browser

1. **Open Chrome Browser**

2. **Navigate to Frontend:**
   ```
   http://localhost:3000
   ```

3. **Open Chrome DevTools:**
   - Press `F12` (Windows/Linux)
   - Press `Cmd+Option+I` (Mac)
   - Or right-click → "Inspect"

4. **Verify in Console Tab:**
   ```javascript
   // Run this in the browser console:
   fetch('http://localhost:8000/health')
     .then(r => r.json())
     .then(data => console.log('Backend Status:', data));
   ```

   **Expected Output:**
   ```javascript
   Backend Status: { status: "healthy", timestamp: "2024-..." }
   ```

---

## 🧪 STEP 4: Test the Platform

### Basic Functionality Test

1. **Check the Homepage**
   - ✅ Page loads without errors
   - ✅ No red errors in console
   - ✅ UI elements are visible
   - ✅ Styles are applied

2. **Test Navigation**
   - ✅ Click through menu items
   - ✅ All pages load correctly

3. **Test File Upload** (if applicable)
   - ✅ Upload test transcript
   - ✅ Watch agent progress
   - ✅ View results

### Chrome DevTools Checklist

Open DevTools (F12) and check:

**Console Tab:**
- [ ] No red error messages
- [ ] React app initialized
- [ ] WebSocket connected (if applicable)

**Network Tab:**
- [ ] All resources loaded (status 200)
- [ ] API calls successful
- [ ] No CORS errors
- [ ] WebSocket upgrade successful

**Performance Tab:**
- [ ] First Contentful Paint < 2s
- [ ] No long tasks
- [ ] Smooth interactions

---

## 🛑 STEP 5: Stop the Servers (When Done)

### Using Stop Script

```bash
./stop.sh
```

**Output:**
```
🛑 Stopping AICOE Platform...
================================
🔧 Stopping Backend Server...
✅ Backend server stopped
⚛️  Stopping Frontend Server...
✅ Frontend server stopped
✅ AICOE Platform stopped successfully!
```

### Manual Stop

```bash
# Kill backend
lsof -ti :8000 | xargs kill -9

# Kill frontend
lsof -ti :3000 | xargs kill -9
```

---

## 🚨 Troubleshooting

### Problem: Port Already in Use

```bash
# Solution: Kill existing processes
lsof -ti :8000 | xargs kill -9
lsof -ti :3000 | xargs kill -9

# Then restart
./start.sh
```

### Problem: Backend Not Responding

```bash
# Check logs
tail -n 50 logs/backend.log

# Look for errors
grep -i error logs/backend.log

# Restart backend only
lsof -ti :8000 | xargs kill -9
cd backend && source venv/bin/activate && uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### Problem: Frontend Not Loading

```bash
# Check logs
tail -n 50 logs/frontend.log

# Clear cache and restart
cd frontend
rm -rf node_modules/.cache
npm start
```

### Problem: Missing API Key

```bash
# Check if .env file exists
cat backend/.env

# Should contain:
SYNTHETIC_API_KEY=your_actual_api_key_here
# OPENROUTER_API_KEY=your_actual_api_key_here  # Optional fallback
```

---

## 📚 Additional Resources

| Document | Purpose |
|----------|---------|
| `STARTUP_GUIDE.md` | Detailed startup instructions |
| `CHROME_TESTING_GUIDE.md` | Complete testing procedures |
| `COMMANDS.md` | Quick command reference |
| `README.md` | Full project documentation |

---

## 🎯 Quick Commands Summary

```bash
# Start everything
./start.sh

# Check status
./status.sh

# View backend logs
tail -f logs/backend.log

# View frontend logs
tail -f logs/frontend.log

# Stop everything
./stop.sh

# Restart everything
./stop.sh && sleep 2 && ./start.sh
```

---

## 🌟 What to Do Once Running

1. **Explore the UI**
   - Navigate through all pages
   - Test buttons and interactions
   - Check responsive design

2. **Test API Endpoints**
   - Visit http://localhost:8000/docs
   - Try different endpoints
   - Check response times

3. **Upload Test Data**
   - Use `test-transcript.txt`
   - Monitor agent execution
   - View generated results

4. **Monitor Performance**
   - Use Chrome DevTools Performance tab
   - Check Lighthouse scores
   - Optimize as needed

---

## ✅ Success Checklist

- [ ] Servers started successfully
- [ ] Status check shows all green
- [ ] Frontend loads in browser
- [ ] Backend health endpoint responds
- [ ] No console errors
- [ ] API documentation accessible
- [ ] Can upload and process files
- [ ] Results display correctly

---

## 🆘 Need Help?

If you encounter issues:

1. **Check the logs:**
   ```bash
   ./status.sh
   tail -n 100 logs/backend.log
   tail -n 100 logs/frontend.log
   ```

2. **Try a clean restart:**
   ```bash
   ./stop.sh
   sleep 2
   ./start.sh
   ```

3. **Verify environment:**
   ```bash
   python3 --version  # Should be 3.8+
   node --version     # Should be 14+
   npm --version      # Should be 6+
   ```

4. **Check the guides:**
   - `STARTUP_GUIDE.md` for detailed startup help
   - `CHROME_TESTING_GUIDE.md` for testing procedures
   - `COMMANDS.md` for quick command reference

---

## 🎉 You're All Set!

Your AICOE Platform is ready to use. Start the servers and begin building amazing AI-powered workflows!

```bash
# Let's go! 🚀
./start.sh
```

**Happy Coding! 💻✨**