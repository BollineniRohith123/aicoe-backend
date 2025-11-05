# AI Architecture Diagram Creation Guide

## Complete Guide to Creating Professional AI System Architecture Diagrams

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Diagram Philosophy](#architecture-diagram-philosophy)
3. [Document Structure](#document-structure)
4. [Section-by-Section Guide](#section-by-section-guide)
5. [Complete Examples](#complete-examples)
6. [Quick Reference Checklist](#quick-reference-checklist)

---

## Overview

### Purpose
This guide helps you create professional, comprehensive AI system architecture diagrams in HTML format based on Product Requirements Documents (PRDs) and AI design patterns. The focus is on **visual clarity, technical completeness, and professional presentation** suitable for executive stakeholders, technical teams, and implementation partners.

### Key Principles
- **Layered architecture visualization** - Clear separation of concerns
- **Modern minimalist design** - Clean, professional aesthetic
- **Lucide icons exclusively** - Consistent, recognizable iconography
- **Light theme enforcement** - Professional, accessible presentation
- **Technical completeness** - All components, flows, and specifications
- **Interactive elements** - Hover effects and responsive behaviors

### What This Template IS For
✅ Creating technical architecture diagrams from PRDs
✅ Visualizing AI/ML system components and data flows
✅ Presenting to technical and executive stakeholders
✅ Documentation for implementation teams
✅ Architecture reviews and approvals

### What This Template IS NOT For
❌ Detailed code-level diagrams
❌ Network topology diagrams
❌ Database schema diagrams only
❌ Infrastructure-only diagrams

---

## Architecture Diagram Philosophy

### Design Principles

#### 1. **Layered Architecture Approach**
All AI system architectures should follow a clear layered structure:
- **Presentation Layer** - User interfaces and touchpoints
- **Application Services Layer** - Business logic and services
- **AI/ML Intelligence Layer** - ML models and processing
- **Data Persistence Layer** - Databases and storage
- **Infrastructure & Edge Computing Layer** - Hardware and deployment

#### 2. **Visual Hierarchy**
- **Top-to-bottom flow** - Natural reading pattern
- **Consistent spacing** - 8px base unit (16px, 24px, 40px, 64px)
- **Color coding** - Different icon colors per layer
- **White space** - Generous padding for clarity

#### 3. **Component Organization**
- **Grid layouts** - Responsive auto-fit columns
- **Component cards** - Consistent card structure
- **Icon + Title + Description + Tech** - Standard component format
- **Hover interactions** - Visual feedback on interaction

---

## Document Structure

### HTML Architecture Diagram Overview

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Meta tags, Lucide CDN, CSS -->
</head>
<body>
    <div class="container">
        <header>
            <!-- Title and subtitle -->
        </header>

        <div class="architecture-diagram">
            <!-- Layered architecture -->
            <div class="layer"><!-- Presentation Layer --></div>
            <div class="data-flow"><!-- Flow arrow --></div>
            <div class="layer"><!-- Application Layer --></div>
            <div class="data-flow"><!-- Flow arrow --></div>
            <div class="layer"><!-- AI/ML Layer --></div>
            <div class="data-flow"><!-- Flow arrow --></div>
            <div class="layer"><!-- Data Layer --></div>
            <div class="data-flow"><!-- Flow arrow --></div>
            <div class="layer"><!-- Infrastructure Layer --></div>
        </div>

        <div class="technical-specs">
            <!-- Performance, Security, Accuracy, Scalability -->
        </div>

        <div class="integration-section">
            <!-- Key data flows -->
        </div>

        <div class="legend">
            <!-- Visual legend -->
        </div>

        <footer>
            <!-- Version and date -->
        </footer>
    </div>

    <script>
        // Initialize Lucide icons
        lucide.createIcons();
    </script>
</body>
</html>
```

---

## Section-by-Section Guide

---

## 1. HTML HEAD Section

### Purpose
Contains essential meta information, external dependencies, and CSS styling.

### Required Elements

#### Meta Tags
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[System Name] - AI Architecture</title>
```

#### Lucide Icon Library
**CRITICAL: Always use Lucide icons**
```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
```

#### CSS Styling Structure
The CSS must include:
1. **Reset and Base Styles** - Normalize across browsers
2. **Container and Layout** - Max-width 1200px, centered
3. **Typography** - Inter font family with fallbacks
4. **Color System** - Light theme colors only
5. **Component Styles** - Layers, components, cards
6. **Responsive Behavior** - Mobile, tablet, desktop
7. **Print Styles** - A4 portrait optimization

### Writing Guidance

**Font Stack:**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
```

**Color Palette (Light Theme Only):**
```css
Background-Primary: #FFFFFF
Background-Secondary: #F9FAFB
Text-Primary: #111827
Text-Secondary: #4B5563
Text-Tertiary: #6B7280
Primary-Blue: #2563EB
Border: #E5E7EB
Error-Red: #DC2626
Success-Green: #059669
Warning-Orange: #D97706
```

**Base Spacing:**
```css
Base unit: 8px
Small: 16px
Medium: 24px
Large: 32px
Extra-large: 40px
```

---

## 2. HEADER Section

### Purpose
Provides document title and subtitle context.

### Structure
```html
<header>
    <h1>[System Name]</h1>
    <p class="subtitle">[Architecture Description]</p>
</header>
```

### Writing Guidance

**Title:**
- System or product name
- Clear and descriptive
- 32px font size, 600 weight

**Subtitle:**
- Brief architecture description
- Highlight key capabilities
- 16px font size, secondary color

### Examples

**GOOD:**
```html
<header>
    <h1>Smart Retail Shopping Platform</h1>
    <p class="subtitle">AI-Powered Customer Recognition, Item Tracking & Seamless Checkout Architecture</p>
</header>
```

**AVOID:**
```html
<header>
    <h1>System</h1> <!-- Too vague -->
    <p class="subtitle">Architecture</p> <!-- Not descriptive -->
</header>
```

---

## 3. ARCHITECTURE LAYERS

### Layer Structure Template

Each layer follows this consistent structure:

```html
<div class="layer">
    <div class="layer-header">
        <i data-lucide="[icon-name]" class="layer-icon" width="24" height="24"></i>
        <h2 class="layer-title">[Layer Name]</h2>
    </div>
    <div class="components-grid">
        <!-- Component cards -->
    </div>
</div>
```

---

## 3.1 PRESENTATION LAYER

### Purpose
User-facing interfaces and touchpoints for all user types.

### Layer Icon
```html
<i data-lucide="monitor" class="layer-icon" width="24" height="24"></i>
```

### Layer Title
**"Presentation Layer"**

### Components to Include
Based on PRD **Information Architecture** and **User Interface** sections:

1. **Customer Mobile App**
   - Icon: `smartphone`
   - Description: Customer-facing mobile experience
   - Tech: React Native, WebSocket, Push Notifications

2. **Staff Tablet/Desktop Interface**
   - Icon: `tablet` or `monitor`
   - Description: Staff operational tools
   - Tech: Progressive Web App, Real-time Updates

3. **Manager Dashboard**
   - Icon: `layout-dashboard`
   - Description: Analytics and operations monitoring
   - Tech: React, D3.js, WebSocket

4. **Admin Portal** (if applicable)
   - Icon: `settings`
   - Description: System administration
   - Tech: React Admin, REST APIs

### Component Card Structure

```html
<div class="component">
    <div class="component-header">
        <i data-lucide="[icon]" width="20" height="20" style="color: #2563EB;"></i>
        <h3 class="component-title">[Component Name]</h3>
    </div>
    <p class="component-desc">[Brief description of capabilities]</p>
    <p class="component-tech">Tech: [Technology stack]</p>
</div>
```

### Icon Color
**Primary Blue (#2563EB)** for presentation layer

---

## 3.2 APPLICATION SERVICES LAYER

### Purpose
Business logic, orchestration, and service components.

### Layer Icon
```html
<i data-lucide="cpu" class="layer-icon" width="24" height="24"></i>
```

### Layer Title
**"Application Services Layer"**

### Components to Include
Based on PRD **Use Cases** and **Functional Requirements**:

1. **Core Business Services**
   - Customer Recognition Service
   - Item Tracking Service
   - Checkout Service
   - Payment Processing Service

2. **Supporting Services**
   - Analytics Service
   - Notification Service
   - Authentication Service
   - Integration Service

### Component Template

```html
<div class="component">
    <div class="component-header">
        <i data-lucide="[service-icon]" width="20" height="20" style="color: #059669;"></i>
        <h3 class="component-title">[Service Name]</h3>
    </div>
    <p class="component-desc">[Service capabilities and responsibilities]</p>
    <p class="component-tech">Tech: [Programming language, framework, architecture]</p>
</div>
```

### Common Service Icons
- `user-check` - Customer/User services
- `scan` - Scanning/Tracking services
- `shopping-cart` - E-commerce services
- `credit-card` - Payment services
- `bar-chart` - Analytics services
- `bell` - Notification services
- `shield` - Security services
- `database` - Data services

### Icon Color
**Success Green (#059669)** for application layer

---

## 3.3 AI/ML INTELLIGENCE LAYER

### Purpose
Machine learning models, processing engines, and AI capabilities.

### Layer Icon
```html
<i data-lucide="brain" class="layer-icon" width="24" height="24"></i>
```

### Layer Title
**"AI/ML Intelligence Layer"**

### Components to Include
Based on PRD **AI/ML Requirements** and **Design Patterns**:

1. **Computer Vision Components**
   - Face Recognition Engine
   - Object Detection Models
   - Image Classification
   - Scene Understanding

2. **Processing Components**
   - Real-time Stream Processing
   - Event Processing
   - Pattern Detection
   - Anomaly Detection

3. **Analytics Components**
   - Predictive Analytics
   - Recommendation Engine
   - Demand Forecasting
   - Behavior Analysis

4. **Supporting ML Components**
   - Model Training Pipeline
   - Model Serving Infrastructure
   - Feature Store
   - ML Monitoring

### Component Template

```html
<div class="component">
    <div class="component-header">
        <i data-lucide="[ml-icon]" width="20" height="20" style="color: #D97706;"></i>
        <h3 class="component-title">[ML Component Name]</h3>
    </div>
    <p class="component-desc">[ML capabilities and techniques]</p>
    <p class="component-tech">Tech: [ML frameworks, models, techniques]</p>
</div>
```

### Common ML Icons
- `eye` - Computer vision
- `brain` - Neural networks
- `activity` - Real-time processing
- `trending-up` - Predictive analytics
- `shield-check` - Fraud detection
- `zap` - Fast inference

### Icon Color
**Warning Orange (#D97706)** for AI/ML layer

### Technology Naming
Be specific about ML technologies:
- **Frameworks:** TensorFlow, PyTorch, Scikit-learn
- **Models:** YOLO, BERT, ResNet, Transformer
- **Processing:** Apache Kafka, Spark, Flink
- **Serving:** TensorFlow Serving, TorchServe

---

## 3.4 DATA PERSISTENCE LAYER

### Purpose
Databases, storage systems, and data management.

### Layer Icon
```html
<i data-lucide="database" class="layer-icon" width="24" height="24"></i>
```

### Layer Title
**"Data Persistence Layer"**

### Components to Include
Based on PRD **Data Requirements**:

1. **Relational Databases**
   - Customer Database
   - Transaction Store
   - Product Catalog

2. **NoSQL Databases**
   - Document Store
   - Key-Value Store
   - Time-Series Database

3. **Cache Layers**
   - Session Cache
   - Application Cache
   - CDN Cache

4. **Data Warehouses**
   - Analytics Data Warehouse
   - Business Intelligence Store

5. **Object Storage**
   - Media Storage
   - Archive Storage
   - Backup Storage

### Component Template

```html
<div class="component">
    <div class="component-header">
        <i data-lucide="[storage-icon]" width="20" height="20" style="color: #DC2626;"></i>
        <h3 class="component-title">[Storage Name]</h3>
    </div>
    <p class="component-desc">[Data stored and structure]</p>
    <p class="component-tech">Tech: [Database technology, features]</p>
</div>
```

### Common Storage Icons
- `users` - Customer/User data
- `receipt` - Transactional data
- `package` - Product/Inventory data
- `zap` - Cache/Fast storage
- `archive` - Data warehouse
- `image` - Media storage
- `hard-drive` - General storage

### Icon Color
**Error Red (#DC2626)** for data layer

### Technology Naming
Be specific about data technologies:
- **Relational:** PostgreSQL, MySQL, SQL Server
- **NoSQL:** MongoDB, Cassandra, DynamoDB
- **Cache:** Redis, Memcached
- **Warehouse:** Snowflake, BigQuery, Redshift
- **Object Storage:** AWS S3, Azure Blob, GCS

---

## 3.5 INFRASTRUCTURE & EDGE COMPUTING LAYER

### Purpose
Hardware, edge devices, cloud infrastructure, and deployment.

### Layer Icon
```html
<i data-lucide="server" class="layer-icon" width="24" height="24"></i>
```

### Layer Title
**"Infrastructure & Edge Computing"**

### Components to Include

1. **Edge Computing**
   - In-store Camera Networks
   - IoT Gateways
   - Edge AI Processors
   - Sensor Networks

2. **Cloud Infrastructure**
   - Container Orchestration
   - Serverless Functions
   - Auto-scaling Groups
   - Load Balancers

3. **Networking**
   - API Gateways
   - Message Queues
   - Service Mesh
   - CDN

### Component Template

```html
<div class="component">
    <div class="component-header">
        <i data-lucide="[infra-icon]" width="20" height="20" style="color: #6B7280;"></i>
        <h3 class="component-title">[Infrastructure Component]</h3>
    </div>
    <p class="component-desc">[Infrastructure capabilities]</p>
    <p class="component-tech">Tech: [Infrastructure technology]</p>
</div>
```

### Common Infrastructure Icons
- `video` - Cameras
- `wifi` - IoT/Networking
- `cloud` - Cloud infrastructure
- `server` - Servers
- `hard-drive` - Storage infrastructure

### Icon Color
**Tertiary Gray (#6B7280)** for infrastructure layer

---

## 4. DATA FLOW CONNECTORS

### Purpose
Visual separation between layers with directional flow indication.

### Structure
```html
<div class="data-flow">
    <div class="flow-arrow">
        <i data-lucide="arrow-down" width="20" height="20"></i>
        <span>[Layer/Protocol Description]</span>
        <i data-lucide="arrow-down" width="20" height="20"></i>
    </div>
</div>
```

### Common Flow Descriptions
- "API Gateway / Load Balancer"
- "Event Stream / Message Bus"
- "Data Access Layer"
- "Infrastructure Layer"
- "Network Layer"

### Styling
```css
.data-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 16px 0;
    color: #6B7280;
}
```

---

## 5. TECHNICAL SPECIFICATIONS Section

### Purpose
Quantitative technical requirements and targets.

### Structure
```html
<div class="technical-specs">
    <h2>Technical Specifications</h2>
    <div class="specs-grid">
        <div class="spec-card"><!-- Performance --></div>
        <div class="spec-card"><!-- Security --></div>
        <div class="spec-card"><!-- AI Accuracy --></div>
        <div class="spec-card"><!-- Scalability --></div>
    </div>
</div>
```

### Spec Card Template
```html
<div class="spec-card">
    <div class="spec-title">
        <i data-lucide="[icon]" width="20" height="20" style="color: #2563EB;"></i>
        [Specification Category]
    </div>
    <ul class="spec-list">
        <li>[Specific requirement or target]</li>
        <li>[Specific requirement or target]</li>
        <li>[Specific requirement or target]</li>
    </ul>
</div>
```

### Standard Specification Categories

#### 1. Performance Targets
**Icon:** `zap`
**Include:**
- Response time targets (< 100ms, < 2s, etc.)
- Throughput requirements (requests/sec)
- Latency requirements
- Availability targets (99.9%, 99.99%)

**Example:**
```html
<li>Item recognition latency < 100ms</li>
<li>Bill generation < 2 seconds</li>
<li>System availability > 99.9%</li>
```

#### 2. Security & Compliance
**Icon:** `shield`
**Include:**
- Encryption standards (AES-256, TLS 1.3)
- Compliance requirements (PCI DSS, GDPR, HIPAA)
- Authentication methods
- Data protection measures

**Example:**
```html
<li>AES-256 encryption at rest</li>
<li>TLS 1.3 for data in transit</li>
<li>PCI DSS Level 1 compliance</li>
<li>GDPR & CCPA compliant</li>
```

#### 3. AI Model Accuracy
**Icon:** `target`
**Include:**
- Model accuracy percentages
- Precision and recall targets
- False positive/negative rates
- Confidence thresholds

**Example:**
```html
<li>Customer recognition > 95%</li>
<li>Product identification > 98%</li>
<li>False positive rate < 2%</li>
```

#### 4. Scalability
**Icon:** `trending-up`
**Include:**
- Concurrent user capacity
- Data volume handling
- Geographic distribution
- Auto-scaling capabilities

**Example:**
```html
<li>Support 1000+ concurrent shoppers</li>
<li>Process 100+ items/second</li>
<li>Multi-region deployment ready</li>
```

---

## 6. DATA FLOW INTEGRATION Section

### Purpose
Illustrate key end-to-end workflows through the architecture.

### Structure
```html
<div class="integration-section">
    <h3 class="integration-title">Key Data Flows</h3>

    <div style="margin: 24px 0;">
        <h4>[Flow Name]</h4>
        <div class="integration-flow">
            <div class="integration-box">[Component 1]</div>
            <i data-lucide="arrow-right" width="20" height="20"></i>
            <div class="integration-box">[Component 2]</div>
            <i data-lucide="arrow-right" width="20" height="20"></i>
            <div class="integration-box">[Component 3]</div>
        </div>
    </div>
</div>
```

### Workflow Selection
Choose 3-5 critical workflows from PRD use cases:
- Primary user journeys
- Critical business processes
- Complex integrations
- High-value scenarios

### Example Workflows

**Customer Entry Flow:**
```
Camera Network → Recognition Service → Customer DB → Staff Notification
```

**Item Tracking Flow:**
```
Camera Network → Computer Vision → Item Tracking Service → Session Cache → Customer App
```

**Checkout Flow:**
```
Checkout Trigger → Bill Generation → Payment Service → Transaction Store → Receipt Delivery
```

---

## 7. LEGEND Section

### Purpose
Explain visual conventions and color coding.

### Structure
```html
<div class="legend">
    <h4 class="legend-title">Architecture Legend</h4>
    <div class="legend-items">
        <div class="legend-item">
            <div class="legend-color" style="background: #FFFFFF;"></div>
            <span>User-facing interfaces</span>
        </div>
        <!-- More legend items -->
    </div>
</div>
```

### Standard Legend Items
- Layer backgrounds and their meanings
- Icon color coding per layer
- Flow arrow meanings
- Special indicators (security, encryption, etc.)

---

## 8. FOOTER Section

### Purpose
Document metadata and version control.

### Structure
```html
<footer>
    <p>[System Name] - AI Architecture v[version]</p>
    <p>Generated: [Month Year] | Status: [Status]</p>
</footer>
```

### Status Options
- Concept Design
- In Review
- Approved
- Production-Ready Architecture
- Implemented

---

## Complete Example: Smart Retail Platform

See `/Users/srinivaskarri/Desktop/test/outputs/retail-shop-ai-architecture.html` for complete implementation.

### Key Architectural Decisions

**From PRD Analysis:**
1. **Use Cases** → Application Services
   - UC001: Customer Recognition → Customer Recognition Service
   - UC002: Item Tracking → Item Tracking Service
   - UC003: Checkout → Checkout Service + Payment Service

2. **UI/UX Requirements** → Presentation Layer
   - Customer Mobile App screens
   - Staff Tablet Interface screens
   - Manager Dashboard screens

3. **Data Requirements** → Data Persistence Layer
   - Customer data → Customer Database
   - Transaction data → Transaction Store
   - Product data → Product Catalog

4. **AI/ML Capabilities** → AI/ML Intelligence Layer
   - Computer vision requirements → Computer Vision Engine
   - Real-time processing → Stream Processing
   - Analytics needs → Predictive Analytics Engine

5. **Non-Functional Requirements** → Technical Specifications
   - Performance → Performance Targets card
   - Security → Security & Compliance card
   - Accuracy → AI Model Accuracy card
   - Scalability → Scalability card

---

## Design Pattern Integration

### Using Design Pattern Libraries

When a PRD references specific AI design patterns, integrate them into the architecture:

#### 1. Identify Pattern Components
Review the design pattern library for:
- Core components
- Integration points
- Technology stack recommendations
- Architecture layers

#### 2. Map Pattern to Architecture
- **Pattern presentation components** → Presentation Layer
- **Pattern business logic** → Application Services Layer
- **Pattern ML models** → AI/ML Intelligence Layer
- **Pattern data stores** → Data Persistence Layer
- **Pattern infrastructure** → Infrastructure Layer

#### 3. Integrate Pattern Specifications
- Use pattern performance targets
- Apply pattern security requirements
- Adopt pattern technology recommendations
- Follow pattern integration approaches

---

## Quick Reference Checklist

### Before You Start
- [ ] Read the complete PRD thoroughly
- [ ] Identify all use cases and requirements
- [ ] Review any referenced design patterns
- [ ] Understand the business domain
- [ ] Identify all user types and interfaces

### HTML Head Section
- [ ] UTF-8 charset meta tag
- [ ] Viewport meta tag
- [ ] Descriptive title
- [ ] Lucide icon CDN link
- [ ] Complete CSS styling (reset, layout, components, responsive)
- [ ] Light theme color palette
- [ ] Inter font family
- [ ] Print styles for A4

### Header Section
- [ ] Clear system name (H1, 32px)
- [ ] Descriptive subtitle
- [ ] Bottom border separator

### Architecture Layers
- [ ] Presentation Layer (monitor icon, #2563EB)
  - [ ] All user interfaces from PRD
  - [ ] Mobile, tablet, desktop components
  - [ ] Technology stack specified
- [ ] Data flow connector (arrow + label)
- [ ] Application Services Layer (cpu icon, #059669)
  - [ ] All services from use cases
  - [ ] Business logic components
  - [ ] Integration services
- [ ] Data flow connector
- [ ] AI/ML Intelligence Layer (brain icon, #D97706)
  - [ ] ML models and engines
  - [ ] Processing components
  - [ ] Analytics engines
- [ ] Data flow connector
- [ ] Data Persistence Layer (database icon, #DC2626)
  - [ ] All databases from data requirements
  - [ ] Cache layers
  - [ ] Storage systems
- [ ] Data flow connector
- [ ] Infrastructure Layer (server icon, #6B7280)
  - [ ] Edge computing
  - [ ] Cloud infrastructure
  - [ ] Networking components

### Component Cards
- [ ] Component header with icon
- [ ] Lucide icon (correct name, size, color)
- [ ] Component title (clear, descriptive)
- [ ] Component description (capabilities)
- [ ] Technology specification (specific tech names)
- [ ] Hover effect CSS
- [ ] Responsive grid layout

### Technical Specifications
- [ ] Performance Targets card (zap icon)
  - [ ] Latency requirements
  - [ ] Throughput targets
  - [ ] Availability targets
- [ ] Security & Compliance card (shield icon)
  - [ ] Encryption standards
  - [ ] Compliance requirements
  - [ ] Authentication methods
- [ ] AI Model Accuracy card (target icon)
  - [ ] Accuracy percentages
  - [ ] False positive rates
  - [ ] Confidence thresholds
- [ ] Scalability card (trending-up icon)
  - [ ] Concurrent user capacity
  - [ ] Data volume handling
  - [ ] Multi-region support

### Data Flow Integration
- [ ] 3-5 key workflows selected
- [ ] Workflow titles (H4)
- [ ] Integration boxes for each step
- [ ] Arrow icons between steps
- [ ] Accurate component names
- [ ] Logical flow sequence

### Legend
- [ ] Legend title
- [ ] Color coding explained
- [ ] Icon meanings
- [ ] Flow indicators
- [ ] Special symbols

### Footer
- [ ] System name and version
- [ ] Generation date (Month Year)
- [ ] Architecture status
- [ ] Professional formatting

### JavaScript
- [ ] Lucide icons initialization
- [ ] Script at end of body
- [ ] Correct syntax: `lucide.createIcons();`

### Final Validation
- [ ] All Lucide icons render correctly
- [ ] Responsive at mobile (320px), tablet (768px), desktop (1024px)
- [ ] Light theme throughout (no dark elements)
- [ ] Consistent spacing (8px base unit)
- [ ] No horizontal scrolling at any size
- [ ] Hover effects work smoothly
- [ ] Print layout works (A4 portrait)
- [ ] No broken images or icons
- [ ] All text legible and properly sized
- [ ] Professional visual appearance

---

## Common Mistakes to Avoid

### 1. Icon Problems
❌ **WRONG:**
```html
<i class="fa fa-database"></i> <!-- Font Awesome -->
<img src="icon.png"> <!-- Custom images -->
<span>📊</span> <!-- Emoji icons -->
```

✅ **CORRECT:**
```html
<i data-lucide="database" width="20" height="20" style="color: #DC2626;"></i>
```

### 2. Color Issues
❌ **WRONG:**
```css
background: #000000; /* Dark background */
background: linear-gradient(...); /* Gradients */
color: #FFFFFF; /* White text on white background */
```

✅ **CORRECT:**
```css
background: #FFFFFF; /* Light backgrounds */
background: #F9FAFB; /* Secondary light */
color: #111827; /* Dark text on light */
```

### 3. Component Structure
❌ **WRONG:**
```html
<div class="component">
    <h3>Service Name</h3> <!-- Missing icon -->
    <p>Description</p> <!-- No tech stack -->
</div>
```

✅ **CORRECT:**
```html
<div class="component">
    <div class="component-header">
        <i data-lucide="cpu" width="20" height="20" style="color: #059669;"></i>
        <h3 class="component-title">Service Name</h3>
    </div>
    <p class="component-desc">Description of capabilities</p>
    <p class="component-tech">Tech: Python, FastAPI, Docker</p>
</div>
```

### 4. Vague Technology Names
❌ **WRONG:**
```
Tech: Database, Cloud, ML Model
```

✅ **CORRECT:**
```
Tech: PostgreSQL 14, AWS RDS, Encrypted Fields
Tech: Kubernetes, Docker, AWS EKS
Tech: TensorFlow 2.x, YOLO v8, TensorRT
```

### 5. Missing Layers
❌ **WRONG:**
- Only showing Presentation + Database
- Skipping AI/ML layer for AI systems
- No infrastructure layer

✅ **CORRECT:**
- All 5 layers present
- AI/ML layer for AI systems
- Complete stack visualization

---

## Responsive Design Requirements

### Breakpoints
```css
Mobile: 320px - 767px
Tablet: 768px - 1023px
Desktop: 1024px - 1440px
Wide: 1441px+
```

### Component Grid Behavior
```css
/* Mobile: 1 column */
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));

/* Tablet: 2 columns */
grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));

/* Desktop: 3-4 columns */
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
```

### Typography Scaling
- H1: 32px (desktop), 28px (mobile)
- H2: 24px (desktop), 20px (mobile)
- H3: 20px (desktop), 18px (mobile)
- Body: 16px (all devices)
- Small: 14px (all devices)
- Caption: 12px (all devices)

---

## Print Optimization

### Page Setup
```css
@media print {
    @page {
        size: A4 portrait;
        margin: 20mm;
    }

    body {
        padding: 0;
        font-size: 10pt;
    }

    .component:hover {
        transform: none; /* Disable hover in print */
    }

    /* Avoid page breaks inside components */
    .component, .spec-card {
        page-break-inside: avoid;
    }
}
```

---

## Accessibility Requirements

### WCAG 2.1 AA Compliance
- [ ] Text contrast ratio ≥ 4.5:1
- [ ] UI component contrast ≥ 3:1
- [ ] Semantic HTML structure
- [ ] Alt text for icons (via aria-label)
- [ ] Keyboard navigation support
- [ ] Focus indicators visible
- [ ] Heading hierarchy logical (H1 → H2 → H3)

### Icon Accessibility
```html
<i data-lucide="database"
   width="20"
   height="20"
   aria-label="Database storage"
   role="img"></i>
```

---

## Version Control and Updates

### Version Numbering
- **v1.0** - Initial architecture design
- **v1.1** - Minor updates (component additions)
- **v2.0** - Major revisions (layer changes)

### Change Log Format
```html
<!--
Version 1.1 - November 2025
- Added Analytics Service to Application Layer
- Updated AI/ML accuracy targets
- Enhanced security specifications

Version 1.0 - October 2025
- Initial architecture design
- All 5 layers defined
- Technical specifications established
-->
```

---

## Final Validation Questions

Before publishing your architecture diagram, ask:

1. **Completeness:** Does the diagram show all components from the PRD?
2. **Accuracy:** Are all technology names and specifications correct?
3. **Clarity:** Can a non-technical executive understand the layers?
4. **Consistency:** Do all components follow the same card structure?
5. **Icons:** Are all icons from Lucide and properly colored?
6. **Flows:** Are the data flows logical and complete?
7. **Specifications:** Are technical specs quantitative and realistic?
8. **Responsive:** Does it work on mobile, tablet, and desktop?
9. **Light Theme:** Is the light theme enforced throughout?
10. **Professional:** Does it look polished and ready for stakeholders?

If you answered "no" to any question, revise before publishing.

---

## Additional Resources

### Lucide Icon Reference
Browse all available icons: https://lucide.dev/icons/

### Recommended Icons by Layer

**Presentation Layer:**
- monitor, smartphone, tablet, layout-dashboard, users, user

**Application Services:**
- cpu, server, cog, settings, user-check, scan, shopping-cart, credit-card, bell, bar-chart

**AI/ML Intelligence:**
- brain, eye, activity, trending-up, shield-check, zap, sparkles

**Data Persistence:**
- database, hard-drive, archive, image, receipt, package, users, zap (cache)

**Infrastructure:**
- server, cloud, wifi, video, network, globe

**Data Flows:**
- arrow-down, arrow-right, arrow-up, move-horizontal, move-vertical

---

## Conclusion

This guide provides a comprehensive framework for creating professional AI architecture diagrams that effectively communicate complex system designs to both technical and executive audiences. By following these guidelines, your architecture diagrams will be:

- **Visually consistent** with professional design standards
- **Technically complete** with all necessary components
- **Easy to understand** with clear layering and flows
- **Ready for implementation** with specific technology choices
- **Suitable for stakeholders** at all levels

Remember: **Clarity, completeness, and professionalism first. Technical accuracy always.**

---

**Document Version:** 1.0
**Last Updated:** 2025-11-04
**Based on:** retail-shop-ai-architecture.html example
**Related Guides:** 01-guide-use-case-writing.md, 02-guide-prd-writing.md
