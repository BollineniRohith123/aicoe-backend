import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { 
  Upload, FileText, Sparkles, AlertCircle, 
  CheckCircle2, ArrowRight, ArrowLeft 
} from "lucide-react";
import "./TranscriptInput.css";

export default function TranscriptInputEnhanced() {
  const navigate = useNavigate();
  const [projectName, setProjectName] = useState("");
  const [transcript, setTranscript] = useState("");
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = () => {
    const newErrors = {};
    
    if (!projectName.trim()) {
      newErrors.projectName = "Project name is required";
    } else if (projectName.trim().length < 3) {
      newErrors.projectName = "Project name must be at least 3 characters";
    }
    
    if (!transcript.trim()) {
      newErrors.transcript = "Transcript is required";
    } else if (transcript.trim().length < 50) {
      newErrors.transcript = "Transcript must be at least 50 characters";
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }
    
    setIsSubmitting(true);
    
    // Simulate brief processing
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Navigate to processing with data
    navigate("/processing", {
      state: {
        projectName,
        transcript
      }
    });
  };

  const loadSampleTranscript = async () => {
    try {
      const response = await fetch("/test_transcript_ui_test.txt");
      if (response.ok) {
        const text = await response.text();
        setTranscript(text);
        setProjectName("Task Management App");
      }
    } catch (error) {
      // Fallback sample
      setTranscript(`Meeting Transcript - Task Management App

Date: November 1, 2025
Attendees: Product Manager, Tech Lead, UX Designer

Product Manager: Good morning everyone. Today we're going to discuss building a simple task management application. We need something clean and intuitive.

Tech Lead: Sounds good. What are the core features we're looking at?

Product Manager: Let's keep it simple for the MVP. We need:
1. User registration and login
2. Create, view, and manage tasks
3. Mark tasks as complete
4. Simple dashboard to see all tasks

UX Designer: I like the simplicity. For the user registration, should we include social login options?

Product Manager: No, let's keep it simple with email and password for now. We can add OAuth later.`);
      setProjectName("Task Management App");
    }
  };

  const characterCount = transcript.length;
  const wordCount = transcript.trim().split(/\s+/).filter(word => word.length > 0).length;

  return (
    <div className="transcript-input-container">
      {/* Header */}
      <header className="input-header">
        <div className="input-header-content">
          <Button
            variant="ghost"
            onClick={() => navigate("/")}
            className="back-button"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="input-main">
        <div className="input-content">
          {/* Title Section */}
          <div className="input-title-section">
            <div className="title-badge">
              <Sparkles className="w-4 h-4" />
              <span>Step 1 of 3</span>
            </div>
            <h1 className="input-title">
              Upload Your Meeting Transcript
            </h1>
            <p className="input-subtitle">
              Our AI agents will analyze your transcript and generate comprehensive 
              project documentation including PRDs, mockups, and technical specifications.
            </p>
          </div>

          {/* Form Card */}
          <Card className="input-form-card">
            <form onSubmit={handleSubmit} className="input-form">
              {/* Project Name Field */}
              <div className="form-field">
                <Label htmlFor="projectName" className="form-label">
                  <FileText className="w-4 h-4" />
                  Project Name
                </Label>
                <Input
                  id="projectName"
                  type="text"
                  placeholder="e.g., Task Management System"
                  value={projectName}
                  onChange={(e) => {
                    setProjectName(e.target.value);
                    if (errors.projectName) {
                      setErrors({...errors, projectName: null});
                    }
                  }}
                  className={`form-input ${errors.projectName ? 'input-error' : ''}`}
                />
                {errors.projectName && (
                  <div className="error-message">
                    <AlertCircle className="w-4 h-4" />
                    {errors.projectName}
                  </div>
                )}
              </div>

              {/* Transcript Field */}
              <div className="form-field">
                <div className="label-row">
                  <Label htmlFor="transcript" className="form-label">
                    <Upload className="w-4 h-4" />
                    Meeting Transcript
                  </Label>
                  <Button
                    type="button"
                    variant="link"
                    size="sm"
                    onClick={loadSampleTranscript}
                    className="sample-button"
                  >
                    Load Sample
                  </Button>
                </div>
                <Textarea
                  id="transcript"
                  placeholder="Paste your meeting transcript here..."
                  value={transcript}
                  onChange={(e) => {
                    setTranscript(e.target.value);
                    if (errors.transcript) {
                      setErrors({...errors, transcript: null});
                    }
                  }}
                  className={`form-textarea ${errors.transcript ? 'input-error' : ''}`}
                  rows={15}
                />
                {errors.transcript && (
                  <div className="error-message">
                    <AlertCircle className="w-4 h-4" />
                    {errors.transcript}
                  </div>
                )}
                
                {/* Character Count */}
                <div className="character-count">
                  <span className={characterCount < 50 ? 'count-warning' : 'count-ok'}>
                    {characterCount.toLocaleString()} characters • {wordCount.toLocaleString()} words
                  </span>
                  {characterCount < 50 && (
                    <span className="count-hint">
                      (Minimum 50 characters required)
                    </span>
                  )}
                </div>
              </div>

              {/* Features Info */}
              <div className="features-info">
                <div className="feature-item">
                  <CheckCircle2 className="w-5 h-5 text-green-500" />
                  <span>Multi-agent AI processing</span>
                </div>
                <div className="feature-item">
                  <CheckCircle2 className="w-5 h-5 text-green-500" />
                  <span>Generates 7+ deliverables</span>
                </div>
                <div className="feature-item">
                  <CheckCircle2 className="w-5 h-5 text-green-500" />
                  <span>Real-time progress tracking</span>
                </div>
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                size="lg"
                disabled={isSubmitting}
                className="submit-button"
              >
                {isSubmitting ? (
                  <>
                    <div className="spinner-small" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2" />
                    Start AI Processing
                    <ArrowRight className="w-5 h-5 ml-2" />
                  </>
                )}
              </Button>
            </form>
          </Card>

          {/* Info Cards */}
          <div className="info-cards">
            <Card className="info-card">
              <h3 className="info-card-title">What happens next?</h3>
              <ul className="info-card-list">
                <li>12 AI agents analyze your transcript</li>
                <li>Generate PRDs, mockups, and proposals</li>
                <li>Real-time progress updates</li>
                <li>Download all deliverables</li>
              </ul>
            </Card>
            
            <Card className="info-card">
              <h3 className="info-card-title">Processing Time</h3>
              <ul className="info-card-list">
                <li>Average: 20-30 minutes</li>
                <li>Depends on transcript length</li>
                <li>Real-time status updates</li>
                <li>Can navigate away safely</li>
              </ul>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
