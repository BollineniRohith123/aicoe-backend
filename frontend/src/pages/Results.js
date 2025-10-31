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

  const useCases = result.results?.requirements?.use_cases || [];
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
            <div className="flex gap-2 flex-wrap">
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
                PRD (MD)
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  if (projectId) {
                    downloadArtifact(projectId, "prd_pdf", `${projectName}-PRD.pdf`);
                  } else {
                    alert("PDF download only available for saved projects");
                  }
                }}
                className="gap-2"
              >
                <Download className="w-4 h-4" />
                PRD (PDF)
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
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  if (projectId) {
                    downloadArtifact(projectId, "commercial_proposal", `${projectName}-Proposal.md`);
                  } else {
                    downloadFile(proposalContent, `${projectName}-Proposal.md`, "text/markdown");
                  }
                }}
                className="gap-2"
              >
                <Download className="w-4 h-4" />
                Proposal (MD)
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  if (projectId) {
                    downloadArtifact(projectId, "commercial_proposal_pdf", `${projectName}-Proposal.pdf`);
                  } else {
                    alert("PDF download only available for saved projects");
                  }
                }}
                className="gap-2"
              >
                <Download className="w-4 h-4" />
                Proposal (PDF)
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  if (projectId) {
                    downloadArtifact(projectId, "bom_json", `${projectName}-BOM.json`);
                  } else {
                    downloadFile(JSON.stringify(bomData, null, 2), `${projectName}-BOM.json`, "application/json");
                  }
                }}
                className="gap-2"
              >
                <Download className="w-4 h-4" />
                BOM (JSON)
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  if (projectId) {
                    downloadArtifact(projectId, "bom_pdf", `${projectName}-BOM.pdf`);
                  } else {
                    alert("PDF download only available for saved projects");
                  }
                }}
                className="gap-2"
              >
                <Download className="w-4 h-4" />
                BOM (PDF)
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  if (projectId) {
                    downloadArtifact(projectId, "architecture_diagram", `${projectName}-Architecture.html`);
                  } else {
                    downloadFile(architectureContent, `${projectName}-Architecture.html`, "text/html");
                  }
                }}
                className="gap-2"
              >
                <Download className="w-4 h-4" />
                Architecture
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

        {/* Use Cases Display */}
        <div className="space-y-6">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-foreground mb-2">Interactive Use Cases</h2>
            <p className="text-muted-foreground">Explore your project requirements through interactive mockups</p>
          </div>

          {useCases.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {useCases.map((useCase, index) => (
                <Card key={index} className="p-6 hover:shadow-lg transition-shadow">
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-xl font-semibold text-foreground mb-2">
                        {useCase.title || `Use Case ${index + 1}`}
                      </h3>
                      <p className="text-muted-foreground text-sm">
                        {useCase.description || "No description available"}
                      </p>
                    </div>

                    {useCase.primaryActor && (
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-foreground">Primary Actor:</span>
                        <span className="text-sm text-muted-foreground">{useCase.primaryActor}</span>
                      </div>
                    )}

                    <Button
                      className="w-full gap-2"
                      onClick={() => {
                        // Open the corresponding mockup in a new tab
                        const mockupUrl = projectId
                          ? `${API_BASE_URL}/api/download/${projectId}/mockup/use-case-${index + 1}.html`
                          : "#"; // Fallback for demo
                        if (mockupUrl !== "#") {
                          window.open(mockupUrl, '_blank');
                        } else {
                          alert("Mockup preview only available for saved projects");
                        }
                      }}
                    >
                      <Eye className="w-4 h-4" />
                      View Interactive Mockup
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          ) : (
            <Card className="p-8 text-center">
              <p className="text-muted-foreground">No use cases available</p>
            </Card>
          )}
        </div>

        {/* Footer Info */}
        <div className="mt-12 p-6 bg-secondary bg-opacity-50 rounded-lg border border-border">
          <h3 className="font-semibold text-foreground mb-3">Next Steps</h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li className="flex gap-2">
              <span className="text-primary font-bold">•</span>
              <span>Explore each use case by clicking "View Interactive Mockup"</span>
            </li>
            <li className="flex gap-2">
              <span className="text-primary font-bold">•</span>
              <span>Download all deliverables from the header download buttons</span>
            </li>
            <li className="flex gap-2">
              <span className="text-primary font-bold">•</span>
              <span>Share mockups with stakeholders for immediate feedback</span>
            </li>
            <li className="flex gap-2">
              <span className="text-primary font-bold">•</span>
              <span>Use the generated artifacts as the foundation for development</span>
            </li>
          </ul>
        </div>
      </main>
    </div>
  );
}
