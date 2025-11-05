# Strategic Product Requirements Document (PRD) Writing Guide

## Complete Guide to Creating Business-Focused Product Requirements with AI Technology

---

## Table of Contents

1. [Overview](#overview)
2. [Document Structure](#document-structure)
3. [Section-by-Section Guide](#section-by-section-guide)
4. [Design System Guidelines](#design-system-guidelines)
5. [Complete Example](#complete-example)
6. [Quick Reference Checklist](#quick-reference-checklist)

---

## Overview

### Purpose
This guide helps you create strategic, business-focused Product Requirements Documents (PRDs) for AI-powered applications across any domain. The template emphasizes **business value, user outcomes, and strategic capabilities** while enforcing **minimalistic design principles with light theme only**.

### Key Principles
- **Business value over technical specifications**
- **User outcomes over quantitative metrics**
- **Strategic product vision over implementation details**
- **Minimalistic design with light theme enforcement**
- **Accessibility-first approach (WCAG 2.1 AA)**
- **Functional clarity over visual decoration**

### What This Template IS For
✅ Defining strategic product capabilities and business value
✅ Documenting user personas, journeys, and outcomes
✅ Specifying UI/UX requirements with minimalistic design
✅ Ensuring accessibility and responsive design standards
✅ Planning AI-driven product features
✅ Creating mockup and prototype specifications

### What This Template IS NOT For
❌ Technical architecture and infrastructure details
❌ Development timelines and project plans
❌ Quantitative performance metrics
❌ Dark mode or complex theming systems
❌ Decorative or ornamental design elements

---

## Document Structure

### XML Format Overview

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PRD>
    <!-- Core Project Information -->
    <Overview>...</Overview>
    <Goals>...</Goals>
    <SuccessMetrics>...</SuccessMetrics>
    <Stakeholders>...</Stakeholders>

    <!-- User Research & Personas -->
    <UserPersonas>...</UserPersonas>
    <UserJourneys>...</UserJourneys>

    <!-- Functional Requirements -->
    <UseCases>...</UseCases>

    <!-- UI/UX Design Specifications -->
    <DesignSystem>...</DesignSystem>
    <InformationArchitecture>...</InformationArchitecture>
    <Wireframes>...</Wireframes>
    <UserInterface>...</UserInterface>
    <ResponsiveDesign>...</ResponsiveDesign>
    <InteractionSpecifications>...</InteractionSpecifications>
    <AccessibilityRequirements>...</AccessibilityRequirements>

    <!-- Sample Data & Content -->
    <SampleData>...</SampleData>
    <ContentStrategy>...</ContentStrategy>

    <!-- Technical Requirements -->
    <FunctionalRequirements>...</FunctionalRequirements>
    <NonFunctionalRequirements>...</NonFunctionalRequirements>
    <DataRequirements>...</DataRequirements>

    <!-- Testing & Validation -->
    <AcceptanceCriteria>...</AcceptanceCriteria>
    <UsabilityTesting>...</UsabilityTesting>

    <!-- Project Management -->
    <Assumptions>...</Assumptions>
    <RisksAndMitigations>...</RisksAndMitigations>
    <OpenQuestions>...</OpenQuestions>
    <NextSteps>...</NextSteps>
</PRD>
```

---

## Section-by-Section Guide

---

## 1. OVERVIEW Section

### Purpose
Provides the strategic context, vision, and high-level objectives for the product.

### Structure
```xml
<Overview>
[Strategic product description, scope, and business objectives]
</Overview>
```

### Writing Guidance

**Focus on:**
- Business problem being solved
- Strategic product vision
- Target audience and market
- High-level capabilities
- Business value proposition

**Avoid:**
- Technical implementation details
- Specific timelines or deadlines
- Quantitative metrics or KPIs
- Development methodologies

### Examples

**GOOD:**
```xml
<Overview>
This AI-powered customer service platform empowers organizations to deliver exceptional support experiences through intelligent automation and human expertise. The product enables customer service teams to resolve inquiries more effectively by providing instant access to organizational knowledge, intelligent recommendations, and contextual insights. The platform serves mid-to-large enterprises seeking to enhance customer satisfaction while optimizing support operations. Strategic capabilities include natural language understanding, automated knowledge retrieval, and intelligent routing that augments human representatives rather than replacing them. The product vision centers on creating seamless collaboration between AI technology and human expertise to deliver superior customer outcomes.
</Overview>
```

**AVOID:**
```xml
<Overview>
This system will be built using microservices architecture on AWS with a React frontend and Node.js backend. We'll use a BERT-based NLP model achieving 95% accuracy, processing queries in under 2 seconds. The project timeline is 6 months with a budget of $500K. We'll deploy using Docker and Kubernetes with CI/CD via GitHub Actions. Expected ROI is 250% within 18 months.
</Overview>
<!-- Too technical, includes timelines, metrics, costs, ROI, architecture -->
```

---

## 2. GOALS Section

### Purpose
Defines the strategic business goals the product aims to achieve.

### Structure
```xml
<Goals>
    <Goal>[Specific strategic goal 1]</Goal>
    <Goal>[Specific strategic goal 2]</Goal>
    <Goal>[Specific strategic goal 3]</Goal>
</Goals>
```

### Writing Guidance

**Each Goal Should:**
- Be strategic and outcome-focused
- Relate to business value or user benefit
- Be clear and actionable
- Avoid implementation specifics
- Use qualitative language

**Format:**
- Start with an action verb (Enable, Enhance, Improve, Deliver, Create)
- Focus on capabilities or outcomes
- Keep concise (1-2 sentences)

### Examples

**GOOD:**
```xml
<Goals>
    <Goal>Enable customer service representatives to resolve complex queries efficiently through intelligent knowledge access and AI-powered recommendations</Goal>
    <Goal>Enhance customer satisfaction by reducing response times and improving answer accuracy through seamless human-AI collaboration</Goal>
    <Goal>Improve operational efficiency by automating routine inquiries while preserving human touch for complex customer interactions</Goal>
    <Goal>Create a scalable knowledge management system that learns from every interaction and continuously improves recommendation quality</Goal>
    <Goal>Deliver consistent support experiences across all channels by providing unified access to organizational knowledge and customer context</Goal>
</Goals>
```

**AVOID:**
```xml
<Goals>
    <Goal>Achieve 95% chatbot accuracy within 3 months</Goal>
    <Goal>Reduce average handling time by 45% and CSAT scores by 23 points</Goal>
    <Goal>Deploy to production by Q4 2025 with 90% adoption rate</Goal>
    <Goal>Integrate with Salesforce, Zendesk, and internal CRM using REST APIs</Goal>
    <Goal>Generate $2.3M in cost savings with ROI of 280%</Goal>
    <!-- All include specific metrics, timelines, technical details, or ROI -->
</Goals>
```

---

## 3. SUCCESS METRICS Section

### Purpose
Defines how product success will be measured using qualitative indicators.

### Structure
```xml
<SuccessMetrics>
    <Metric name="[MetricName]" description="[Qualitative description]" target="[Qualitative target]"/>
</SuccessMetrics>
```

### Writing Guidance

**Focus on:**
- Qualitative success indicators
- Observable business outcomes
- User satisfaction measures
- Strategic value achievement

**Avoid:**
- Specific percentages or numbers
- Time-based targets
- Technical performance metrics
- ROI or financial projections

### Examples

**GOOD:**
```xml
<SuccessMetrics>
    <Metric name="Customer Satisfaction" description="Improved customer feedback and satisfaction levels" target="Consistently positive customer feedback and high satisfaction ratings"/>
    <Metric name="Representative Efficiency" description="Enhanced ability to resolve queries effectively" target="Representatives report improved confidence and faster resolution capabilities"/>
    <Metric name="Knowledge Accessibility" description="Easy access to relevant organizational knowledge" target="High utilization of AI recommendations with positive representative feedback"/>
    <Metric name="First-Contact Resolution" description="Increased ability to resolve queries on first interaction" target="Noticeable improvement in first-contact resolution rates"/>
    <Metric name="User Adoption" description="Strong engagement from customer service teams" target="Widespread voluntary adoption and integration into daily workflows"/>
</SuccessMetrics>
```

**AVOID:**
```xml
<SuccessMetrics>
    <Metric name="CSAT Score" description="Customer satisfaction score" target="Increase from 78% to 92% within 6 months"/>
    <Metric name="Response Time" description="Average time to respond" target="Reduce from 4.5 minutes to under 2 minutes"/>
    <Metric name="Cost Savings" description="Operational cost reduction" target="$2.3M annually with 280% ROI"/>
    <Metric name="Accuracy" description="AI model performance" target="95% accuracy on validation dataset"/>
    <!-- All include specific numbers, percentages, timelines, or ROI -->
</SuccessMetrics>
```

---

## 4. STAKEHOLDERS Section

### Purpose
Identifies key business stakeholders and their roles in the product.

### Structure
```xml
<Stakeholders>
    <Stakeholder role="[Role]" name="[Name]" contact="[Contact info]"/>
</Stakeholders>
```

### Writing Guidance

**Include:**
- Business sponsors and executives
- Product owners and managers
- Key user representatives
- Important reviewers or approvers

**Avoid:**
- Technical team members (developers, architects)
- External vendors or contractors
- Overly detailed organizational charts

### Examples

**GOOD:**
```xml
<Stakeholders>
    <Stakeholder role="Executive Sponsor" name="Sarah Chen" contact="sarah.chen@company.com"/>
    <Stakeholder role="Product Owner" name="Michael Rodriguez" contact="m.rodriguez@company.com"/>
    <Stakeholder role="Customer Service Director" name="Jennifer Lee" contact="j.lee@company.com"/>
    <Stakeholder role="VP of Customer Experience" name="David Thompson" contact="d.thompson@company.com"/>
    <Stakeholder role="Representative User Group Lead" name="Amanda Foster" contact="a.foster@company.com"/>
</Stakeholders>
```

---

## 5. USER PERSONAS Section

### Purpose
Defines detailed user profiles representing key audience segments.

### Structure
```xml
<UserPersonas>
    <Persona id="[ID]" name="[Persona Name]">
        <Demographics>[Age, role, experience level, etc.]</Demographics>
        <Goal>[Primary goal when using the system]</Goal>
        <PainPoint>[Current challenges and frustrations]</PainPoint>
        <TechComfort>[Technology comfort level]</TechComfort>
        <DeviceUsage>[Primary devices used]</DeviceUsage>
        <ContextOfUse>[When, where, and how they use the system]</ContextOfUse>
    </Persona>
</UserPersonas>
```

### Writing Guidance

**Demographics:**
- Include relevant background (age range, role, experience)
- Avoid personally identifiable information
- Focus on characteristics that impact product usage

**Goal:**
- What the user wants to accomplish
- Why they're using the product
- What success looks like for them

**PainPoint:**
- Current challenges and frustrations
- Problems the product should solve
- Barriers to achieving their goals

**TechComfort:**
- Comfort level with technology (beginner, intermediate, advanced)
- Relevant technical skills or limitations
- Learning preferences

**DeviceUsage:**
- Primary devices (desktop, mobile, tablet)
- Operating systems or browsers
- Access patterns

**ContextOfUse:**
- When they use the product (during work hours, on-the-go, etc.)
- Where they use it (office, home, field, etc.)
- Circumstances surrounding usage

### Examples

**GOOD:**
```xml
<UserPersonas>
    <Persona id="P001" name="Emily - Experienced Customer Service Representative">
        <Demographics>32-45 years old, 5+ years in customer service, handles complex escalations, works in busy call center environment</Demographics>
        <Goal>Resolve customer issues quickly and accurately while maintaining high satisfaction scores and building customer relationships</Goal>
        <PainPoint>Struggles to find accurate information quickly across multiple knowledge bases, leading to longer handling times and occasional incorrect answers. Frustrated by inconsistent information and lack of confidence in complex scenarios.</PainPoint>
        <TechComfort>Intermediate - comfortable with standard business software but prefers simple, intuitive interfaces. Values efficiency over complexity.</TechComfort>
        <DeviceUsage>Primarily desktop computer during 8-hour shifts. Occasionally uses mobile app for quick reference during breaks. Dual monitor setup with multiple applications open.</DeviceUsage>
        <ContextOfUse>Uses the system continuously throughout work day while actively engaged in customer conversations. Needs quick, accurate information under time pressure. Often multitasks between multiple systems.</ContextOfUse>
    </Persona>

    <Persona id="P002" name="Jason - New Customer Service Representative">
        <Demographics>22-28 years old, less than 1 year in customer service, learning product knowledge and company procedures, eager to succeed</Demographics>
        <Goal>Learn quickly, handle customer queries confidently, avoid mistakes that might affect customer satisfaction or personal performance metrics</Goal>
        <PainPoint>Overwhelmed by the volume of product information and company policies. Lacks confidence in unfamiliar scenarios and frequently needs supervisor assistance. Worried about providing incorrect information to customers.</PainPoint>
        <TechComfort>Advanced with consumer technology but new to enterprise customer service tools. Quick learner but needs clear guidance and structure.</TechComfort>
        <DeviceUsage>Desktop computer during training and standard shifts. Uses mobile for training materials and job aids. Comfortable with multi-screen workflows.</DeviceUsage>
        <ContextOfUse>Relies heavily on the system during every customer interaction, especially for unfamiliar topics. Uses it as a learning tool during downtime. Needs confidence-building through clear recommendations and explanations.</ContextOfUse>
    </Persona>

    <Persona id="P003" name="Rachel - Customer Service Supervisor">
        <Demographics>35-50 years old, 10+ years in customer service including 3+ years in leadership, manages team of 15-25 representatives, responsible for quality and performance</Demographics>
        <Goal>Ensure team delivers consistent, high-quality customer service while developing representative skills and maintaining operational efficiency</Goal>
        <PainPoint>Difficulty monitoring quality across large team, time-consuming coaching for knowledge gaps, inconsistent service quality especially with new or less experienced representatives. Limited visibility into common issues or knowledge gaps.</PainPoint>
        <TechComfort>Intermediate to advanced - comfortable with business analytics and reporting tools. Values actionable insights over complex data.</TechComfort>
        <DeviceUsage>Desktop for management tasks and reporting. Mobile for monitoring team performance while away from desk. Needs quick access to team metrics and individual performance indicators.</DeviceUsage>
        <ContextOfUse>Uses system for team monitoring, quality assurance, and coaching. Reviews AI recommendations for appropriateness. Identifies training needs based on system insights. Balances oversight with direct customer escalations.</ContextOfUse>
    </Persona>
</UserPersonas>
```

**AVOID:**
```xml
<UserPersonas>
    <Persona id="P001" name="User">
        <Demographics>Anyone who uses computers</Demographics> <!-- Too vague -->
        <Goal>Use the system</Goal> <!-- Not specific -->
        <PainPoint>Current system is slow</PainPoint> <!-- Technical, not user-focused -->
        <TechComfort>Normal</TechComfort> <!-- Unclear -->
        <DeviceUsage>Computer</DeviceUsage> <!-- Not specific enough -->
        <ContextOfUse>At work</ContextOfUse> <!-- Too brief, lacks context -->
    </Persona>
</UserPersonas>
```

---

## 6. USER JOURNEYS Section

### Purpose
Maps the complete user experience through specific workflows, showing emotions, pain points, and opportunities.

### Structure
```xml
<UserJourneys>
    <Journey persona="[Persona ID]" usecase="[Use Case ID]">
        <Stage name="[Stage Name]" description="[What user is doing]">
            <Actions>[Specific actions taken]</Actions>
            <Touchpoints>[Systems, interfaces, or people involved]</Touchpoints>
            <Emotions>[User emotions - frustrated, confident, confused]</Emotions>
            <PainPoints>[Specific problems encountered]</PainPoints>
            <Opportunities>[Improvement opportunities]</Opportunities>
        </Stage>
    </Journey>
</UserJourneys>
```

### Writing Guidance

**Journey Mapping:**
- Map the complete end-to-end experience
- Include all stages from awareness to completion
- Focus on user perspective, not system processes
- Identify emotional highs and lows

**Stage Elements:**
- **Actions**: What the user actually does
- **Touchpoints**: What they interact with
- **Emotions**: How they feel (use descriptive words)
- **PainPoints**: Problems or frustrations
- **Opportunities**: Where the product can improve the experience

### Examples

**GOOD:**
```xml
<UserJourneys>
    <Journey persona="P001" usecase="UC001">
        <Stage name="Receiving Customer Query" description="Representative receives incoming customer call or message">
            <Actions>Answers call/message, greets customer, listens to initial query, begins documenting interaction in CRM</Actions>
            <Touchpoints>Phone system, CRM interface, customer interaction</Touchpoints>
            <Emotions>Focused, attentive, slightly anxious if query sounds complex</Emotions>
            <PainPoints>Limited context about customer before interaction begins. Pressure to quickly understand issue while maintaining friendly demeanor.</PainPoints>
            <Opportunities>Provide instant customer context and potential issue identification before representative engages</Opportunities>
        </Stage>

        <Stage name="Understanding the Problem" description="Representative clarifies customer need and gathers necessary information">
            <Actions>Asks clarifying questions, searches for customer history, attempts to categorize the issue, takes notes</Actions>
            <Touchpoints>CRM system, knowledge base search, customer conversation, manual notes</Touchpoints>
            <Emotions>Engaged but potentially stressed if issue is unclear or unfamiliar. Concerned about asking too many questions and frustrating customer.</Emotions>
            <PainPoints>Difficulty finding relevant information quickly. Multiple systems to search through. Uncertainty about which information is most current or accurate.</PainPoints>
            <Opportunities>Intelligent query analysis that automatically surfaces relevant information and suggests clarifying questions</Opportunities>
        </Stage>

        <Stage name="Searching for Solution" description="Representative looks for answer or resolution approach">
            <Actions>Searches knowledge bases, reviews similar past cases, consults internal documentation, possibly asks colleague for input</Actions>
            <Touchpoints>Multiple knowledge bases, case history, documentation sites, colleague chat/desk, customer (keeping them informed)</Touchpoints>
            <Emotions>Increasingly frustrated if search is taking too long. Worried about customer wait time. Loss of confidence if unable to find clear answer.</Emotions>
            <PainPoints>Information scattered across multiple systems. Search results often irrelevant or outdated. Difficulty assessing which solution is best. Customer becoming impatient during long hold/wait.</PainPoints>
            <Opportunities>AI-powered unified search that provides ranked, relevant solutions with confidence indicators and reasoning. Suggested response templates.</Opportunities>
        </Stage>

        <Stage name="Validating Solution" description="Representative evaluates potential solution before presenting to customer">
            <Actions>Reviews recommended solution details, checks if it applies to customer's specific situation, considers potential complications, prepares explanation</Actions>
            <Touchpoints>Knowledge articles, product documentation, solution guidelines, customer context</Touchpoints>
            <Emotions>Cautiously optimistic if good solution found. Still slightly uncertain about edge cases or customer-specific factors.</Emotions>
            <PainPoints>Uncertainty about whether solution will work in this specific case. Limited confidence in recommendation. No easy way to verify before presenting to customer.</PainPoints>
            <Opportunities>Provide clear reasoning for recommendations, highlight relevant case examples, flag potential complications, build representative confidence</Opportunities>
        </Stage>

        <Stage name="Delivering Resolution" description="Representative presents solution to customer and guides implementation">
            <Actions>Explains solution clearly to customer, answers follow-up questions, walks through implementation steps if needed, confirms customer understanding</Actions>
            <Touchpoints>Customer conversation, solution documentation for reference, follow-up scheduling if needed</Touchpoints>
            <Emotions>Relieved and confident when presenting validated solution. Professional satisfaction from helping customer. Pride in handling interaction well.</Emotions>
            <PainPoints>Occasionally customer questions expose gaps in understanding. Some solutions are difficult to explain clearly. Concern about whether customer can actually implement solution.</PainPoints>
            <Opportunities>Provide customer-friendly explanations and step-by-step guides. Anticipate common follow-up questions with prepared answers.</Opportunities>
        </Stage>

        <Stage name="Documenting and Closing" description="Representative completes interaction documentation and closes case">
            <Actions>Documents resolution in CRM, categorizes case properly, adds any relevant notes for future reference, confirms customer satisfaction, closes interaction</Actions>
            <Touchpoints>CRM system, case management, satisfaction survey, internal quality tracking</Touchpoints>
            <Emotions>Satisfied with successful resolution. Slightly fatigued from effort. Ready for next interaction.</Emotions>
            <PainPoints>Time-consuming documentation process. Uncertainty about proper categorization. Manual entry of information that system already knows.</PainPoints>
            <Opportunities>Auto-populate case documentation based on interaction. Suggest appropriate categories. Streamline post-interaction tasks.</Opportunities>
        </Stage>
    </Journey>
</UserJourneys>
```

---

## 7. USE CASES Section

### Purpose
Defines specific functional workflows and business capabilities.

### Structure
```xml
<UseCases>
    <UseCase id="[UC-ID]" name="[Use Case Name]">
        <Description>[Detailed description]</Description>
        <PrimaryActor>[Main user type]</PrimaryActor>
        <Preconditions>[What must be true before starting]</Preconditions>
        <Steps>
            <Step>[Detailed step description]</Step>
        </Steps>
        <Postconditions>[End state after completion]</Postconditions>
        <AlternativeFlows>[Error handling, edge cases]</AlternativeFlows>
    </UseCase>
</UseCases>
```

### Writing Guidance

**Note:** This section can reference the detailed use case guide. For complete use case writing guidance, see the "Use-Case-Writing-Guide.md" document.

**Key Points:**
- Focus on business workflows, not technical processes
- Use business actor roles, not technical components
- Describe capabilities and outcomes
- Avoid implementation specifics

### Example

```xml
<UseCases>
    <UseCase id="UC001" name="AI-Assisted Query Resolution">
        <Description>Enable customer service representatives to resolve customer queries efficiently through AI-powered knowledge retrieval and intelligent recommendations</Description>
        <PrimaryActor>Customer Service Representative</PrimaryActor>
        <Preconditions>Representative is authenticated and has access to customer service platform. Customer query has been received through standard channels. Historical customer data is available.</Preconditions>
        <Steps>
            <Step>Representative receives customer query and enters it into the AI-assisted platform</Step>
            <Step>System analyzes query context, customer history, and intent</Step>
            <Step>System retrieves relevant knowledge articles, similar past cases, and product information</Step>
            <Step>System presents ranked recommendations with supporting rationale</Step>
            <Step>Representative reviews AI suggestions and selects most appropriate solution</Step>
            <Step>Representative personalizes response based on customer context</Step>
            <Step>Representative delivers solution to customer and confirms satisfaction</Step>
            <Step>System captures outcome for continuous learning</Step>
        </Steps>
        <Postconditions>Customer query is resolved successfully. Interaction is documented. Representative confidence is enhanced. System learns from the interaction outcome.</Postconditions>
        <AlternativeFlows>If AI recommendations are not suitable, representative can request alternative suggestions, escalate to supervisor, or use traditional knowledge base search. If query is ambiguous, system requests clarification. If customer issue is beyond standard support scope, escalation workflow is triggered.</AlternativeFlows>
    </UseCase>
</UseCases>
```

---

## Design System Guidelines

## 8. DESIGN SYSTEM Section

### Purpose
Establishes consistent design standards, with **mandatory light theme enforcement** and **minimalistic principles**.

### Key Design Principles

#### **⚠️ MANDATORY: Light Theme Only**
- **No dark mode support or toggle**
- All backgrounds must be light (#FFFFFF, #F9FAFB, #F3F4F6)
- All text must be dark for contrast on light backgrounds
- System theme preferences must be ignored
- Consistent light theme across all users and devices

#### **⚠️ MANDATORY: Minimalistic Design**
- Content-first approach with purposeful white space
- No decorative elements unless functional
- Essential functionality only
- Clean, simple visual hierarchy
- Maximum 800px content width for readability

#### **⚠️ MANDATORY: Lucide Icons Only**
- Use Lucide icon library exclusively: https://lucide.dev/
- Standard sizes: 16px, 20px, 24px
- Functional icons only (search, navigation, status, actions)
- Must use CSS variables for colors
- All icons need proper ARIA labels

### Light Theme Color Palette

**⚠️ TEMPLATE DEFAULTS - DO NOT EDIT**

```xml
<ColorPalette readonly="true">
    <!-- Backgrounds - ALWAYS LIGHT -->
    <Color name="Background-Primary" hex="#FFFFFF" usage="Main content areas, cards, modals"/>
    <Color name="Background-Secondary" hex="#F9FAFB" usage="Page backgrounds, subtle areas"/>
    <Color name="Background-Tertiary" hex="#F3F4F6" usage="Disabled states, placeholders"/>

    <!-- Text - ALWAYS DARK -->
    <Color name="Text-Primary" hex="#111827" usage="Headlines, primary content"/>
    <Color name="Text-Secondary" hex="#4B5563" usage="Supporting text, descriptions"/>
    <Color name="Text-Tertiary" hex="#6B7280" usage="Captions, metadata"/>

    <!-- Interactive -->
    <Color name="Primary" hex="#2563EB" usage="Primary actions, links"/>
    <Color name="Primary-Hover" hex="#1D4ED8" usage="Primary actions hover state"/>

    <!-- Utility -->
    <Color name="Border" hex="#E5E7EB" usage="Borders, dividers, outlines"/>
    <Color name="Error" hex="#DC2626" usage="Error states only"/>
    <Color name="Success" hex="#059669" usage="Success states only"/>
    <Color name="Warning" hex="#D97706" usage="Warning states only"/>
</ColorPalette>
```

### Typography System

**⚠️ TEMPLATE DEFAULTS - DO NOT EDIT**

```xml
<Typography readonly="true">
    <FontFamily primary="Inter" fallback="system-ui, -apple-system, sans-serif"/>
    <FontSizes>
        <Size name="H1" pixels="32" usage="Page titles only" weight="600" lineHeight="1.2"/>
        <Size name="H2" pixels="24" usage="Section headers" weight="600" lineHeight="1.3"/>
        <Size name="H3" pixels="20" usage="Subsection headers" weight="600" lineHeight="1.4"/>
        <Size name="Body" pixels="16" usage="All body text" weight="400" lineHeight="1.5"/>
        <Size name="Small" pixels="14" usage="Supporting text only" weight="400" lineHeight="1.5"/>
        <Size name="Caption" pixels="12" usage="Labels, metadata" weight="400" lineHeight="1.4"/>
    </FontSizes>
    <TypographyPrinciples>
        <Principle>Maximum 2 font weights (400, 600)</Principle>
        <Principle>Consistent line heights for readability</Principle>
        <Principle>No decorative fonts or excessive styling</Principle>
    </TypographyPrinciples>
</Typography>
```

### Spacing System

**⚠️ TEMPLATE DEFAULTS - DO NOT EDIT**

```xml
<SpacingSystem readonly="true">
    <BaseUnit>8px</BaseUnit>
    <Spacing>
        <Space size="xs">8px</Space>
        <Space size="sm">16px</Space>
        <Space size="md">24px</Space>
        <Space size="lg">40px</Space>
        <Space size="xl">64px</Space>
        <Space size="2xl">96px</Space>
    </Spacing>
    <WhiteSpacePrinciples>
        <Principle>Generous padding around all content blocks</Principle>
        <Principle>Minimum 40px between major sections</Principle>
        <Principle>White space equals content importance</Principle>
    </WhiteSpacePrinciples>
</SpacingSystem>
```

### Component Standards

**⚠️ TEMPLATE DEFAULTS - DO NOT EDIT**

#### Button Component

```xml
<Component name="Button">
    <LightThemeSpecification>
        <Primary background="#2563EB" text="#FFFFFF" border="none"/>
        <Secondary background="#FFFFFF" text="#2563EB" border="#2563EB"/>
        <TextOnly background="transparent" text="#2563EB" border="none"/>
        <Disabled background="#F3F4F6" text="#9CA3AF" border="#E5E7EB"/>
    </LightThemeSpecification>
    <MinimalistPrinciples>
        <Principle>No shadows, gradients, or decorative elements</Principle>
        <Principle>Light backgrounds only - white or light gray</Principle>
        <Principle>Consistent padding: 12px horizontal, 8px vertical</Principle>
    </MinimalistPrinciples>
</Component>
```

#### Card Component

```xml
<Component name="Card">
    <LightThemeSpecification>
        <Background>#FFFFFF</Background>
        <Border>#E5E7EB</Border>
        <TextPrimary>#111827</TextPrimary>
    </LightThemeSpecification>
    <MinimalistPrinciples>
        <Principle>Always white (#FFFFFF) background</Principle>
        <Principle>Light gray (#E5E7EB) borders only</Principle>
        <Principle>Generous internal padding (24px)</Principle>
    </MinimalistPrinciples>
</Component>
```

#### Input Component

```xml
<Component name="Input">
    <LightThemeSpecification>
        <Background>#FFFFFF</Background>
        <Border>#E5E7EB</Border>
        <FocusBorder>#2563EB</FocusBorder>
        <Text>#111827</Text>
        <Placeholder>#6B7280</Placeholder>
    </LightThemeSpecification>
    <MinimalistPrinciples>
        <Principle>White background for all input fields</Principle>
        <Principle>Clear dark labels above inputs</Principle>
        <Principle>Light gray borders with colored focus states</Principle>
    </MinimalistPrinciples>
</Component>
```

### Icon Implementation

**⚠️ MANDATORY: Lucide Icons Only**

```xml
<IconSystem readonly="true">
    <RequiredIconLibrary>Lucide Icons - https://lucide.dev/</RequiredIconLibrary>
    <IconSpecifications>
        <IconSource>Lucide icon library exclusively - no custom icons</IconSource>
        <IconSizing>16px, 20px, 24px standard sizes</IconSizing>
        <IconColors>Use CSS variables: var(--text-primary), var(--text-secondary)</IconColors>
    </IconSpecifications>

    <StandardIcons>
        <Icon name="Search" lucideName="search" usage="Search inputs"/>
        <Icon name="Menu" lucideName="menu" usage="Navigation toggle"/>
        <Icon name="X" lucideName="x" usage="Close dialogs"/>
        <Icon name="Check" lucideName="check" usage="Success states"/>
        <Icon name="AlertCircle" lucideName="alert-circle" usage="Errors"/>
    </StandardIcons>

    <ImplementationExample>
        <!-- CDN Integration -->
        <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>

        <!-- HTML Usage -->
        <i data-lucide="search" style="color: var(--text-secondary); width: 20px; height: 20px;"></i>

        <!-- Initialization -->
        lucide.createIcons();
    </ImplementationExample>
</IconSystem>
```

---

## 9. RESPONSIVE DESIGN Section

### Purpose
Ensures the product works seamlessly across all device sizes with consistent light theme.

### Breakpoints

**⚠️ TEMPLATE DEFAULTS - DO NOT EDIT**

```xml
<Breakpoints readonly="true">
    <Breakpoint name="Mobile" minWidth="320px" maxWidth="767px"/>
    <Breakpoint name="Tablet" minWidth="768px" maxWidth="1023px"/>
    <Breakpoint name="Desktop" minWidth="1024px" maxWidth="1440px"/>
    <Breakpoint name="Wide" minWidth="1441px"/>
</Breakpoints>
```

### Responsive Principles

**⚠️ TEMPLATE DEFAULTS - DO NOT EDIT**

```xml
<ResponsivePrinciples readonly="true">
    <Principle>Mobile-first approach with progressive enhancement</Principle>
    <Principle>Maintain generous spacing across all breakpoints</Principle>
    <Principle>Single-column layouts on mobile for clarity</Principle>
    <Principle>No horizontal scrolling at any breakpoint</Principle>
    <Principle>Consistent touch targets (44px minimum)</Principle>
    <Principle>Light theme consistency across all device sizes</Principle>
    <Principle>White backgrounds maintained on all screen sizes</Principle>
</ResponsivePrinciples>
```

### Adaptive Behaviors

```xml
<AdaptiveBehaviors>
    <Component name="Navigation">
        <Mobile>Hamburger menu with full-screen overlay on white background</Mobile>
        <Tablet>Horizontal navigation bar with dropdown menus</Tablet>
        <Desktop>Full horizontal navigation with all options visible</Desktop>
    </Component>

    <Component name="Data Table">
        <Mobile>Card-based layout with stacked rows on white background</Mobile>
        <Tablet>Horizontal scroll with fixed first column</Tablet>
        <Desktop>Full table view with all columns visible</Desktop>
    </Component>

    <Component name="Search">
        <Mobile>Full-width input with icon, 44px touch target</Mobile>
        <Tablet>Standard width input in header area</Tablet>
        <Desktop>Expanded search with advanced filters visible</Desktop>
    </Component>
</AdaptiveBehaviors>
```

---

## 10. ACCESSIBILITY REQUIREMENTS Section

### Purpose
Ensures the product is accessible to all users following WCAG 2.1 AA standards with light theme.

### Compliance Level

```xml
<ComplianceLevel>WCAG 2.1 AA</ComplianceLevel>
```

### Light Theme Accessibility

**⚠️ TEMPLATE DEFAULTS - DO NOT EDIT**

```xml
<LightThemeAccessibility readonly="true">
    <ContrastRequirements>
        <Requirement level="AAA" ratio="7:1" description="Text-Primary (#111827) on Background-Primary (#FFFFFF)"/>
        <Requirement level="AA" ratio="4.5:1" description="Text-Secondary (#4B5563) on Background-Primary (#FFFFFF)"/>
        <Requirement level="AA" ratio="3:1" description="Primary (#2563EB) on Background-Primary (#FFFFFF)"/>
        <Requirement level="AA" ratio="3:1" description="Error (#DC2626) on Background-Primary (#FFFFFF)"/>
    </ContrastRequirements>

    <LightThemeRules>
        <Rule>All contrast ratios calculated specifically for light backgrounds</Rule>
        <Rule>No dark mode accessibility testing required</Rule>
        <Rule>Focus indicators must be visible on white backgrounds</Rule>
        <Rule>Color-coding must work with light theme palette only</Rule>
    </LightThemeRules>
</LightThemeAccessibility>
```

### Keyboard Navigation

```xml
<KeyboardNavigation>
    <TabOrder>Logical tab order following visual layout from top to bottom, left to right</TabOrder>
    <Shortcuts>
        <Shortcut key="/" action="Focus search input"/>
        <Shortcut key="Escape" action="Close modal or dialog"/>
        <Shortcut key="Enter" action="Submit form or activate button"/>
    </Shortcuts>

    <!-- Light Theme Focus States -->
    <LightThemeFocus readonly="true">
        <FocusColor>#2563EB</FocusColor>
        <FocusWidth>2px</FocusWidth>
        <FocusStyle>solid outline</FocusStyle>
        <FocusOffset>2px</FocusOffset>
        <FocusBackground>Maintain white background with colored outline</FocusBackground>
    </LightThemeFocus>
</KeyboardNavigation>
```

### Screen Reader Support

```xml
<ScreenReaderSupport>
    <ARIALabels>
        <Label element="Search input" aria-label="Search knowledge base"/>
        <Label element="Close button" aria-label="Close dialog"/>
        <Label element="Navigation menu" aria-label="Main navigation"/>
        <Label element="Submit button" aria-label="Submit query"/>
    </ARIALabels>

    <StructuralMarkup>
        <Structure>Use semantic HTML5 elements (header, nav, main, aside, footer)</Structure>
        <Structure>Proper heading hierarchy (H1 > H2 > H3)</Structure>
        <Structure>ARIA landmark roles where semantic HTML is insufficient</Structure>
        <Structure>Skip navigation link for keyboard users</Structure>
    </StructuralMarkup>
</ScreenReaderSupport>
```

---

## 11. CONTENT STRATEGY Section

### Purpose
Defines the tone, voice, and messaging approach for the product.

### Structure

```xml
<ContentStrategy>
    <CopyTone>[Friendly/Professional/Technical]</CopyTone>

    <MessageTypes>
        <MessageType name="Success" tone="Positive, encouraging" examples="Successfully saved. Your changes have been applied."/>
        <MessageType name="Error" tone="Helpful, not blaming" examples="Something went wrong. Please try again or contact support."/>
        <MessageType name="Warning" tone="Cautious, informative" examples="This action cannot be undone. Are you sure you want to continue?"/>
        <MessageType name="Info" tone="Clear, informative" examples="Your session will expire in 5 minutes. Save your work to avoid losing changes."/>
    </MessageTypes>

    <Microcopy>
        <Element name="SearchButton" content="Search" rationale="Single action word, clear purpose"/>
        <Element name="CancelButton" content="Cancel" rationale="Standard, familiar term"/>
        <Element name="SaveButton" content="Save" rationale="Clear completion action"/>
        <Element name="LoadingText" content="Loading..." rationale="Simple progress indication"/>
    </Microcopy>
</ContentStrategy>
```

### Minimalistic Content Guidelines

**⚠️ TEMPLATE DEFAULTS - DO NOT EDIT**

```xml
<MinimalistContent readonly="true">
    <ContentPrinciples>
        <Principle>One idea per sentence</Principle>
        <Principle>Essential information only</Principle>
        <Principle>No marketing language or unnecessary adjectives</Principle>
        <Principle>Clear, actionable language</Principle>
        <Principle>Consistent terminology throughout</Principle>
    </ContentPrinciples>
</MinimalistContent>
```

---

## Complete Example

### AI-Powered Customer Service Platform PRD

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PRD>
<!-- CORE PROJECT INFORMATION -->
<Overview>
This AI-powered customer service platform empowers organizations to deliver exceptional support experiences through intelligent automation and human expertise. The product enables customer service teams to resolve inquiries more effectively by providing instant access to organizational knowledge, intelligent recommendations, and contextual insights. The platform serves mid-to-large enterprises seeking to enhance customer satisfaction while optimizing support operations. Strategic capabilities include natural language understanding, automated knowledge retrieval, and intelligent routing that augments human representatives rather than replacing them. The product vision centers on creating seamless collaboration between AI technology and human expertise to deliver superior customer outcomes.
</Overview>

<Goals>
    <Goal>Enable customer service representatives to resolve complex queries efficiently through intelligent knowledge access and AI-powered recommendations</Goal>
    <Goal>Enhance customer satisfaction by reducing response times and improving answer accuracy through seamless human-AI collaboration</Goal>
    <Goal>Improve operational efficiency by automating routine inquiries while preserving human touch for complex customer interactions</Goal>
    <Goal>Create a scalable knowledge management system that learns from every interaction and continuously improves recommendation quality</Goal>
</Goals>

<SuccessMetrics>
    <Metric name="Customer Satisfaction" description="Improved customer feedback and satisfaction levels" target="Consistently positive customer feedback and high satisfaction ratings"/>
    <Metric name="Representative Efficiency" description="Enhanced ability to resolve queries effectively" target="Representatives report improved confidence and faster resolution capabilities"/>
    <Metric name="Knowledge Accessibility" description="Easy access to relevant organizational knowledge" target="High utilization of AI recommendations with positive representative feedback"/>
    <Metric name="First-Contact Resolution" description="Increased ability to resolve queries on first interaction" target="Noticeable improvement in first-contact resolution rates"/>
</SuccessMetrics>

<Stakeholders>
    <Stakeholder role="Executive Sponsor" name="Sarah Chen" contact="sarah.chen@company.com"/>
    <Stakeholder role="Product Owner" name="Michael Rodriguez" contact="m.rodriguez@company.com"/>
    <Stakeholder role="Customer Service Director" name="Jennifer Lee" contact="j.lee@company.com"/>
    <Stakeholder role="VP of Customer Experience" name="David Thompson" contact="d.thompson@company.com"/>
</Stakeholders>

<!-- USER RESEARCH & PERSONAS -->
<UserPersonas>
    <Persona id="P001" name="Emily - Experienced Customer Service Representative">
        <Demographics>32-45 years old, 5+ years in customer service, handles complex escalations, works in busy call center environment</Demographics>
        <Goal>Resolve customer issues quickly and accurately while maintaining high satisfaction scores and building customer relationships</Goal>
        <PainPoint>Struggles to find accurate information quickly across multiple knowledge bases, leading to longer handling times and occasional incorrect answers</PainPoint>
        <TechComfort>Intermediate - comfortable with standard business software but prefers simple, intuitive interfaces</TechComfort>
        <DeviceUsage>Primarily desktop computer during 8-hour shifts with dual monitor setup</DeviceUsage>
        <ContextOfUse>Uses the system continuously throughout work day while actively engaged in customer conversations</ContextOfUse>
    </Persona>
</UserPersonas>

<!-- UI/UX DESIGN SPECIFICATIONS -->
<DesignSystem>
    <!-- ⚠️ TEMPLATE DEFAULTS - DO NOT EDIT: Minimalistic Design Standards -->
    <DesignPhilosophy readonly="true">
        <CorePrinciples>
            <Principle name="Minimalism">Content-first approach with purposeful white space</Principle>
            <Principle name="Clarity">Clear visual hierarchy and intuitive navigation</Principle>
            <Principle name="Functionality">Every element serves a specific user need</Principle>
        </CorePrinciples>

        <!-- ⚠️ TEMPLATE DEFAULTS - DO NOT EDIT: Light Theme Enforcement -->
        <ThemeEnforcement readonly="true">
            <RequiredTheme>Light theme only - no dark mode support or toggle</RequiredTheme>
            <BackgroundStrategy>Always light backgrounds (#FFFFFF, #F9FAFB) for optimal readability</BackgroundStrategy>
            <TextStrategy>Dark text on light backgrounds for maximum contrast and accessibility</TextStrategy>
            <UserPreferences>System dark mode preferences must be ignored - light theme enforced</UserPreferences>
        </ThemeEnforcement>
    </DesignPhilosophy>

    <BrandIdentity>
        <!-- ⚠️ TEMPLATE DEFAULTS - DO NOT EDIT: Light Theme Color Palette -->
        <ColorPalette readonly="true">
            <!-- Light Theme Backgrounds -->
            <Color name="Background-Primary" hex="#FFFFFF" usage="Main content areas, cards"/>
            <Color name="Background-Secondary" hex="#F9FAFB" usage="Page backgrounds"/>

            <!-- Light Theme Text Colors -->
            <Color name="Text-Primary" hex="#111827" usage="Headlines, primary content"/>
            <Color name="Text-Secondary" hex="#4B5563" usage="Supporting text"/>

            <!-- Interactive Colors -->
            <Color name="Primary" hex="#2563EB" usage="Primary actions, links"/>
            <Color name="Border" hex="#E5E7EB" usage="Borders, dividers"/>
        </ColorPalette>

        <!-- ⚠️ TEMPLATE DEFAULTS - DO NOT EDIT: Clean Typography System -->
        <Typography readonly="true">
            <FontFamily primary="Inter" fallback="system-ui, sans-serif"/>
            <FontSizes>
                <Size name="H1" pixels="32" weight="600" lineHeight="1.2"/>
                <Size name="Body" pixels="16" weight="400" lineHeight="1.5"/>
            </FontSizes>
        </Typography>
    </BrandIdentity>

    <!-- ⚠️ TEMPLATE DEFAULTS - DO NOT EDIT: Icon System Requirements -->
    <IconSystem readonly="true">
        <RequiredIconLibrary>Lucide Icons - https://lucide.dev/</RequiredIconLibrary>
        <IconSpecifications>
            <IconSource>Lucide icon library exclusively</IconSource>
            <IconSizing>16px, 20px, 24px standard sizes</IconSizing>
            <IconColors>Use CSS variables for colors</IconColors>
        </IconSpecifications>
    </IconSystem>
</DesignSystem>

<!-- USER INTERFACE -->
<UserInterface>
    <UIComponent name="Search Input">
        <Description>Primary search interface for querying knowledge base</Description>
        <Location>Top center of main interface</Location>
        <KeyElements>
            <Element>Search input field with placeholder text</Element>
            <Element>Lucide search icon (data-lucide="search")</Element>
            <Element>Submit button</Element>
        </KeyElements>

        <InteractionBehavior>
            <Trigger event="typing" response="Show autocomplete suggestions in dropdown"/>
            <Trigger event="submit" response="Display search results below"/>
            <Trigger event="focus" response="Show focus outline in primary color"/>
        </InteractionBehavior>

        <ResponsiveBehavior>
            <Breakpoint size="mobile" behavior="Full width with 44px height for touch targets"/>
            <Breakpoint size="desktop" behavior="Fixed 600px width centered in header"/>
        </ResponsiveBehavior>

        <AccessibilityFeatures>
            <Feature>aria-label="Search knowledge base"</Feature>
            <Feature>Keyboard shortcut: "/" to focus</Feature>
            <Feature>Clear focus indicator (#2563EB outline)</Feature>
        </AccessibilityFeatures>

        <!-- ⚠️ TEMPLATE DEFAULTS - DO NOT EDIT: Light Theme UI Guidelines -->
        <LightThemeUI readonly="true">
            <BackgroundStrategy>White (#FFFFFF) input background</BackgroundStrategy>
            <TextStrategy>Dark text (#111827) for input</TextStrategy>
            <BorderStrategy>Light gray (#E5E7EB) border with primary (#2563EB) focus state</BorderStrategy>
        </LightThemeUI>
    </UIComponent>

    <UIComponent name="Result Cards">
        <Description>Display knowledge base articles and recommendations</Description>
        <Location>Main content area below search</Location>
        <KeyElements>
            <Element>Card container with white background</Element>
            <Element>Article title (H3, 20px, weight 600)</Element>
            <Element>Snippet of content (body text, 16px)</Element>
            <Element>Confidence indicator</Element>
            <Element>Lucide icons for actions (bookmark, share)</Element>
        </KeyElements>

        <InteractionBehavior>
            <Trigger event="hover" response="Subtle background color shift to #F9FAFB"/>
            <Trigger event="click" response="Expand to show full article"/>
        </InteractionBehavior>

        <ResponsiveBehavior>
            <Breakpoint size="mobile" behavior="Single column, full width, stacked cards"/>
            <Breakpoint size="desktop" behavior="Grid layout, 2-3 cards per row"/>
        </ResponsiveBehavior>

        <!-- ⚠️ TEMPLATE DEFAULTS - DO NOT EDIT: Light Theme UI Guidelines -->
        <LightThemeUI readonly="true">
            <BackgroundStrategy>White (#FFFFFF) card background</BackgroundStrategy>
            <BorderStrategy>Light gray (#E5E7EB) borders for separation</BorderStrategy>
            <TextStrategy>Dark primary text (#111827) for titles, secondary (#4B5563) for snippets</TextStrategy>
        </LightThemeUI>
    </UIComponent>
</UserInterface>

<!-- ACCESSIBILITY REQUIREMENTS -->
<AccessibilityRequirements>
    <ComplianceLevel>WCAG 2.1 AA</ComplianceLevel>

    <!-- ⚠️ TEMPLATE DEFAULTS - DO NOT EDIT: Light Theme Accessibility Standards -->
    <LightThemeAccessibility readonly="true">
        <ContrastRequirements>
            <Requirement level="AAA" ratio="7:1" description="Text-Primary (#111827) on Background-Primary (#FFFFFF)"/>
            <Requirement level="AA" ratio="4.5:1" description="Text-Secondary (#4B5563) on Background-Primary (#FFFFFF)"/>
        </ContrastRequirements>
    </LightThemeAccessibility>

    <KeyboardNavigation>
        <TabOrder>Search input → Results → Action buttons → Navigation</TabOrder>
        <Shortcuts>
            <Shortcut key="/" action="Focus search input"/>
            <Shortcut key="Escape" action="Close expanded article"/>
        </Shortcuts>
    </KeyboardNavigation>
</AccessibilityRequirements>

</PRD>
```

---

## Quick Reference Checklist

### Before You Start

- [ ] Understand the business problem and strategic objectives
- [ ] Identify target users and their needs
- [ ] Know the key business value propositions
- [ ] Commit to minimalistic design with light theme only
- [ ] Confirm Lucide icons will be used exclusively

### Core Information Sections

**Overview:**
- [ ] Describes business problem and strategic vision
- [ ] Identifies target audience
- [ ] Highlights key capabilities
- [ ] Avoids technical implementation details

**Goals:**
- [ ] 3-5 strategic business goals
- [ ] Action-oriented (Enable, Enhance, Improve, Create)
- [ ] Focused on capabilities and outcomes
- [ ] No specific metrics or timelines

**Success Metrics:**
- [ ] Qualitative success indicators
- [ ] Observable business outcomes
- [ ] No percentages, numbers, or ROI
- [ ] Realistic and meaningful targets

**Stakeholders:**
- [ ] Business sponsors and executives
- [ ] Product owners and key users
- [ ] Contact information included
- [ ] Technical team members excluded

### User Research Sections

**User Personas:**
- [ ] 2-5 detailed personas representing key user segments
- [ ] Each includes demographics, goals, pain points
- [ ] Technology comfort level described
- [ ] Device usage and context documented
- [ ] Specific and realistic (not generic)

**User Journeys:**
- [ ] Maps complete end-to-end experience
- [ ] Includes actions, touchpoints, emotions
- [ ] Identifies pain points and opportunities
- [ ] References specific personas and use cases

**Use Cases:**
- [ ] Describes business workflows, not technical processes
- [ ] Uses business actors, not technical components
- [ ] Includes preconditions and postconditions
- [ ] Documents alternative flows and edge cases

### Design System Sections

**⚠️ MANDATORY Design Standards:**
- [ ] Light theme only - no dark mode support
- [ ] All backgrounds are light (#FFFFFF, #F9FAFB, #F3F4F6)
- [ ] All text is dark for contrast
- [ ] Lucide icons only - no custom icons
- [ ] Minimalistic approach - no decorative elements

**Color Palette:**
- [ ] Uses template default colors (Background-Primary #FFFFFF, etc.)
- [ ] Light theme CSS variables defined
- [ ] Contrast ratios meet WCAG AA standards
- [ ] No dark mode variables or theming

**Typography:**
- [ ] Inter font family (or system fallback)
- [ ] Maximum 2 font weights (400, 600)
- [ ] 6 size levels (H1, H2, H3, Body, Small, Caption)
- [ ] Consistent line heights for readability

**Spacing:**
- [ ] 8px base unit
- [ ] 6 spacing levels (xs through 2xl)
- [ ] Generous white space throughout
- [ ] Minimum 40px between major sections

**Icons:**
- [ ] Lucide icons exclusively
- [ ] Standard sizes: 16px, 20px, 24px
- [ ] Colors use CSS variables
- [ ] All icons have ARIA labels
- [ ] CDN or npm package specified

### UI/UX Sections

**User Interface Components:**
- [ ] Each component has clear description and location
- [ ] Interaction behaviors documented
- [ ] Responsive behaviors for all breakpoints
- [ ] Accessibility features included
- [ ] Light theme styling specified

**Responsive Design:**
- [ ] Standard breakpoints used (Mobile, Tablet, Desktop, Wide)
- [ ] Mobile-first approach
- [ ] Single-column layouts on mobile
- [ ] No horizontal scrolling
- [ ] 44px minimum touch targets
- [ ] Light theme consistent across all sizes

**Accessibility:**
- [ ] WCAG 2.1 AA compliance level
- [ ] Contrast requirements for light theme
- [ ] Keyboard navigation documented
- [ ] ARIA labels for all interactive elements
- [ ] Screen reader support specified
- [ ] Focus indicators visible on white backgrounds

### Content & Strategy Sections

**Content Strategy:**
- [ ] Copy tone defined (Friendly, Professional, Technical)
- [ ] Message types documented (Success, Error, Warning, Info)
- [ ] Microcopy specified for key elements
- [ ] Minimalistic content principles followed
- [ ] No marketing language or unnecessary adjectives

**Sample Data:**
- [ ] Representative data structures defined
- [ ] Sample records provided
- [ ] Edge cases considered (long text, empty fields)

### Technical Requirements Sections

**Functional Requirements:**
- [ ] Specific, measurable requirements
- [ ] Focused on capabilities, not implementation
- [ ] Each has unique ID (FR-001, FR-002, etc.)

**Non-Functional Requirements:**
- [ ] Performance, security, usability requirements
- [ ] Qualitative targets (not specific metrics)
- [ ] Each has unique ID (NFR-001, NFR-002, etc.)

**Data Requirements:**
- [ ] Data sources identified
- [ ] Field names and types documented
- [ ] Retention policies specified

### Testing & Validation Sections

**Acceptance Criteria:**
- [ ] Specific, measurable criteria
- [ ] Testable and verifiable
- [ ] Each has unique ID (AC-001, AC-002, etc.)

**Usability Testing:**
- [ ] Test scenarios documented
- [ ] Specific tasks defined
- [ ] Success metrics identified

### Project Management Sections

**Assumptions:**
- [ ] Key project assumptions documented
- [ ] Dependencies identified

**Risks & Mitigations:**
- [ ] Major risks identified
- [ ] Mitigation strategies defined
- [ ] Each has unique ID (R-001, R-002, etc.)

**Open Questions:**
- [ ] Unresolved questions captured
- [ ] Owners assigned for resolution

**Next Steps:**
- [ ] Immediate action items documented
- [ ] Clear ownership and expectations

---

## Language and Style Validation

### Use This Qualitative Language

| Concept | Use This | Not This |
|---------|----------|----------|
| Performance | "rapid response" | "< 2 seconds" |
| Accuracy | "high accuracy" | "95% accurate" |
| Improvement | "significant improvement" | "50% reduction" |
| Adoption | "strong user adoption" | "90% adoption rate" |
| Timeline | "phased approach" | "6-month implementation" |
| Value | "substantial business value" | "ROI of 250%" |
| Cost | "cost optimization" | "$1M savings" |
| Scale | "enterprise scale" | "500 users" |

### Design Language Checklist

- [ ] "Light theme" (not "light mode" or "default theme")
- [ ] "White background" (specific color, not vague)
- [ ] "Minimalistic design" (not "simple" or "clean")
- [ ] "Lucide icons" (specific library named)
- [ ] "Generous white space" (not just "spacing")
- [ ] "WCAG 2.1 AA" (specific standard)
- [ ] "Focus outline" (not "focus ring" or "focus border")

---

## Final Validation Questions

Before finalizing your PRD, ask yourself:

1. **Business Focus:** Does this read like a strategic product vision or a technical spec?
2. **User-Centric:** Are user needs and outcomes clearly prioritized?
3. **Design Clarity:** Is the minimalistic, light-theme-only approach enforced throughout?
4. **Accessibility:** Are WCAG 2.1 AA standards met with specific light theme requirements?
5. **Icon Consistency:** Are Lucide icons specified exclusively with no custom icons?
6. **Responsive Design:** Are all breakpoints and adaptive behaviors documented?
7. **Qualitative Language:** Have all quantitative metrics been removed?
8. **Completeness:** Are all essential sections filled with meaningful content?
9. **Testability:** Can acceptance criteria be validated without ambiguity?
10. **Stakeholder Clarity:** Would executives and users understand the product vision?

---

## Common Mistakes to Avoid

### Design Mistakes

1. **Dark Mode Support:** Adding dark theme options or toggles (Light theme only!)
2. **Custom Icons:** Using any icon library other than Lucide
3. **Decorative Elements:** Adding shadows, gradients, or ornamental graphics
4. **Complex Theming:** Creating multiple color schemes or user preferences
5. **Inconsistent Spacing:** Not using the 8px-based spacing system

### Content Mistakes

1. **Technical Language:** Using terms like "API," "microservices," "containers"
2. **Specific Metrics:** Including "95% accuracy," "<2 seconds," "50% improvement"
3. **Financial Details:** Mentioning costs, savings, or ROI percentages
4. **Timelines:** Specifying "6 months," "Q4 2025," or specific deadlines
5. **Marketing Fluff:** Using excessive adjectives or promotional language

### Structure Mistakes

1. **Missing Personas:** Not creating detailed, realistic user personas
2. **Vague Goals:** Goals that aren't actionable or strategic
3. **Technical Use Cases:** Describing system processes instead of user workflows
4. **Incomplete Journeys:** Not mapping the full end-to-end user experience
5. **Missing Accessibility:** Forgetting ARIA labels, keyboard navigation, or contrast requirements

---

## Best Practices

### For Strategic Success

1. **Start with Users:** Always begin with user research and personas
2. **Think Capabilities:** Focus on what the product enables, not how it's built
3. **Stay Qualitative:** Use descriptive language instead of specific metrics
4. **Maintain Flexibility:** Avoid prescribing implementation details

### For Design Excellence

1. **Enforce Light Theme:** Consistently apply light backgrounds and dark text
2. **Use Lucide Icons:** Never deviate from the Lucide icon library
3. **Embrace White Space:** Generous spacing is a feature, not wasted space
4. **Prioritize Accessibility:** WCAG compliance isn't optional

### For Stakeholder Communication

1. **Be Clear:** Use straightforward language without jargon
2. **Show Value:** Always connect features to business outcomes
3. **Provide Context:** Explain the "why" behind decisions
4. **Stay Focused:** One idea per section, no information overload

---

## Conclusion

This PRD template provides a comprehensive framework for creating strategic, business-focused product requirements that effectively communicate the value of AI-powered products. By emphasizing user outcomes, enforcing minimalistic design with light theme only, and maintaining business focus over technical details, your PRDs will serve as clear, actionable guides for product development.

**Remember:**
- **Light theme only** - no exceptions
- **Lucide icons exclusively** - no custom icons
- **Minimalistic design** - functionality over decoration
- **Business value first** - implementation details later
- **Accessibility always** - WCAG 2.1 AA compliance

---

**Document Version:** 1.0
**Last Updated:** 2025-11-04
**Based on Template:** 002-template-prd.md v3.0
