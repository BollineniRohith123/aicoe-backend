import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Download, ChevronLeft, Eye, Code, FileText } from "lucide-react";
import axios from "axios";
import { API_BASE_URL } from "@/const";

// Simple Markdown renderer component
const MarkdownRenderer = ({ content }) => {
  return (
    <div 
      className="prose prose-sm max-w-none dark:prose-invert"
      dangerouslySetInnerHTML={{ __html: parseMarkdown(content) }}
    />
  );
};

// Basic markdown parser (simplified)
const parseMarkdown = (markdown) => {
  let html = markdown;
  
  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  
  // Bold
  html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
  
  // Italic
  html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');
  
  // Lists
  html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
  html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
  
  // Line breaks
  html = html.replace(/\n/gim, '<br/>');
  
  return html;
};

export default function Results() {
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState("prd");
  const [showMockupPreview, setShowMockupPreview] = useState(true);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = sessionStorage.getItem("lastResult");
    if (stored) {
      try {
        const data = JSON.parse(stored);
        setResult(data);
        setLoading(false);
      } catch (error) {
        console.error("Failed to parse result:", error);
        navigate("/");
      }
    } else {
      navigate("/");
    }
  }, [navigate]);

  const downloadFile = (content, filename, type) => {
    const blob = new Blob([content], { type });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const downloadArtifact = async (projectId, artifactType, filename) => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/download/${projectId}/${artifactType}`,
        { responseType: 'blob' }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Download failed:", error);
      alert("Failed to download file");
    }
  };

  if (loading || !result) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Loading results...</p>
        </div>
      </div>
    );
  }

  const prdContent = result.results?.prd?.prd_markdown || "PRD not available";
  const mockupContent = result.results?.mockup?.mockup_html || "<p>Mockup not available</p>";
  const projectName = result.project_name || "Project";
  const projectId = result.project_id;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card sticky top-0 z-40">
        <div className="container py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate("/")}
                className="gap-2"
              >
                <ChevronLeft className="w-4 h-4" />
                Back
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-foreground">
                  {projectName}
                </h1>
                <p className="text-xs text-muted-foreground">
                  Status: {result.status} | Workflow: {result.workflow_id}
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  if (projectId) {
                    downloadArtifact(projectId, "prd", `${projectName}-PRD.md`);
                  } else {
                    downloadFile(prdContent, `${projectName}-PRD.md`, "text/markdown");
                  }
                }}
                className="gap-2"
              >
                <Download className="w-4 h-4" />
                PRD
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  if (projectId) {
                    downloadArtifact(projectId, "mockup", `${projectName}-Mockup.html`);
                  } else {
                    downloadFile(mockupContent, `${projectName}-Mockup.html`, "text/html");
                  }
                }}
                className="gap-2"
              >
                <Download className="w-4 h-4" />
                Mockup
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-8">
        {/* Success Message */}
        {result.status === "success" && (
          <div className="mb-6 p-4 bg-green-500 bg-opacity-10 border border-green-500 rounded-lg">
            <p className="text-sm text-green-700 dark:text-green-400 font-medium">
              ✅ All agents completed successfully! Your deliverables are ready.
            </p>
          </div>
        )}

        {/* Agent Stages Summary */}
        {result.stages && (
          <Card className="mb-8 p-6">
            <h3 className="text-lg font-semibold text-foreground mb-4">Agent Execution Summary</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {result.stages.map((stage, idx) => (
                <div key={idx} className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                    stage.status === "completed" ? "bg-green-500 text-white" : 
                    stage.status === "failed" ? "bg-red-500 text-white" :
                    "bg-gray-300 text-gray-700"
                  }`}>
                    {stage.status === "completed" ? "✓" : stage.status === "failed" ? "✗" : "•"}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-foreground capitalize">{stage.name}</p>
                    {stage.duration && (
                      <p className="text-xs text-muted-foreground">{stage.duration.toFixed(1)}s</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="prd" className="gap-2">
              <FileText className="w-4 h-4" />
              Product Requirements Document
            </TabsTrigger>
            <TabsTrigger value="mockup" className="gap-2">
              <Code className="w-4 h-4" />
              Interactive Mockup
            </TabsTrigger>
          </TabsList>

          {/* PRD Tab */}
          <TabsContent value="prd" className="space-y-4">
            <Card className="p-8 bg-card border border-border">
              <div className="prose prose-sm max-w-none dark:prose-invert">
                <MarkdownRenderer content={prdContent} />
              </div>
            </Card>
          </TabsContent>

          {/* Mockup Tab */}
          <TabsContent value="mockup" className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-foreground">
                Apple-Style Interactive Mockup
              </h2>
              <Button
                size="sm"
                variant="outline"
                onClick={() => setShowMockupPreview(!showMockupPreview)}
                className="gap-2"
              >
                {showMockupPreview ? <Code className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                {showMockupPreview ? "Show Code" : "Show Preview"}
              </Button>
            </div>

            {showMockupPreview ? (
              <Card className="border border-border overflow-hidden">
                <iframe
                  srcDoc={mockupContent}
                  className="w-full h-screen border-0"
                  title="Mockup Preview"
                  sandbox="allow-same-origin"
                />
              </Card>
            ) : (
              <Card className="p-6 bg-card border border-border">
                <pre className="bg-background p-4 rounded-lg overflow-auto max-h-96 text-xs font-mono text-foreground">
                  <code>{mockupContent}</code>
                </pre>
              </Card>
            )}
          </TabsContent>
        </Tabs>

        {/* Footer Info */}
        <div className="mt-12 p-6 bg-secondary bg-opacity-50 rounded-lg border border-border">
          <h3 className="font-semibold text-foreground mb-3">Next Steps</h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li className="flex gap-2">
              <span className="text-primary font-bold">•</span>
              <span>Download the PRD in Markdown format for further editing</span>
            </li>
            <li className="flex gap-2">
              <span className="text-primary font-bold">•</span>
              <span>Download the mockup HTML for integration into your design system</span>
            </li>
            <li className="flex gap-2">
              <span className="text-primary font-bold">•</span>
              <span>Share the mockup with stakeholders for feedback</span>
            </li>
            <li className="flex gap-2">
              <span className="text-primary font-bold">•</span>
              <span>Use the PRD as the foundation for your development roadmap</span>
            </li>
          </ul>
        </div>
      </main>
    </div>
  );
}
