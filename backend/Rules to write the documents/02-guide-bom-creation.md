# Bill of Materials Creation Guide

## Complete Guide to Creating Cloud Infrastructure BOM from Architecture Documents

---

## Table of Contents

1. [Overview](#overview)
2. [Document Structure](#document-structure)
3. [Section-by-Section Guide](#section-by-section-guide)
4. [Complete Example](#complete-example)
5. [Quick Reference Checklist](#quick-reference-checklist)

---

## Overview

### Purpose
This guide helps you create comprehensive Bill of Materials (BOM) documents that map technical architecture components to specific cloud provider services with accurate cost estimates and procurement details.

### Key Principles
- **Architecture-to-Service Mapping**: Direct mapping between architecture layers and cloud services
- **Cost Transparency**: Clear cost estimates with multiple pricing models
- **Procurement Readiness**: Include SKUs, service IDs, and procurement metrics
- **Scalability Planning**: Document scaling scenarios and cost implications
- **Vendor Specificity**: Use official cloud provider service names and identifiers

### What This Template IS For
✅ Mapping architecture components to cloud services
✅ Providing accurate cost estimates with SKUs
✅ Supporting procurement and budgeting decisions
✅ Planning capacity and scaling requirements
✅ Documenting service dependencies and integrations

### What This Template IS NOT For
❌ Detailed technical implementation specifications
❌ Network topology and infrastructure design
❌ Application code or deployment scripts
❌ Security configuration details
❌ Operational runbooks and procedures

---

## Document Structure

### HTML Format Overview

A BOM document consists of these major sections:

1. **Header & Summary**: Title, overview, cost summary
2. **Architecture Reference**: Link to source architecture document
3. **Layer Mapping Sections**: Services organized by architecture layer
4. **Cost Summary**: Detailed cost breakdown and total estimates
5. **Scaling Scenarios**: Different deployment scales with costs
6. **Notes & Assumptions**: Important considerations and caveats

---

## Section-by-Section Guide

---

## 1. HEADER & SUMMARY Section

### Purpose
Provides immediate overview of the BOM including total services and estimated costs.

### Structure
```html
<header>
    <h1>[Project Name]</h1>
    <p class="subtitle">[Cloud Provider] - Bill of Materials</p>
    <p>Architecture-to-Cloud Services Mapping with Cost Estimates</p>
</header>

<div class="summary-cards">
    <div class="summary-card">
        <div class="summary-label">Total [Cloud] Services</div>
        <div class="summary-value">[Number]</div>
    </div>
    <!-- Additional summary cards -->
</div>
```

### Writing Guidance

| Field | How to Write | Purpose |
|-------|-------------|---------|
| **Project Name** | Exact name from architecture document | Ensures traceability |
| **Cloud Provider** | Full official name (e.g., Oracle Cloud Infrastructure, AWS) | Clear vendor identification |
| **Total Services** | Count of unique services mapped | Shows scope |
| **Estimated Cost** | Monthly recurring cost in dollars | Budget planning |
| **Deployment Scale** | Small/Medium/Large/Enterprise | Context for sizing |

### Examples

**GOOD:**
```html
<h1>Smart Retail Shopping Platform</h1>
<p class="subtitle">Oracle Cloud Infrastructure (OCI) - Bill of Materials</p>

<div class="summary-cards">
    <div class="summary-card">
        <div class="summary-label">Total OCI Services</div>
        <div class="summary-value">28</div>
        <div class="summary-detail">IaaS, PaaS, AI/ML</div>
    </div>
    <div class="summary-card">
        <div class="summary-label">Estimated Monthly Cost</div>
        <div class="summary-value">$12.5K</div>
        <div class="summary-detail">Medium-scale deployment</div>
    </div>
</div>
```

**AVOID:**
```html
<h1>Project BOM</h1> <!-- Too vague -->
<p class="subtitle">Cloud Services</p> <!-- Which cloud? -->
<div class="summary-value">Many</div> <!-- Not specific -->
<div class="summary-value">Expensive</div> <!-- Not quantified -->
```

---

## 2. ARCHITECTURE REFERENCE Section

### Purpose
Links the BOM to the source architecture document for traceability and context.

### Structure
```html
<div class="architecture-link">
    <i data-lucide="file-text" class="architecture-link-icon"></i>
    <div class="architecture-link-text">
        <div class="architecture-link-title">Reference Architecture Document</div>
        <div class="architecture-link-desc">This BOM maps to: [filename.html]</div>
    </div>
</div>
```

### Writing Guidance

**Requirements:**
- Include exact filename of architecture document
- Provide brief description of what's being mapped
- Make it visually distinct for easy reference
- Consider making it a clickable link if applicable

### Example

**GOOD:**
```html
<div class="architecture-link">
    <i data-lucide="file-text"></i>
    <div class="architecture-link-text">
        <div class="architecture-link-title">Reference Architecture Document</div>
        <div class="architecture-link-desc">
            This BOM maps to: retail-shop-ai-architecture.html
            <br>Architecture: AI-Powered Customer Recognition, Item Tracking & Seamless Checkout
        </div>
    </div>
</div>
```

---

## 3. LAYER MAPPING SECTIONS

### Purpose
Maps each architecture layer to specific cloud services with detailed procurement information.

### Structure
```html
<div class="layer-section">
    <div class="layer-header">
        <i data-lucide="[icon]" class="layer-icon"></i>
        <h2 class="layer-title">[Layer Name]</h2>
    </div>

    <div class="mapping-info">
        <div class="mapping-info-title">Architecture Mapping</div>
        <div class="mapping-info-text">
            [Architecture Components] → [Cloud Services]
        </div>
    </div>

    <table class="services-table">
        <thead>
            <tr>
                <th>Cloud Service</th>
                <th>Service ID</th>
                <th>Use Case</th>
                <th>Metric</th>
                <th>Est. Monthly Cost</th>
            </tr>
        </thead>
        <tbody>
            <!-- Service rows -->
        </tbody>
    </table>
</div>
```

### Writing Guidance

#### Layer Header
**How to Write:**
- Use exact layer name from architecture document
- Choose appropriate icon that represents the layer
- Match icon style with architecture document

**Layer Organization Examples:**
- Presentation Layer
- Application Services Layer
- AI/ML Intelligence Layer
- Data Persistence Layer
- Infrastructure & Edge Computing Layer
- Security & Governance Layer
- Observability & Monitoring Layer

#### Architecture Mapping Box
**How to Write:**
- List architecture components on left side of arrow
- List cloud services on right side of arrow
- Use clear, concise component names
- Format: `[Component A, Component B, Component C] → [Cloud Service Category]`

**Examples:**

✅ **GOOD:**
```
Architecture Mapping:
Customer Recognition, Item Tracking, Checkout Services → OCI Compute + Kubernetes
```

```
Architecture Mapping:
Computer Vision Engine, Stream Processing, Predictive Analytics → OCI AI Services + GPU Compute
```

❌ **AVOID:**
```
Architecture Mapping:
Stuff → Cloud Things
```

```
Architecture Mapping:
See architecture document for details
```

#### Service Table Rows

**Required Columns:**

1. **Cloud Service Name**
   - Use official cloud provider service name
   - Full name, not abbreviations (except well-known ones)
   - Examples: "Container Engine (OKE)", "Autonomous Database - ATP"

2. **Service ID / SKU**
   - Official SKU or service identifier from cloud provider
   - Format as badge: `<span class="sku-badge">OCI-COMP-001</span>`
   - Must be verifiable in provider documentation

3. **Use Case**
   - Brief description of what this service does in your architecture
   - 5-15 words maximum
   - Focus on business/technical purpose
   - Examples: "Kubernetes orchestration for microservices", "Customer profiles, product catalog (OLTP)"

4. **Metric**
   - Specific unit of measurement for billing
   - Include quantity estimated
   - Format as badge: `<span class="metric-badge">24 OCPU x 730 hrs</span>`
   - Examples: "4 ECPU x 730 hrs", "1M images/month", "500 GB storage"

5. **Estimated Monthly Cost**
   - Dollar amount per month
   - Format as: "$X,XXX/month" or "Free" or "Included"
   - Style with cost-estimate class
   - Round to reasonable precision ($13, not $12.87)

### Complete Table Example

**GOOD:**
```html
<table class="services-table">
    <thead>
        <tr>
            <th>OCI Service</th>
            <th>Service ID</th>
            <th>Use Case</th>
            <th>Metric</th>
            <th>Est. Monthly Cost</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="service-name">Container Engine (OKE)</td>
            <td><span class="sku-badge">OCI-DEV-005</span></td>
            <td>Kubernetes orchestration for microservices</td>
            <td><span class="metric-badge">Control plane (free)</span></td>
            <td class="cost-estimate">$0/month</td>
        </tr>
        <tr>
            <td class="service-name">Autonomous Database - ATP</td>
            <td><span class="sku-badge">OCI-DB-002</span></td>
            <td>Customer profiles, product catalog (OLTP)</td>
            <td><span class="metric-badge">4 ECPU x 730 hrs</span></td>
            <td class="cost-estimate">$2,336/month</td>
        </tr>
        <tr>
            <td class="service-name">Vision Service</td>
            <td><span class="sku-badge">OCI-AI-006</span></td>
            <td>Customer recognition, product identification</td>
            <td><span class="metric-badge">1M images/month</span></td>
            <td class="cost-estimate">$1,500/month</td>
        </tr>
    </tbody>
</table>
```

**AVOID:**
```html
<tbody>
    <tr>
        <td>Database</td> <!-- Too vague -->
        <td>DB-001</td> <!-- Not official SKU -->
        <td>Stores data</td> <!-- Not specific -->
        <td>Some</td> <!-- Not quantified -->
        <td>$$$</td> <!-- Not precise -->
    </tr>
</tbody>
```

---

## 4. COST SUMMARY Section

### Purpose
Provides comprehensive cost breakdown by category and total estimated costs.

### Structure
```html
<div class="cost-summary">
    <div class="cost-summary-title">Monthly Cost Breakdown</div>

    <div class="cost-breakdown">
        <div class="cost-item">
            <div class="cost-item-header">[Category Name]</div>
            <div class="cost-detail">
                <span class="cost-label">[Service Name]</span>
                <span class="cost-value">$X,XXX</span>
            </div>
            <!-- More cost details -->
        </div>
        <!-- More cost items -->
    </div>

    <div class="total-cost">
        <div class="total-cost-label">Estimated Total Monthly Cost</div>
        <div class="total-cost-value">$XX,XXX/month</div>
        <div class="total-cost-detail">≈ $XXX,XXX/year at [Pricing Model]</div>
    </div>
</div>
```

### Writing Guidance

#### Cost Categories
**Organize costs by logical groupings:**
- Infrastructure Services (Compute, Storage, Network)
- AI/ML Services
- Database Services
- Platform Services (Integration, API, etc.)
- Security & Compliance
- Observability & Monitoring

#### Cost Detail Format
**Each line item should include:**
- Clear service name or category
- Monthly cost amount
- Format with proper currency symbols and commas

#### Total Cost Section
**Requirements:**
- Display prominently with distinct styling
- Show monthly total
- Calculate and show annual total
- Indicate which pricing model (PAYG, committed, etc.)

### Example

**GOOD:**
```html
<div class="cost-summary">
    <div class="cost-summary-title">
        <i data-lucide="dollar-sign"></i>
        Monthly Cost Breakdown
    </div>

    <div class="cost-breakdown">
        <div class="cost-item">
            <div class="cost-item-header">Infrastructure Services</div>
            <div class="cost-detail">
                <span class="cost-label">Compute (OKE Workers)</span>
                <span class="cost-value">$1,752</span>
            </div>
            <div class="cost-detail">
                <span class="cost-label">Storage (Block/Object/Archive)</span>
                <span class="cost-value">$97</span>
            </div>
            <div class="cost-detail">
                <span class="cost-label">Network (LB + FastConnect)</span>
                <span class="cost-value">$306</span>
            </div>
        </div>

        <div class="cost-item">
            <div class="cost-item-header">AI/ML Services</div>
            <div class="cost-detail">
                <span class="cost-label">Vision Service</span>
                <span class="cost-value">$1,500</span>
            </div>
            <div class="cost-detail">
                <span class="cost-label">GPU Compute (H100)</span>
                <span class="cost-value">$2,552</span>
            </div>
        </div>
    </div>

    <div class="total-cost">
        <div class="total-cost-label">Estimated Total Monthly Cost (PAYG)</div>
        <div class="total-cost-value">$12,462/month</div>
        <div class="total-cost-detail">≈ $149,544/year at Pay-As-You-Go rates</div>
    </div>
</div>
```

#### Cost Optimization Section

**Include pricing model comparisons:**

```html
<div style="background: #FFFFFF; padding: 20px;">
    <div style="font-size: 18px; font-weight: 600; margin-bottom: 16px;">
        Cost Optimization with [Commitment Model]
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px;">
        <div>
            <div style="font-size: 14px; color: #6B7280;">Annual Commitment (34% savings)</div>
            <div style="font-size: 24px; font-weight: 600; color: #059669;">$8,225/month</div>
            <div style="font-size: 12px; color: #6B7280;">≈ $98,700/year (save $50,844)</div>
        </div>
        <!-- Additional pricing models -->
    </div>
</div>
```

---

## 5. SCALING SCENARIOS Section

### Purpose
Documents how costs change with different deployment scales and usage patterns.

### Structure
```html
<div class="layer-section">
    <div class="layer-header">
        <i data-lucide="trending-up" class="layer-icon"></i>
        <h2 class="layer-title">Scaling Scenarios</h2>
    </div>

    <table class="services-table">
        <thead>
            <tr>
                <th>Deployment Scale</th>
                <th>Usage Volume</th>
                <th>Compute Scaling</th>
                <th>Est. Monthly Cost</th>
                <th>Use Case</th>
            </tr>
        </thead>
        <tbody>
            <!-- Scaling scenarios -->
        </tbody>
    </table>
</div>
```

### Writing Guidance

**Define 3-5 scaling tiers:**
- **Small/Pilot**: Initial deployment, proof of concept
- **Medium/Production**: Standard production deployment
- **Large/Multi-Site**: Enterprise deployment across locations
- **Enterprise/Global**: Large-scale, high-volume deployment

**For each tier specify:**
- Business usage volume (transactions, users, etc.)
- Technical resources (OCPU, GPU, storage)
- Estimated monthly cost
- Typical use case description

### Example

**GOOD:**
```html
<tbody>
    <tr>
        <td class="service-name">Small (Pilot)</td>
        <td>100-500 shoppers/day</td>
        <td>12 OCPU, 2 GPU (100 hrs)</td>
        <td class="cost-estimate">$6,500/month</td>
        <td>Single store pilot, proof of concept</td>
    </tr>
    <tr>
        <td class="service-name">Medium (Production)</td>
        <td>500-2000 shoppers/day</td>
        <td>24 OCPU, 2 GPU (200 hrs)</td>
        <td class="cost-estimate">$12,462/month</td>
        <td>Single large store or 2-3 medium stores</td>
    </tr>
    <tr>
        <td class="service-name">Large (Multi-Store)</td>
        <td>2000-5000 shoppers/day</td>
        <td>48 OCPU, 4 GPU (400 hrs)</td>
        <td class="cost-estimate">$24,800/month</td>
        <td>5-10 stores, regional deployment</td>
    </tr>
    <tr>
        <td class="service-name">Enterprise</td>
        <td>5000+ shoppers/day</td>
        <td>96+ OCPU, 8+ GPU (730 hrs)</td>
        <td class="cost-estimate">$48,000+/month</td>
        <td>National chain, 20+ stores</td>
    </tr>
</tbody>
```

---

## 6. NOTES & ASSUMPTIONS Section

### Purpose
Documents important caveats, assumptions, and considerations for cost estimates.

### Structure
```html
<div class="notes-section">
    <div class="notes-title">
        <i data-lucide="info"></i>
        Important Notes & Assumptions
    </div>
    <ul class="notes-list">
        <li>[Assumption or note]</li>
        <li>[Another important consideration]</li>
        <!-- More notes -->
    </ul>
</div>
```

### Writing Guidance

**Include notes about:**
- Pricing sources and date ("Based on [Provider] pricing as of [Date]")
- Usage assumptions ("Costs assume 70% average utilization")
- Free tier benefits ("First 10TB outbound data transfer free")
- Optional components ("Edge computing marked as optional")
- Support costs ("Enterprise support included at no extra charge")
- Regional considerations ("Consistent pricing across all regions")
- Commitment models ("Annual commitment provides 34% savings")
- Data transfer costs ("Inbound free, outbound after 10TB at $X/GB")
- Disaster recovery ("Multi-region DR adds ~50% to infrastructure")
- Compliance requirements ("[Compliance standard] configured")

### Example

**GOOD:**
```html
<div class="notes-section">
    <div class="notes-title">
        <i data-lucide="info"></i>
        Important Notes & Assumptions
    </div>
    <ul class="notes-list">
        <li><strong>Cost Estimates:</strong> Based on OCI pricing as of November 2025. Actual costs may vary based on usage patterns and commitment levels.</li>

        <li><strong>Auto-Scaling:</strong> Compute resources configured for auto-scaling based on demand. Costs shown assume 70% average utilization.</li>

        <li><strong>Free Tier:</strong> Some services offer always-free tier (e.g., first 10TB outbound data transfer, IAM, Cloud Guard). Not all free benefits are itemized.</li>

        <li><strong>Edge Computing:</strong> On-premises edge processing marked as optional. Cloud-only deployment possible with camera stream processing in OCI.</li>

        <li><strong>Data Transfer:</strong> Inbound data transfer is free. First 10TB/month outbound is free. Additional transfer at $0.0085/GB not included in estimates.</li>

        <li><strong>Support Costs:</strong> Enterprise support included with OCI at no extra charge. Support Rewards program provides 25-33% credits back.</li>

        <li><strong>PCI DSS Compliance:</strong> Data Safe service configured for PCI DSS requirements. Additional compliance certifications may require consulting services.</li>

        <li><strong>Disaster Recovery:</strong> Multi-region DR adds approximately 50% to infrastructure costs. Not included in base estimates.</li>

        <li><strong>GPU Usage:</strong> GPU costs based on training 200 hours/month. Production inference may use lower-cost CPU or optimized instances.</li>

        <li><strong>Regional Pricing:</strong> OCI offers consistent global pricing. No regional price variations unlike other cloud providers.</li>
    </ul>
</div>
```

---

## 7. SERVICE IDENTIFICATION Best Practices

### How to Map Architecture to Cloud Services

#### Step 1: Analyze Architecture Document
1. Read the full architecture document
2. Identify all distinct architecture layers
3. List all components within each layer
4. Note component purposes and requirements

#### Step 2: Consult Cloud Provider Inventory
1. Open cloud provider service catalog
2. Search for services matching component requirements
3. Note official service names and SKUs
4. Verify service capabilities match needs

#### Step 3: Create Mapping Table
For each architecture component, document:
- Architecture layer name
- Component name and purpose
- Mapped cloud service(s)
- Service ID/SKU
- Justification for mapping choice

#### Example Mapping Process

**Architecture Component:**
```
Layer: AI/ML Intelligence Layer
Component: Computer Vision Engine
Purpose: Face recognition, product identification, image preprocessing
Requirements: GPU acceleration, model serving, high throughput
```

**Mapping Research:**
```
Cloud Provider: Oracle Cloud Infrastructure

Option 1: OCI Vision Service (OCI-AI-006)
- Managed service for image analysis
- Pre-built models + custom models
- Pay per transaction
- Cost: ~$1.50 per 1000 images

Option 2: GPU Compute (OCI-COMP-005) + Custom Models
- Full control over models
- NVIDIA H100 instances
- Pay per hour
- Cost: $6.38/GPU-hour

Decision: Use both services
- OCI Vision Service for standard recognition (cost-effective)
- GPU instances for custom model training and fine-tuning
```

**Final BOM Entry:**
```html
<tr>
    <td class="service-name">Vision Service</td>
    <td><span class="sku-badge">OCI-AI-006</span></td>
    <td>Customer recognition, product identification</td>
    <td><span class="metric-badge">1M images/month</span></td>
    <td class="cost-estimate">$1,500/month</td>
</tr>
<tr>
    <td class="service-name">GPU Instances - H100</td>
    <td><span class="sku-badge">OCI-COMP-005</span></td>
    <td>Custom ML model training and inference</td>
    <td><span class="metric-badge">2 GPU x 200 hrs</span></td>
    <td class="cost-estimate">$2,552/month</td>
</tr>
```

---

## 8. COST CALCULATION Best Practices

### Determining Realistic Cost Estimates

#### Method 1: Usage-Based Calculation

**For compute resources:**
```
Monthly Cost = (Units × Hours per Month × Rate per Hour)

Example:
24 OCPU × 730 hours × $0.10/OCPU-hour = $1,752/month
```

**For storage resources:**
```
Monthly Cost = (Storage GB × Rate per GB-month)

Example:
500 GB × $0.0255/GB-month = $13/month
```

**For transaction-based services:**
```
Monthly Cost = (Transactions per Month × Rate per Transaction)

Example:
1,000,000 images × $0.0015/image = $1,500/month
```

#### Method 2: Vendor Pricing Calculators
1. Use official cloud provider pricing calculators
2. Input realistic usage estimates
3. Document assumptions used
4. Export or screenshot results
5. Reference in BOM notes

#### Method 3: Reference Architectures
1. Find similar reference architectures from vendor
2. Adjust for your specific scale
3. Apply multipliers for differences
4. Document deviations from reference

### Usage Estimation Guidelines

**For new deployments:**
- Start with conservative estimates
- Include 20-30% buffer for spikes
- Base on similar system metrics if available
- Use vendor sizing guidelines

**For existing systems:**
- Analyze current resource utilization
- Add 20-30% growth factor
- Account for migration inefficiencies
- Consider performance improvements

### Cost Ranges and Precision

**Appropriate precision by cost level:**
- $0-$10: Round to $1 ($3, $7, $9)
- $10-$100: Round to $5 ($15, $45, $95)
- $100-$1000: Round to $10 ($130, $450, $980)
- $1000+: Round to $50 or $100 ($1,500, $3,200, $12,500)

**Use ranges when appropriate:**
- "Variable pricing" for highly dynamic usage
- "$X-$Y" for tiered or usage-dependent costs
- "Starting at $X" when minimum exists

---

## Complete Example

### Retail Shop AI - OCI Bill of Materials

**Context:**
- Architecture: Smart Retail Shopping Platform
- Cloud Provider: Oracle Cloud Infrastructure (OCI)
- Scale: Medium production deployment
- Services: 28 OCI services across 7 layers

**Key BOM Elements:**

1. **Header & Summary**
   - Total: 28 OCI services
   - Cost: $12,462/month (PAYG)
   - Scale: Medium (500-2000 shoppers/day)
   - Savings: 34% with Annual UC

2. **Layer Mappings**
   - Presentation → 4 services ($125/month)
   - Application → 6 services ($1,941/month)
   - AI/ML → 5 services ($4,142/month)
   - Data → 6 services ($6,111/month)
   - Infrastructure → 4 services ($853/month)
   - Security → 6 services ($316/month)
   - Observability → 5 services ($362/month)

3. **Scaling Scenarios**
   - Small: $6,500/month (pilot)
   - Medium: $12,462/month (production)
   - Large: $24,800/month (multi-store)
   - Enterprise: $48,000+/month (national)

4. **Cost Optimization**
   - PAYG: $12,462/month
   - Annual UC (34% off): $8,225/month
   - 3-Year UC (50% off): $6,231/month
   - Support Rewards: +$3,115/month credits

---

## Quick Reference Checklist

### Before You Start

- [ ] Read the complete architecture document
- [ ] Identify all architecture layers and components
- [ ] Access cloud provider service catalog/inventory
- [ ] Have cloud provider pricing information available
- [ ] Understand the deployment scale and usage patterns
- [ ] Know the budget constraints or targets

### Header & Summary

- [ ] Project name matches architecture document
- [ ] Cloud provider clearly identified
- [ ] Total service count is accurate
- [ ] Cost estimate includes timeframe (monthly)
- [ ] Deployment scale is specified
- [ ] Summary cards provide quick overview

### Architecture Reference

- [ ] Source architecture document name included
- [ ] Link or file path provided
- [ ] Brief description of architecture provided
- [ ] Visually distinct for easy reference

### For Each Layer Mapping

- [ ] Layer name matches architecture document
- [ ] Appropriate icon selected
- [ ] Architecture mapping clearly shows component → service
- [ ] Table includes all required columns
- [ ] Service names are official cloud provider names
- [ ] SKUs/Service IDs are correct and verifiable
- [ ] Use cases are specific and clear (5-15 words)
- [ ] Metrics show quantity and units
- [ ] Costs are realistic and properly formatted
- [ ] All architecture components are mapped

### Service Table Rows

- [ ] Service name is official (not abbreviated incorrectly)
- [ ] SKU matches cloud provider inventory
- [ ] Use case describes role in architecture
- [ ] Metric shows quantity × unit × time period
- [ ] Cost is monthly estimate rounded appropriately
- [ ] Free services marked as "Free" or "Included"
- [ ] Optional services clearly indicated

### Cost Summary

- [ ] Costs organized by logical categories
- [ ] Each category has clear header
- [ ] Individual line items add up correctly
- [ ] Total monthly cost is prominent
- [ ] Annual cost calculated (monthly × 12)
- [ ] Pricing model specified (PAYG, committed, etc.)
- [ ] Cost optimization section included
- [ ] Multiple pricing models compared
- [ ] Savings percentages calculated

### Scaling Scenarios

- [ ] 3-5 scaling tiers defined
- [ ] Each tier shows usage volume
- [ ] Compute/resource scaling quantified
- [ ] Costs estimated for each tier
- [ ] Use cases described for each tier
- [ ] Tiers represent realistic deployment sizes
- [ ] Linear or economies of scale reflected

### Notes & Assumptions

- [ ] Pricing source and date documented
- [ ] Usage assumptions clearly stated
- [ ] Free tier benefits noted
- [ ] Optional components identified
- [ ] Support cost policy stated
- [ ] Regional pricing considerations noted
- [ ] Commitment model savings explained
- [ ] Data transfer costs addressed
- [ ] Disaster recovery impact noted
- [ ] Compliance requirements documented
- [ ] At least 8-10 important notes included

### Visual Design

- [ ] Professional, clean layout
- [ ] Consistent color scheme (light theme)
- [ ] Icons from Lucide library
- [ ] Tables are readable and well-formatted
- [ ] Cost figures are prominently displayed
- [ ] SKU badges are styled consistently
- [ ] Metric badges are visually distinct
- [ ] Print-friendly (if applicable)
- [ ] Responsive design for different screens

### Footer

- [ ] Document title and version
- [ ] Generation date
- [ ] Link to official cloud pricing
- [ ] Contact information (if applicable)

---

## Validation Questions

Before finalizing your BOM, ask yourself:

1. **Completeness:** Have I mapped every component from the architecture?
2. **Accuracy:** Are all SKUs/Service IDs correct and verifiable?
3. **Cost Realism:** Are my cost estimates based on real pricing data?
4. **Traceability:** Can someone trace each service back to architecture component?
5. **Procurement Ready:** Does this contain enough detail for procurement?
6. **Scalability:** Have I addressed how costs change with scale?
7. **Clarity:** Would someone unfamiliar with the project understand this?
8. **Optimization:** Have I documented cost optimization opportunities?
9. **Assumptions:** Are all my assumptions clearly stated?
10. **Maintainability:** Can this be updated when pricing changes?

If you answered "no" to any question, revise that section before finalizing.

---

## Common Mistakes to Avoid

### 1. Using Generic Service Names
❌ **WRONG:** "Database Service"
✅ **CORRECT:** "Autonomous Database - Transaction Processing (ATP)"

### 2. Missing or Incorrect SKUs
❌ **WRONG:** "DB-001" (made up)
✅ **CORRECT:** "OCI-DB-002" (verified from inventory)

### 3. Vague Use Cases
❌ **WRONG:** "Data storage"
✅ **CORRECT:** "Customer profiles, product catalog (OLTP workload)"

### 4. Unquantified Metrics
❌ **WRONG:** "Some CPUs"
✅ **CORRECT:** "24 OCPU × 730 hours"

### 5. Unrealistic Costs
❌ **WRONG:** "$100/month" for enterprise database
✅ **CORRECT:** "$2,336/month" (4 ECPU × 730 hrs × $0.80)

### 6. Missing Free Services
❌ **WRONG:** Omitting services because they're free
✅ **CORRECT:** Include with "$0/month" or "Free"

### 7. Ignoring Scaling
❌ **WRONG:** Only one cost estimate
✅ **CORRECT:** Multiple scaling scenarios with costs

### 8. Undocumented Assumptions
❌ **WRONG:** No notes about how costs were calculated
✅ **CORRECT:** Detailed assumptions and sources in notes

### 9. No Cost Optimization
❌ **WRONG:** Only PAYG pricing shown
✅ **CORRECT:** Multiple commitment models compared

### 10. Broken Architecture Link
❌ **WRONG:** No reference to source architecture
✅ **CORRECT:** Clear link to architecture document

---

## Best Practices

### 1. Work Layer by Layer
- Complete one architecture layer at a time
- Verify all components mapped before moving to next
- Keep architecture document open for reference

### 2. Verify Every SKU
- Cross-reference with official cloud provider inventory
- Check that capabilities match requirements
- Note any discrepancies or alternatives

### 3. Document Your Math
- Show calculations for costs
- Reference pricing sources
- Note any assumptions or estimates

### 4. Use Official Pricing
- Always use current official pricing
- Include pricing date in notes
- Link to pricing calculator or price list

### 5. Think About Scale
- Consider growth trajectory
- Model different usage patterns
- Show how costs scale

### 6. Plan for Optimization
- Research commitment discounts
- Identify reserved instance opportunities
- Document cost-saving strategies

### 7. Be Conservative
- Add buffers for unexpected usage
- Account for growth
- Include contingency in estimates

### 8. Keep It Updated
- Note when pricing was checked
- Plan to review quarterly
- Track actual vs estimated costs

---

## Template Usage Tips

### Getting Started
1. **Start with architecture:** Review architecture document thoroughly
2. **List all components:** Create spreadsheet of all architecture components
3. **Research services:** Match each component to cloud service(s)
4. **Gather pricing:** Collect current pricing for all identified services
5. **Calculate costs:** Estimate usage and calculate monthly costs
6. **Build BOM:** Transfer information to BOM HTML template
7. **Review:** Validate completeness and accuracy
8. **Share:** Distribute for stakeholder review and approval

### Maintaining the BOM
- **Quarterly reviews:** Check for pricing changes
- **Architecture updates:** Revise when architecture changes
- **Actual cost tracking:** Compare estimates to real costs
- **Optimization reviews:** Look for new savings opportunities
- **Version control:** Track changes with version numbers and dates

### Using for Procurement
- **Extract SKU list:** Create procurement-ready SKU list
- **Quantity summary:** Aggregate quantities by service
- **Timeline:** Add procurement timeline and milestones
- **Approvals:** Include approval workflow
- **Vendor engagement:** Use as basis for vendor discussions

---

## Conclusion

This guide provides a comprehensive framework for creating accurate, procurement-ready Bill of Materials documents that map technical architecture to cloud provider services. By following these guidelines, you'll create BOM documents that:

- Provide clear traceability from architecture to services
- Include accurate cost estimates with proper documentation
- Support procurement and budgeting decisions
- Scale appropriately for different deployment sizes
- Remain maintainable as pricing and architecture evolve

Remember: **Accuracy and verifiability are paramount. Always use official service names, verified SKUs, and current pricing data.**

---

**Document Version:** 1.0
**Last Updated:** 2025-11-04
**Based on:** retail-shop-ai-bom.html (Reference Implementation)