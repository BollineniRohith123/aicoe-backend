import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  ArrowRight,
  Zap,
  FileText,
  Palette,
  Workflow,
  Clock,
  Shield,
  Users,
  CheckCircle,
  Star,
  TrendingUp,
  Globe
} from "lucide-react";
import { APP_LOGO, APP_TITLE } from "@/const";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border bg-card/95 backdrop-blur-sm sticky top-0 z-50">
        <div className="container py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            {APP_LOGO && (
              <img src={APP_LOGO} alt="Logo" className="w-8 h-8 rounded" />
            )}
            <h1 className="text-xl font-bold text-foreground">{APP_TITLE}</h1>
          </div>
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              onClick={() => navigate("/input")}
              className="text-muted-foreground hover:text-foreground"
            >
              Try Demo
            </Button>
            <Button
              onClick={() => navigate("/input")}
              className="bg-primary hover:bg-primary/90 text-primary-foreground gap-2"
            >
              Get Started
              <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container py-20 md:py-32">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-accent/10 text-accent rounded-full text-sm font-semibold border border-accent/20">
            <Star className="w-4 h-4" />
            Multi-Agent AI Platform v1.0
          </div>
          <h1 className="text-5xl md:text-7xl font-bold text-foreground leading-tight">
            Transform Meeting
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-accent to-primary animate-gradient">
              {" "}Transcripts
            </span>
            <br />
            Into Professional Deliverables
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Automate your product development workflow with AI-powered agents that convert
            meeting transcripts into comprehensive PRDs, interactive mockups, and technical
            specifications in under 30 minutes.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
            <Button
              size="lg"
              onClick={() => navigate("/input")}
              className="bg-primary hover:bg-primary/90 text-primary-foreground gap-2 text-lg px-8 py-6"
            >
              Start Processing Now
              <ArrowRight className="w-5 h-5" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => navigate("/input")}
              className="gap-2 text-lg px-8 py-6 border-2 hover:bg-accent/5"
            >
              <Clock className="w-5 h-5" />
              See Demo
            </Button>
          </div>
          <div className="flex items-center justify-center gap-8 pt-8 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-500" />
              <span>No credit card required</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-500" />
              <span>Free for first 5 transcripts</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-500" />
              <span>30-minute SLA</span>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="container py-16 md:py-24 border-t border-border">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-3xl md:text-4xl font-bold text-primary mb-2">500+</div>
            <div className="text-muted-foreground">Transcripts Processed</div>
          </div>
          <div>
            <div className="text-3xl md:text-4xl font-bold text-primary mb-2">30min</div>
            <div className="text-muted-foreground">Average Processing Time</div>
          </div>
          <div>
            <div className="text-3xl md:text-4xl font-bold text-primary mb-2">95%</div>
            <div className="text-muted-foreground">Accuracy Rate</div>
          </div>
          <div>
            <div className="text-3xl md:text-4xl font-bold text-primary mb-2">24/7</div>
            <div className="text-muted-foreground">AI Agent Availability</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container py-16 md:py-24">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-6">
              Enterprise-Grade AI Agents
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Powered by advanced multi-agent orchestration inspired by Google ADK architecture,
              delivering professional-grade deliverables with unmatched quality and speed.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <Card className="p-8 border border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg group">
              <div className="flex items-start gap-4">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary to-primary/80 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <Zap className="w-7 h-7 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-foreground mb-3">
                    Intelligent Multi-Agent System
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Specialized AI agents collaborate seamlessly: Transcript analysis, Requirements extraction,
                    PRD generation, Mockup creation, and Quality assurance - all working in perfect harmony.
                  </p>
                </div>
              </div>
            </Card>

            {/* Feature 2 */}
            <Card className="p-8 border border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg group">
              <div className="flex items-start gap-4">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-accent to-accent/80 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <FileText className="w-7 h-7 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-foreground mb-3">
                    Comprehensive PRDs
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Generate detailed Product Requirements Documents with 15+ structured sections,
                    including user stories, acceptance criteria, technical specifications, and implementation timelines.
                  </p>
                </div>
              </div>
            </Card>

            {/* Feature 3 */}
            <Card className="p-8 border border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg group">
              <div className="flex items-start gap-4">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary/60 to-accent/60 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <Palette className="w-7 h-7 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-foreground mb-3">
                    Apple-Style Mockups
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Create beautiful, interactive HTML mockups with modern design principles,
                    responsive layouts, and professional UI components that match industry standards.
                  </p>
                </div>
              </div>
            </Card>

            {/* Feature 4 */}
            <Card className="p-8 border border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg group">
              <div className="flex items-start gap-4">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-accent/80 to-primary/60 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <Workflow className="w-7 h-7 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-foreground mb-3">
                    End-to-End Automation
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Complete workflow automation from transcript upload to downloadable artifacts,
                    with real-time progress tracking and instant notifications.
                  </p>
                </div>
              </div>
            </Card>

            {/* Feature 5 */}
            <Card className="p-8 border border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg group">
              <div className="flex items-start gap-4">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary/40 to-accent flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <Shield className="w-7 h-7 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-foreground mb-3">
                    Enterprise Security
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Bank-level security with end-to-end encryption, SOC 2 compliance,
                    and secure data handling ensuring your sensitive information stays protected.
                  </p>
                </div>
              </div>
            </Card>

            {/* Feature 6 */}
            <Card className="p-8 border border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg group">
              <div className="flex items-start gap-4">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-accent to-primary/80 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <Globe className="w-7 h-7 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-foreground mb-3">
                    Global Scale
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Deploy anywhere with cloud-native architecture supporting multi-region deployment,
                    auto-scaling, and 99.9% uptime SLA for mission-critical workflows.
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="container py-16 md:py-24 bg-accent/5">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-6">
              How It Works
            </h2>
            <p className="text-xl text-muted-foreground">
              Four simple steps to transform your meeting transcripts into professional deliverables
            </p>
          </div>

          <div className="space-y-12">
            {/* Step 1 */}
            <div className="flex flex-col md:flex-row gap-8 items-center">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-16 w-16 rounded-2xl bg-gradient-to-br from-primary to-primary/80 text-white font-bold text-2xl shadow-lg">
                  1
                </div>
              </div>
              <div className="flex-1 text-center md:text-left">
                <h3 className="text-2xl font-semibold text-foreground mb-3">
                  Upload Your Transcript
                </h3>
                <p className="text-muted-foreground text-lg leading-relaxed">
                  Simply paste your meeting transcript or upload a file. Our system accepts any text format
                  and automatically detects the content structure for optimal processing.
                </p>
              </div>
            </div>

            {/* Step 2 */}
            <div className="flex flex-col md:flex-row gap-8 items-center">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-16 w-16 rounded-2xl bg-gradient-to-br from-accent to-accent/80 text-white font-bold text-2xl shadow-lg">
                  2
                </div>
              </div>
              <div className="flex-1 text-center md:text-left">
                <h3 className="text-2xl font-semibold text-foreground mb-3">
                  AI Agent Processing
                </h3>
                <p className="text-muted-foreground text-lg leading-relaxed">
                  Our specialized AI agents analyze your transcript, extract key requirements, identify use cases,
                  and collaborate to generate comprehensive deliverables with enterprise-grade quality.
                </p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="flex flex-col md:flex-row gap-8 items-center">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-16 w-16 rounded-2xl bg-gradient-to-br from-primary/80 to-accent text-white font-bold text-2xl shadow-lg">
                  3
                </div>
              </div>
              <div className="flex-1 text-center md:text-left">
                <h3 className="text-2xl font-semibold text-foreground mb-3">
                  Review & Refine
                </h3>
                <p className="text-muted-foreground text-lg leading-relaxed">
                  Preview your generated PRD and interactive HTML mockup with syntax highlighting.
                  Make any necessary adjustments before finalizing your deliverables.
                </p>
              </div>
            </div>

            {/* Step 4 */}
            <div className="flex flex-col md:flex-row gap-8 items-center">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-16 w-16 rounded-2xl bg-gradient-to-br from-accent/80 to-primary text-white font-bold text-2xl shadow-lg">
                  4
                </div>
              </div>
              <div className="flex-1 text-center md:text-left">
                <h3 className="text-2xl font-semibold text-foreground mb-3">
                  Download & Deploy
                </h3>
                <p className="text-muted-foreground text-lg leading-relaxed">
                  Download your complete package (PRD.md, Mockup.html, requirements.json) and share
                  with your team. Ready for immediate implementation and stakeholder review.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="container py-16 md:py-24">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-12">
            Trusted by Product Teams Worldwide
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="p-6 text-center">
              <div className="flex justify-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                ))}
              </div>
              <p className="text-muted-foreground mb-4 italic">
                "Cut our product documentation time from 3 days to 30 minutes. The AI agents
                understand context better than our junior PMs."
              </p>
              <div className="font-semibold">Sarah Chen</div>
              <div className="text-sm text-muted-foreground">VP Product, TechCorp</div>
            </Card>
            <Card className="p-6 text-center">
              <div className="flex justify-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                ))}
              </div>
              <p className="text-muted-foreground mb-4 italic">
                "The mockups are production-ready. We've launched 12 features using AICOE
                outputs with zero design revisions needed."
              </p>
              <div className="font-semibold">Marcus Johnson</div>
              <div className="text-sm text-muted-foreground">Design Director, InnovateLab</div>
            </Card>
            <Card className="p-6 text-center">
              <div className="flex justify-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                ))}
              </div>
              <p className="text-muted-foreground mb-4 italic">
                "ROI was achieved in the first month. What used to take a week of meetings
                and documentation now happens automatically."
              </p>
              <div className="font-semibold">Elena Rodriguez</div>
              <div className="text-sm text-muted-foreground">CTO, StartupXYZ</div>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container py-16 md:py-24">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-gradient-to-r from-primary via-accent to-primary p-12 md:p-16 text-center text-white relative overflow-hidden">
            <div className="absolute inset-0 bg-black/10"></div>
            <div className="relative z-10">
              <h2 className="text-3xl md:text-5xl font-bold mb-6">
                Ready to Transform Your Product Development?
              </h2>
              <p className="text-white/90 text-xl mb-8 max-w-2xl mx-auto">
                Join hundreds of product teams who have accelerated their workflows with AI-powered automation.
                Start your free trial today and see the difference in minutes.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button
                  size="lg"
                  onClick={() => navigate("/input")}
                  className="bg-white text-primary hover:bg-white/90 gap-2 text-lg px-8 py-6 font-semibold"
                >
                  Start Free Trial
                  <ArrowRight className="w-5 h-5" />
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  onClick={() => navigate("/input")}
                  className="border-white text-white hover:bg-white/10 gap-2 text-lg px-8 py-6"
                >
                  <TrendingUp className="w-5 h-5" />
                  View Demo
                </Button>
              </div>
              <div className="mt-6 text-white/80 text-sm">
                No credit card required • 14-day free trial • Cancel anytime
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-card mt-16">
        <div className="container py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-semibold text-foreground mb-4">{APP_TITLE}</h3>
              <p className="text-muted-foreground text-sm">
                Enterprise-grade AI automation for product development teams.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground">Features</a></li>
                <li><a href="#" className="hover:text-foreground">Pricing</a></li>
                <li><a href="#" className="hover:text-foreground">API</a></li>
                <li><a href="#" className="hover:text-foreground">Integrations</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground">About</a></li>
                <li><a href="#" className="hover:text-foreground">Blog</a></li>
                <li><a href="#" className="hover:text-foreground">Careers</a></li>
                <li><a href="#" className="hover:text-foreground">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground">Documentation</a></li>
                <li><a href="#" className="hover:text-foreground">Help Center</a></li>
                <li><a href="#" className="hover:text-foreground">Status</a></li>
                <li><a href="#" className="hover:text-foreground">Community</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-border pt-8 text-center text-muted-foreground text-sm">
            <p>
              &copy; 2025 {APP_TITLE}. Built with advanced AI agent orchestration technology.
              All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
