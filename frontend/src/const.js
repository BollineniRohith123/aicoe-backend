// Application Constants
export const APP_TITLE = "AICOE Automation Platform";
export const APP_LOGO = null; // Set to image URL if you have a logo

// Robust backend URL detection with fallback
const getBackendURL = () => {
  // Try environment variable first
  if (process.env.REACT_APP_BACKEND_URL) {
    return process.env.REACT_APP_BACKEND_URL;
  }
  
  // Check if we're in development (localhost)
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8001';
  }
  
  // For production, use same origin with /api prefix
  return window.location.origin;
};

export const API_BASE_URL = getBackendURL();
