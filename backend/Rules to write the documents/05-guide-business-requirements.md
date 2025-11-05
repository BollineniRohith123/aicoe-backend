# Guide to Writing Business Requirements

## Table of Contents
1. [Overview](#overview)
2. [Purpose and Definition](#purpose-and-definition)
3. [Structure](#structure)
4. [Writing Guidelines](#writing-guidelines)
5. [Quality Checklist](#quality-checklist)
6. [Examples](#examples)
7. [Best Practices](#best-practices)
8. [Common Pitfalls](#common-pitfalls)
9. [Attributes Reference](#attributes-reference)

---

## Overview

Business Requirements (BR) are the foundation of the software development process. They articulate **what** the business needs to achieve and **why**, focusing on user goals, business objectives, and the value delivered.

### Document Hierarchy
```
Business Requirements (BR)
    ↓ maps to
Functional Requirements (FR)
    ↓ maps to
Test Cases (TC)
```

### Naming Convention
- **Format**: BR1, BR2, BR3, BR4, ...
- **Rule**: Each Business Requirement must have a unique identifier
- **Best Practice**: Never reuse IDs, even for deleted requirements
- **Project-specific**: Consider prefixes for different projects (e.g., PROJ1-BR1)

---

## Purpose and Definition

### What is a Business Requirement?

A Business Requirement defines a high-level business need or objective that the system must fulfill. It describes:
- **What** needs to be accomplished
- **Why** it's important to the business
- **Who** will benefit from it
- **How** success will be measured

### What Business Requirements Are NOT

Business Requirements should NOT include:
- Technical implementation details
- Specific technologies or platforms
- User interface designs
- Detailed system behaviors (those belong in Functional Requirements)

### Key Characteristics

Good Business Requirements are:
1. **Outcome-oriented** - Focus on results, not methods
2. **Measurable** - Include quantifiable success criteria
3. **User-centric** - Consider end-user goals
4. **Business-aligned** - Tie to organizational objectives
5. **Technology-agnostic** - Avoid implementation details
6. **Traceable** - Can be linked to FRs and tested

---

## Structure

Each Business Requirement should include the following components:

```markdown
**BR[#]: [Clear, Concise Requirement Title]**

- **Description**: Clear statement of the business need (2-3 sentences)
- **Business Goal**: What the organization aims to achieve
- **User Goal**: What the end user wants to accomplish
- **Success Criteria**: Measurable outcomes that define success (minimum 2-3 criteria)
- **Priority**: High / Medium / Low
- **Stakeholder**: Who requested/owns this requirement (name and role)
```

### Component Descriptions

**Title**
- Brief, action-oriented phrase (5-10 words)
- Starts with a verb when possible
- Examples: "Enable Customer Self-Service", "Improve Order Processing Speed"

**Description**
- Provides context and background
- Explains the need or problem being addressed
- Should be understandable by non-technical stakeholders

**Business Goal**
- Organizational objective or benefit
- May include cost savings, revenue increase, efficiency gains
- Ties to company strategy or KPIs

**User Goal**
- End-user perspective
- What the user wants to accomplish
- Should reflect user research or feedback

**Success Criteria**
- Specific, measurable, achievable metrics
- Minimum 2-3 quantifiable criteria
- Should include targets (percentages, time frames, volumes)
- Examples: "30% reduction in support calls", "95% user satisfaction"

**Priority**
- **High**: Critical for initial release, high business value
- **Medium**: Important but can be phased
- **Low**: Nice-to-have, future enhancement

**Stakeholder**
- Name and role of the person who owns this requirement
- Primary point of contact for questions
- Decision-maker for changes

---

## Writing Guidelines

### 1. Focus on the "What" and "Why", Not the "How"

**Good Example:**
```markdown
**BR1: Enable Real-Time Inventory Visibility**

- **Description**: Sales and warehouse teams need accurate, up-to-date inventory
  information to prevent overselling and improve order fulfillment
- **Business Goal**: Reduce order cancellations by 40% and improve customer
  satisfaction
- **User Goal**: Check current stock levels instantly to make informed decisions
```

**Bad Example:**
```markdown
**BR1: Implement WebSocket API for Inventory Updates**

- **Description**: The system needs to use WebSocket connections to push inventory
  updates to the client application every 5 seconds
- **Business Goal**: Build a real-time system using React and Node.js
```
*Why it's bad: Specifies technical implementation (WebSocket, React, Node.js) instead of business need*

### 2. Be Outcome-Oriented

Focus on the desired result, not the activity.

**Good Example:**
```markdown
**Business Goal**: Increase customer retention by 25% through improved self-service capabilities
**User Goal**: Resolve common issues independently without waiting for support
```

**Bad Example:**
```markdown
**Business Goal**: Build a help center with 50 articles
**User Goal**: Read documentation
```
*Why it's bad: Describes the activity (building, reading) not the outcome (retention, issue resolution)*

### 3. Use Business Language

Write for business stakeholders, not technical teams.

**Good Example:**
```markdown
**BR3: Reduce Order Processing Time**

- **Description**: Orders currently take 2-3 days to process, causing customer
  dissatisfaction and lost sales. Streamlining the process will improve competitiveness.
```

**Bad Example:**
```markdown
**BR3: Optimize Database Queries and Implement Caching**

- **Description**: Current SQL queries have O(n²) complexity and need Redis caching
  to improve performance.
```

### 4. Make It Measurable

Include specific, quantifiable success criteria.

**Good Example:**
```markdown
**Success Criteria**:
  - Order processing time reduced from 48 hours to 4 hours
  - 90% of orders processed without manual intervention
  - Customer satisfaction score increases from 3.2 to 4.5 out of 5
  - Support tickets related to order status decrease by 60%
```

**Bad Example:**
```markdown
**Success Criteria**:
  - Orders process faster
  - Customers are happier
  - Less support work
```

### 5. Keep It Concise

One clear objective per Business Requirement.

**Good Example:**
```markdown
**BR5: Enable Multi-Currency Pricing**

- **Description**: International customers need to view prices in their local currency
  to reduce purchase friction
```

**Bad Example:**
```markdown
**BR5: Enable Multi-Currency Pricing, Tax Calculation, International Shipping,
and Localized Content**
```
*Why it's bad: Combines multiple distinct requirements that should be separate BRs*

### 6. Ensure Uniqueness

Each BR should be distinct and not overlap significantly with others.

**Good Example:**
- BR7: Enable Order Tracking for Customers
- BR8: Provide Real-Time Delivery Notifications
- BR9: Allow Order Modifications Before Shipment

**Bad Example:**
- BR7: Improve Order Experience
- BR8: Enhance Customer Order Management
- BR9: Better Order Handling
*Why it's bad: Too vague and likely overlap significantly*

---

## Quality Checklist

Before finalizing a Business Requirement, verify:

- [ ] **Does it describe a business need or user goal?**
  - Not a technical solution or implementation detail

- [ ] **Is it free from technical implementation details?**
  - No mentions of specific technologies, architectures, or designs

- [ ] **Can success be measured?**
  - Includes specific, quantifiable success criteria

- [ ] **Is it clearly understood by non-technical stakeholders?**
  - Uses business language, avoids technical jargon

- [ ] **Does it provide clear value to the business or user?**
  - Articulates ROI, user benefit, or strategic alignment

- [ ] **Is it a single, focused objective?**
  - Not combining multiple distinct needs

- [ ] **Is it uniquely identified?**
  - Has a unique BR# that won't be reused

- [ ] **Is there a clear stakeholder owner?**
  - Someone accountable for this requirement

- [ ] **Is the priority clearly defined?**
  - High/Medium/Low based on business value and urgency

- [ ] **Is it traceable?**
  - Can be linked to functional requirements and test cases

---

## Examples

### Example 1: E-Commerce Platform

```markdown
**BR1: Enable Customer Self-Service Account Management**

- **Description**: Customers currently must contact support to update their
  account information, leading to high support costs and customer frustration.
  Enabling self-service will improve efficiency and satisfaction.
- **Business Goal**: Reduce customer support costs by 30% and improve customer
  satisfaction scores
- **User Goal**: Update personal information, view order history, and manage
  preferences independently without contacting support
- **Success Criteria**:
  - 70% of account updates performed by customers without support intervention
  - Customer satisfaction score increases from 3.8 to 4.5 out of 5
  - Support tickets related to account management decrease by 30%
  - Self-service adoption rate reaches 60% within 3 months
- **Priority**: High
- **Stakeholder**: Sarah Chen, Customer Success Director
```

### Example 2: Healthcare System

```markdown
**BR2: Improve Patient Appointment Scheduling Efficiency**

- **Description**: Patients experience long wait times on phone to schedule
  appointments, and clinic staff spend 40% of their time on scheduling tasks.
  Streamlining the process will improve patient experience and staff productivity.
- **Business Goal**: Reduce scheduling-related calls by 50% and free up 20 hours
  per week of staff time for patient care
- **User Goal**: Book, reschedule, or cancel appointments at any time without
  calling the clinic
- **Success Criteria**:
  - 60% of appointments booked through self-service within 6 months
  - Average appointment booking time reduced from 8 minutes to 2 minutes
  - No-show rate decreases from 15% to 8% (due to automated reminders)
  - Patient satisfaction with scheduling increases by 35%
- **Priority**: High
- **Stakeholder**: Dr. Michael Roberts, Chief Medical Officer
```

### Example 3: Financial Services

```markdown
**BR3: Enhance Fraud Detection Capabilities**

- **Description**: Current fraud detection relies on manual review, causing delays
  in transaction processing and missed fraud cases. Enhanced detection will protect
  customers and reduce financial losses.
- **Business Goal**: Reduce fraud losses by $2M annually while decreasing false
  positive rate to minimize customer friction
- **User Goal**: Complete legitimate transactions quickly without unnecessary
  security delays or blocks
- **Success Criteria**:
  - Fraud detection rate increases from 85% to 95%
  - False positive rate decreases from 12% to 5%
  - Average transaction processing time remains under 2 seconds
  - Customer complaints about blocked transactions decrease by 40%
  - Fraud-related financial losses decrease by $2M per year
- **Priority**: High
- **Stakeholder**: Jennifer Martinez, Chief Risk Officer
```

### Example 4: Manufacturing System

```markdown
**BR4: Enable Predictive Maintenance for Production Equipment**

- **Description**: Unplanned equipment downtime costs $50K per incident and
  disrupts production schedules. Predictive maintenance will reduce downtime
  and maintenance costs.
- **Business Goal**: Reduce unplanned downtime by 60% and decrease maintenance
  costs by $200K annually
- **User Goal**: (Maintenance Team) Receive advance notice of potential equipment
  failures to schedule maintenance during planned downtime
- **Success Criteria**:
  - Unplanned downtime incidents reduced from 20 to 8 per year
  - 80% of equipment failures predicted at least 48 hours in advance
  - Overall equipment effectiveness (OEE) increases from 75% to 85%
  - Maintenance costs decrease by $200K annually
  - Mean time between failures (MTBF) increases by 40%
- **Priority**: High
- **Stakeholder**: Tom Anderson, VP of Operations
```

### Example 5: Educational Platform

```markdown
**BR5: Personalize Learning Paths for Students**

- **Description**: Students have diverse learning styles and pace, but current
  one-size-fits-all approach results in 35% course abandonment. Personalized
  paths will improve engagement and completion.
- **Business Goal**: Increase course completion rate from 65% to 85% and improve
  student outcomes
- **User Goal**: (Student) Progress through material at my own pace with content
  adapted to my learning style and knowledge gaps
- **Success Criteria**:
  - Course completion rate increases from 65% to 85%
  - Average student assessment scores increase by 15%
  - Student engagement time increases by 25%
  - Student satisfaction rating increases from 3.9 to 4.6 out of 5
  - Course abandonment rate decreases from 35% to 15%
- **Priority**: Medium
- **Stakeholder**: Dr. Lisa Wang, Chief Academic Officer
```

---

## Best Practices

### 1. Start with Discovery

Before writing Business Requirements:
- **Conduct stakeholder interviews** - Understand business objectives and pain points
- **Research user needs** - User interviews, surveys, analytics
- **Analyze current state** - Document existing processes and metrics
- **Review business strategy** - Align requirements with organizational goals
- **Benchmark competitors** - Understand market expectations

### 2. Engage Stakeholders Early

- **Identify key stakeholders** - Decision-makers, end users, technical leads
- **Conduct workshops** - Collaborative requirements gathering sessions
- **Validate assumptions** - Confirm understanding of business needs
- **Prioritize together** - Business value vs. effort discussions
- **Get formal sign-off** - Written approval before moving to functional requirements

### 3. Use the Right Level of Detail

Business Requirements should be:
- **High-level enough** to avoid technical constraints
- **Specific enough** to be measurable and testable
- **Clear enough** for all stakeholders to understand

### 4. Link to Business Strategy

Each BR should tie to:
- Strategic business objectives
- Key Performance Indicators (KPIs)
- Return on Investment (ROI)
- Competitive positioning
- Regulatory compliance

### 5. Version Control and Change Management

- **Track all changes** - Maintain version history with dates and reasons
- **Use version numbers** - e.g., BR1 v1.0, BR1 v1.1, BR1 v2.0
- **Document change impact** - How changes affect related FRs and TCs
- **Require approval for changes** - Formal change control process
- **Communicate changes** - Notify all affected stakeholders

### 6. Review and Validate Regularly

- **Peer reviews** - Have other business analysts review for clarity
- **Stakeholder reviews** - Validate with requirement owners
- **Technical feasibility** - Confirm requirements are technically achievable
- **Regular checkpoints** - Review requirements throughout development
- **Post-implementation review** - Validate success criteria were met

### 7. Maintain Traceability

Every Business Requirement should:
- Be linked to at least one Functional Requirement
- Be testable through Test Cases
- Be tracked in a traceability matrix
- Have clear status (Draft → Approved → Implemented)

### 8. Use Templates and Standards

- **Consistent format** - All BRs follow the same structure
- **Standard terminology** - Maintain a project glossary
- **Naming conventions** - Consistent BR numbering scheme
- **Quality gates** - Requirements must pass checklist before approval

---

## Common Pitfalls

### Pitfall 1: Including Technical Implementation

**Bad Example:**
```markdown
**BR2: Implement REST API with JWT Authentication**
```

**Why it's bad:** Specifies technical solution instead of business need

**Good Alternative:**
```markdown
**BR2: Secure User Authentication and Authorization**

- **Description**: Users need secure access to their accounts with protection
  against unauthorized access
- **Business Goal**: Prevent security breaches and maintain user trust
```

### Pitfall 2: Combining Multiple Objectives

**Bad Example:**
```markdown
**BR3: Improve Website Performance, Add Mobile App, Enhance SEO, and Integrate
Social Media**
```

**Why it's bad:** Too broad, multiple distinct requirements combined

**Good Alternative:**
- BR3: Improve Website Load Performance
- BR4: Provide Mobile Application Access
- BR5: Enhance Search Engine Visibility
- BR6: Enable Social Media Integration

### Pitfall 3: Vague Success Criteria

**Bad Example:**
```markdown
**Success Criteria**:
  - Users are happier
  - System works better
  - Support team has less work
```

**Why it's bad:** Not measurable, subjective, no targets

**Good Alternative:**
```markdown
**Success Criteria**:
  - Customer satisfaction score increases from 3.5 to 4.5 out of 5
  - Page load time decreases from 4.2s to under 2s
  - Support tickets decrease by 40% (from 500 to 300 per month)
```

### Pitfall 4: Missing Stakeholder

**Bad Example:**
```markdown
**Stakeholder**: Management
```

**Why it's bad:** Too vague, no specific accountability

**Good Alternative:**
```markdown
**Stakeholder**: Jennifer Smith, VP of Sales (jennifer.smith@company.com)
```

### Pitfall 5: Technology-Specific Language

**Bad Example:**
```markdown
**BR5: Migrate Database to PostgreSQL and Implement Redis Caching**
```

**Why it's bad:** Focuses on technical solution, not business need

**Good Alternative:**
```markdown
**BR5: Improve Data Access Performance**

- **Description**: Users experience slow response times when accessing reports
  and dashboards, impacting productivity
- **Business Goal**: Reduce average query response time by 70%
```

### Pitfall 6: No Clear Priority

**Bad Example:**
```markdown
**Priority**: Important
```

**Why it's bad:** Ambiguous, not using standard values

**Good Alternative:**
```markdown
**Priority**: High

**Justification**: Critical for Q1 launch, affects 80% of users, high business value
```

### Pitfall 7: Not User-Centric

**Bad Example:**
```markdown
**User Goal**: Use the new system features
```

**Why it's bad:** Doesn't express what user wants to accomplish

**Good Alternative:**
```markdown
**User Goal**: Complete expense report submission in 5 minutes instead of 30
minutes, with fewer errors and less rework
```

---

## Attributes Reference

### Complete Business Requirement Attributes

When documenting Business Requirements in a formal tool or database, include these attributes:

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| **ID** | String | Yes | Unique identifier | BR1, BR2, BR3 |
| **Title** | String | Yes | Brief, descriptive name | Enable Customer Self-Service |
| **Description** | Text | Yes | Detailed explanation of need | 2-3 sentences explaining context |
| **Business Goal** | Text | Yes | Organizational objective | Reduce costs by 30% |
| **User Goal** | Text | Yes | End-user objective | Update account without calling support |
| **Success Criteria** | List | Yes | Measurable outcomes (2-3 minimum) | Specific metrics with targets |
| **Priority** | Enum | Yes | High / Medium / Low | High |
| **Stakeholder** | String | Yes | Name and role | Sarah Chen, Customer Success Director |
| **Version** | String | Yes | Version number | 1.0, 1.1, 2.0 |
| **Status** | Enum | Yes | Current state | Draft / Approved / Implemented |
| **Created Date** | Date | Yes | When BR was created | 2025-01-15 |
| **Created By** | String | Yes | Author name | John Smith |
| **Last Modified Date** | Date | Yes | Last update date | 2025-01-20 |
| **Last Modified By** | String | Yes | Who made last change | Jane Doe |
| **Approval Date** | Date | No | When approved | 2025-01-18 |
| **Approved By** | String | No | Who approved | Michael Johnson |
| **Implementation Date** | Date | No | When implemented | 2025-02-28 |
| **Business Value** | Enum | No | ROI level | High / Medium / Low |
| **Risk** | Enum | No | Implementation risk | High / Medium / Low |
| **Dependencies** | List | No | Related BRs | BR3, BR7 |
| **Assumptions** | Text | No | Key assumptions made | Users have email addresses |
| **Constraints** | Text | No | Limitations or restrictions | Must comply with GDPR |
| **Source** | String | No | Origin of requirement | Customer survey, stakeholder request |
| **Category** | String | No | Grouping/classification | Customer Experience, Security |
| **Related FRs** | List | No | Linked functional requirements | FR1, FR2, FR5 |
| **Notes** | Text | No | Additional information | Any relevant comments |

### Status Definitions

| Status | Definition | Who Can Set | Next Status |
|--------|------------|-------------|-------------|
| **Draft** | Being written, not yet reviewed | Business Analyst | Approved |
| **Approved** | Reviewed and approved by stakeholders | Stakeholder | Implemented |
| **Implemented** | Development complete, deployed to production | Project Manager | N/A |
| **Deferred** | Postponed to future release | Stakeholder | Draft (when revisited) |
| **Rejected** | Will not be implemented | Stakeholder | N/A |
| **Deprecated** | No longer relevant or replaced | Business Analyst | N/A |

---

## Document Templates

### Minimal Business Requirement Template

```markdown
**BR[#]: [Title]**

- **Description**: [2-3 sentences]
- **Business Goal**: [What organization achieves]
- **User Goal**: [What user accomplishes]
- **Success Criteria**:
  - [Measurable criterion 1]
  - [Measurable criterion 2]
  - [Measurable criterion 3]
- **Priority**: High / Medium / Low
- **Stakeholder**: [Name, Role]
```

### Extended Business Requirement Template

```markdown
**BR[#]: [Title]**

**Version**: 1.0
**Status**: Draft
**Created**: YYYY-MM-DD by [Author]
**Last Modified**: YYYY-MM-DD by [Author]

- **Description**: [Detailed explanation of business need, context, and current situation]

- **Business Goal**: [Organizational objective, strategic alignment, financial impact]

- **User Goal**: [End-user perspective, what they want to accomplish, pain points addressed]

- **Success Criteria**:
  - [Specific, measurable criterion with target and timeframe]
  - [Specific, measurable criterion with target and timeframe]
  - [Specific, measurable criterion with target and timeframe]
  - [Additional criteria as needed]

- **Priority**: High / Medium / Low
  - **Justification**: [Why this priority level]

- **Stakeholder**: [Full Name, Title, Contact Information]
  - **Department**: [Department/Division]
  - **Role**: [Decision Authority / Consulted / Informed]

- **Business Value**: High / Medium / Low
  - **ROI**: [Expected return on investment]
  - **Strategic Importance**: [How it aligns with strategy]

- **Assumptions**:
  - [Key assumption 1]
  - [Key assumption 2]

- **Constraints**:
  - [Regulatory, legal, or business constraint 1]
  - [Technical or budget constraint 2]

- **Dependencies**:
  - [BR# - Brief description of dependency]

- **Risks**:
  - [Risk 1 and mitigation approach]
  - [Risk 2 and mitigation approach]

- **Source**: [Customer feedback / Stakeholder request / Market research / etc.]

- **Category**: [Functional area or domain]

- **Acceptance Criteria**:
  - [How we'll know this BR is successfully implemented]

**Approval**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Business Stakeholder | | | |
| Product Owner | | | |
| Project Sponsor | | | |

**Change History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | [Name] | Initial creation |
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-04 | [Your Name] | Initial document creation |

---

**End of Business Requirements Guide**
