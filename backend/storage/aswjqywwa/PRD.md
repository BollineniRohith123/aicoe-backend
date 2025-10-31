---
**AICOE Product Requirements Document**

**Document Classification:** Internal - Confidential
**Version:** 1.0
**Date:** October 29, 2025
**Prepared By:** AICOE Multi-Agent Platform
**Project:** Manufacturing process automation with AI

---

# Manufacturing process automation with AI - Product Requirements Document

## 1. Executive Summary
This document outlines the product requirements for an AI-driven manufacturing optimization system for a Tier 1 automotive parts manufacturer. The facility, producing over 500,000 transmission components annually, faces significant operational challenges including unplanned downtime, low Overall Equipment Effectiveness (OEE), and high defect rates. This project aims to implement a comprehensive AI solution integrating predictive maintenance, automated quality inspection, production process optimization, and a digital twin. The expected business impact is substantial, including a 50% reduction in unplanned downtime, an increase in OEE to industry-leading levels, and a significant ROI within 24 months. Key stakeholders include Operations, Quality, Maintenance, IT, and Executive leadership, with a phased implementation over 24 months.

## 2. Goals & Objectives
### Business Goals
- Reduce unplanned downtime by 50% (from 2,400 to 1,200 hours annually), saving $1.4M in lost production.
- Increase Overall Equipment Effectiveness (OEE) from 68% to 75% or higher.
- Reduce the product defect rate from 8.2% to below 3%.
- Decrease manual quality inspection time by 90% (from 45 to under 5 minutes per batch).
- Increase production capacity utilization from 60-80% to 90%+.
- Achieve a positive Return on Investment (ROI) within 24 months of full implementation.

### User Goals
- **Maintenance Supervisor:** Proactively schedule maintenance to prevent equipment failure and minimize production disruption.
- **Quality Assurance Manager:** Automate defect detection to improve accuracy and free up inspectors for value-added tasks.
- **Production Manager:** Optimize production schedules and machine settings in real-time to maximize throughput.
- **Manufacturing Engineer:** Simulate process changes in a digital twin to validate improvements before physical implementation.
- **Operations Director:** Gain complete, real-time visibility into all aspects of the production floor for data-driven decision-making.

### Technical Goals
- Achieve 99.5% system uptime for production-critical functions.
- Ensure data latency is under 5 seconds for real-time analytics and alerts.
- Attain >90% prediction accuracy for equipment failures.
- Attain >95% accuracy for automated defect detection.
- Integrate disparate data systems (production, quality, maintenance) into a unified data lake.
- Successfully integrate with the legacy SCADA system from 2012.

## 3. Problem Statement
### What problem are we solving?
The manufacturing facility is operating below its potential due to reactive maintenance practices, manual quality control processes, and a lack of real-time data visibility. This leads to significant financial losses from unplanned downtime, high scrap and rework costs, and operational inefficiencies.

### Who has this problem?
The problem impacts the entire organization, most critically the Operations Director, Production Managers, Maintenance Supervisors, and Quality Assurance Managers who are responsible for meeting production targets, managing costs, and ensuring product quality.

### Current pain points and limitations
- **Unplanned Downtime:** 2,400 hours annually, costing $2.8M in lost production.
- **Low OEE:** At 68%, it is significantly below the 75% industry average.
- **High Defect Rate:** 8.2% of finished products require costly rework or are scrapped.
- **Inspection Bottleneck:** Manual inspection is slow (45 mins/batch), creating production delays.
- **Resource Allocation:** Production lines are underutilized, running at only 60-80% capacity.
- **Visibility Gaps:** Only 40% of the production floor is covered by sensors, leading to blind spots.
- **Data Silos:** Critical production, quality, and maintenance data are stored in separate, unintegrated systems.

### Opportunity size and market context
By addressing these inefficiencies with AI, the facility can save millions annually, improve its competitive position in the automotive supply chain, and create a scalable model for future digital transformation initiatives across multiple sites.

## 4. User Personas & Stakeholders
### User Personas

**Persona 1: David Chen, Maintenance Supervisor**
- **Role/Title:** Maintenance Supervisor
- **Goals and Motivations:** To maximize equipment uptime and minimize emergency repairs. Wants to move from a reactive "fix-it-when-it-breaks" model to a proactive, scheduled maintenance approach.
- **Pain Points:** Constantly firefighting unexpected equipment failures. Lack of data to predict which machines need attention. Pressure from production to get lines running again quickly.
- **Technical Proficiency:** Comfortable with CMMS systems and diagnostic tools. New to AI-driven dashboards but eager to learn.

**Persona 2: Karen Lee, Quality Assurance Manager**
- **Role/Title:** Quality Assurance Manager
- **Goals and Motivatives:** To reduce the defect rate and ensure 100% compliance with automotive quality standards (IATF 16949). Wants to improve the speed and accuracy of inspections.
- **Pain Points:** Manual inspection is a bottleneck and prone to human error. High rework and scrap costs impact the department's budget. Difficulty in tracing the root cause of defects quickly.
- **Technical Proficiency:** Proficient with statistical process control (SPC) software. Understands the potential of computer vision but needs a user-friendly implementation.

**Persona 3: Maria Rodriguez, Production Manager**
- **Role/Title:** Production Manager
- **Goals and Motivations:** To meet daily and weekly production targets. To optimize resource allocation and machine settings for maximum throughput.
- **Pain Points:** Production lines stop unexpectedly. Lack of real-time insight into which processes are underperforming. Difficulty balancing speed with quality.
- **Technical Proficiency:** Expert in production planning and floor management. Familiar with basic reporting dashboards.

### Key Stakeholders
- **Robert Martinez (Operations Director):** Project sponsor. Interested in overall ROI, OEE improvement, and strategic alignment.
- **Emily Watson (Data Scientist):** Responsible for model development, accuracy, and the MLOps pipeline.
- **Tom Anderson (Manufacturing Engineer):** Focused on process optimization, digital twin validation, and ensuring technical feasibility on the floor.
- **James Wilson (IT Infrastructure Lead):** Accountable for network security, data architecture, and system integration.
- **Sarah Kim (Financial Analyst):** Tracks project budget, measures financial impact, and validates ROI.
- **Executive Leadership:** Final approvers of budget and strategic direction.

## 5. Features & User Stories
### Must-Have
- **Predictive Maintenance System**
  - User Story: As a Maintenance Supervisor, I want to receive automated alerts for potential equipment failures so that I can schedule proactive maintenance and avoid unplanned downtime.
  - User Story: As a Maintenance Technician, I want to access a real-time equipment health dashboard so that I can quickly diagnose issues and order necessary parts.
- **Automated Quality Inspection**
  - User Story: As a Quality Inspector, I want the system to automatically flag defective components so that I can focus my attention on complex or uncertain cases.
  - User Story: As a Production Manager, I want to see real-time defect rates so that I can immediately address process deviations.
- **Real-time Production Monitoring Dashboard**
  - User Story: As an Operations Director, I want a single dashboard showing OEE, throughput, and equipment status across all lines so that I can make informed strategic decisions.
  - User Story: As a Production Manager, I want to receive intelligent alerts for production anomalies so that I can intervene before they escalate.

### Should-Have
- **Production Process Optimization**
  - User Story: As a Manufacturing Engineer, I want to receive recommendations for optimal machine settings so that I can maximize throughput and minimize energy consumption.
  - User Story: As a Production Manager, I want an optimized production schedule that accounts for predicted maintenance and equipment availability.
- **Digital Twin Simulation**
  - User Story: As a Manufacturing Engineer, I want to simulate the impact of a new product introduction in a digital twin so that I can identify and mitigate bottlenecks before physical implementation.
- **AI Model Management**
  - User Story: As a Data Scientist, I want an automated system to monitor model drift and trigger retraining so that prediction accuracy remains consistently high.

### Nice-to-Have
- **Advanced Analytics and Reporting**
  - User Story: As a Financial Analyst, I want automated reports on the cost savings generated by the AI system so that I can track ROI against projections.
- **Mobile Access for Floor Staff**
  - User Story: As a Maintenance Technician, I want to receive and acknowledge maintenance alerts on a mobile device so that I can respond faster, even when away from a terminal.

## 6. Use Cases

### UC-001: Predictive Maintenance for Critical Equipment
- **Actors:** Maintenance Supervisor, Maintenance Technician, Production Manager, AI System
- **Preconditions:** IoT sensors are installed on critical equipment; Data pipeline is operational; ML models are trained and deployed; Maintenance team has access to the dashboard.
- **Main Flow:**
  1. System continuously collects real-time sensor data from equipment.
  2. Data is processed through ML models to detect anomaly patterns.
  3. When a potential failure is predicted, system generates an alert.
  4. Alert is sent to Maintenance Supervisor with equipment details and urgency level.
  5. Supervisor reviews alert and creates maintenance work order.
  6. Maintenance Technician is assigned and receives equipment health report.
  7. Technician performs proactive maintenance based on predictions.
  8. Maintenance actions are logged in the system.
  9. System updates equipment health status and continues monitoring.
- **Alternate Flows:**
  - **False positive prediction:** Technician inspects, finds no issues, logs false positive, system uses feedback to retrain model.
  - **Critical imminent failure detected:** System sends immediate critical alert, production line is scheduled for shutdown, emergency team is dispatched.
- **Postconditions:** Equipment health status is updated; Maintenance actions are recorded; ML model performance is tracked.
- **Success Criteria:** >90% prediction accuracy; Alerts generated at least 24 hours before failure.

### UC-002: Automated Quality Inspection with Computer Vision
- **Actors:** Quality Assurance Manager, Quality Inspector, Production Manager, AI System
- **Preconditions:** Industrial cameras are installed; CV models are trained; Lighting is calibrated; Integration with line control system is established.
- **Main Flow:**
  1. Component arrives at inspection station.
  2. System triggers image capture from multiple angles.
  3. Images are processed by CV models in real-time.
  4. System analyzes images for known defect patterns.
  5. If no defects, component passes to next station.
  6. If defects detected, system classifies type and severity.
  7. Defective component is automatically routed to rework/scrap.
  8. Inspection results are logged with timestamp and images.
  9. Quality dashboard updates with real-time statistics.
- **Alternate Flows:**
  - **Uncertain defect detection:** System flags for manual review; Inspector makes final determination; decision is fed back to improve model.
  - **Camera/lighting malfunction:** System detects failure, line is paused, maintenance is notified, system switches to manual mode.
- **Postconditions:** Inspection results are recorded; Defective components are routed; Quality metrics are updated.
- **Success Criteria:** >95% inspection accuracy; Inspection time reduced to under 5 minutes per batch.

### UC-003: Production Process Optimization
- **Actors:** Production Manager, Manufacturing Engineer, Operations Director, AI System
- **Preconditions:** Production data is collected; Quality data is integrated; Optimization models are trained; Dashboard is available.
- **Main Flow:**
  1. System collects production parameters (speed, temp, pressure).
  2. System correlates parameters with quality outcomes and throughput.
  3. AI models identify optimal parameter combinations.
  4. System generates real-time recommendations for machine settings.
  5. Production Manager reviews and approves recommendations.
  6. Approved settings are automatically applied to equipment.
  7. System monitors results and adjusts recommendations.
  8. Production schedules are optimized based on availability.
  9. Resource allocation recommendations are generated.
- **Alternate Flows:**
  - **Settings conflict with safety limits:** System flags violation, blocks recommendation, notifies manager, provides alternatives.
  - **Multiple optimization goals conflict:** System presents trade-off analysis, engineer selects strategy, system adjusts.
- **Postconditions:** Optimal settings are applied; Schedule is updated; Performance is tracked.
- **Success Criteria:** Production capacity utilization increased to >90%; OEE increased to >75%.

### UC-004: Digital Twin Simulation and Analysis
- **Actors:** Manufacturing Engineer, Operations Director, Production Manager, Data Scientist
- **Preconditions:** Digital twin model is created; Real-time sync is established; Simulation engine is configured; UI is available.
- **Main Flow:**
  1. Digital twin updates with real-time production data.
  2. Engineer defines simulation scenario (e.g., new product).
  3. System runs simulation using current and historical data.
  4. Simulation predicts bottlenecks, resource needs, issues.
  5. Results are visualized with metrics and recommendations.
  6. Engineer adjusts parameters and re-runs simulation.
  7. Validated scenarios are saved for future reference.
  8. Digital twin is used to train AI models.
  9. What-if analysis is performed for equipment upgrades.
- **Alternate Flows:**
  - **Synchronization fails:** System detects issues, alerts IT, operates in last-known-good state, shows warnings.
  - **Results are inconclusive:** System identifies insufficient data, notifies Data Scientist, offers simplified simulations.
- **Postconditions:** Simulation results are documented; Twin state is saved; Decision support data is generated.
- **Success Criteria:** Enables risk-free testing; Reduces new product intro time by 30%.

### UC-005: Real-time Production Monitoring and Alerting
- **Actors:** Operations Director, Production Manager, Quality Assurance Manager, Maintenance Supervisor
- **Preconditions:** Data integration is complete; Dashboard is configured; Alert system is set up; Roles are defined.
- **Main Flow:**
  1. System aggregates data from SCADA, quality, and maintenance.
  2. Real-time dashboard displays status and metrics.
  3. KPIs are calculated (OEE, defect rate, throughput).
  4. System monitors for deviations from normal parameters.
  5. When anomalies are detected, intelligent alerts are generated.
  6. Alerts are routed to appropriate roles based on severity.
  7. Users can drill down for root cause analysis.
  8. Historical trend analysis is available.
  9. Automated reports are generated for handovers.
- **Alternate Flows:**
  - **Data source unavailable:** System detects loss, shows indicators, alerts IT, continues with available data.
  - **Alert fatigue:** System analyzes patterns, adjusts thresholds, allows customization, provides digests.
- **Postconditions:** Production status is visible; Issues are addressed; Data is preserved.
- **Success Criteria:** Visibility increased to 100% of floor; Faster response to issues.

### UC-006: AI Model Management and Continuous Improvement
- **Actors:** Data Scientist, IT Infrastructure Lead, Operations Director
- **Preconditions:** MLOps platform is deployed; Initial models are in production; Training pipeline is established; Metrics are defined.
- **Main Flow:**
  1. System monitors performance of all production AI models.
  2. Model accuracy, precision, and recall are tracked.
  3. When performance degrades, retraining is triggered.
  4. New model versions are trained with latest data.
  5. Models undergo validation and testing before deployment.
  6. A/B testing compares new model with current.
  7. Successful models are promoted with version control.
  8. Model drift is detected and addressed automatically.
  9. Explainability reports are generated.
  10. Governance and audit logs are maintained.
- **Alternate Flows:**
  - **Retraining fails:** System logs failure, notifies Data Scientist, previous model remains, analysis is initiated.
  - **New model performs worse:** System automatically rolls back, analysis is conducted, architecture is adjusted.
- **Postconditions:** Model performance is optimized; Versions are tracked; Governance is met.
- **Success Criteria:** Models maintain >90% accuracy; Continuous improvement is enabled.

## 7. Functional Requirements
### Predictive Maintenance
- FR-01: The system shall continuously ingest real-time data streams from at least 500 IoT sensors.
- FR-02: The system shall apply machine learning models to sensor data to predict equipment failures at least 24 hours in advance.
- FR-03: The system shall generate automated alerts and work orders in the CMMS upon predicting a failure.
- FR-04: The system shall provide a dashboard visualizing the real-time health status of all monitored equipment.
- FR-05: The system shall log all maintenance activities and use them as feedback for model retraining.

### Automated Quality Inspection
- FR-06: The system shall trigger image capture from industrial cameras as components enter the inspection station.
- FR-07: The system shall analyze captured images using computer vision models to identify defects with >95% accuracy.
- FR-08: The system shall automatically route components flagged as defective to the designated rework or scrap area.
- FR-09: The system shall log all inspection results, including images and defect classifications, to a time-series database.
- FR-10: The system shall flag components with uncertain defect detection for manual review.

### Production Process Optimization
- FR-11: The system shall collect real-time production parameters (e.g., speed, temperature, pressure).
- FR-12: The system shall correlate production parameters with quality outcomes and throughput data.
- FR-13: The system shall generate recommendations for optimal machine settings to maximize OEE.
- FR-14: The system shall allow a Production Manager to approve or reject recommended settings before they are applied.
- FR-15: The system shall generate optimized production schedules based on equipment availability and demand forecasts.

### Digital Twin
- FR-16: The system shall maintain a digital twin model that synchronizes with the physical production floor state in near real-time.
- FR-17: The system shall allow users to define and run "what-if" simulation scenarios.
- FR-18: The system shall provide visualizations of simulation results, including predicted bottlenecks and resource utilization.
- FR-19: The system shall use the digital twin to generate synthetic data for training AI models.

### Monitoring and Alerting
- FR-20: The system shall provide a unified dashboard displaying KPIs for OEE, defect rate, throughput, and equipment status.
- FR-21: The system shall allow users to define custom thresholds for KPIs and performance metrics.
- FR-22: The system shall generate and route intelligent alerts to the appropriate stakeholders based on pre-defined rules.
- FR-23: The system shall provide historical trend analysis and drill-down capabilities for root cause analysis.

### Platform and Data
- FR-24: The system shall integrate with the existing legacy SCADA system via a middleware solution.
- FR-25: The system shall store all raw and processed data in a centralized data lake.
- FR-26: The system shall support real-time data streaming with a latency of less than 5 seconds.
- FR-27: The system shall enforce role-based access control for all users and functions.
- FR-28: The system shall log all user actions and system events for audit purposes.

## 8. Non-Functional Requirements
### Performance
- **Response Time:** The system shall render dashboard visualizations in under 3 seconds.
- **Throughput:** The system shall process data from 500+ sensors and 15 cameras concurrently without data loss.
- **Scalability:** The architecture must support scaling to accommodate data from a 50% increase in production equipment and future multi-site deployment.
- **Data Latency:** Real-time analytics and alerts must be generated within 5 seconds of event occurrence.

### Security
- **Authentication:** Users shall authenticate via the company's existing Active Directory/LDAP service.
- **Authorization:** Access to data and functions shall be governed by Role-Based Access Control (RBAC).
- **Data Protection:** All data, both in transit and at rest, shall be encrypted using AES-256 standards.
- **Compliance:** The system must comply with IATF 16949 and relevant data protection regulations.
- **Network Security:** The production network shall be segmented from the corporate network, with strict firewall rules between them.

### Usability
- **User Experience:** The interface must be intuitive for plant floor staff with varying levels of technical proficiency, minimizing training time.
- **Accessibility:** The web-based interface shall conform to WCAG 2.1 AA accessibility standards.
- **Customization:** Users shall be able to personalize their dashboard layouts and alert preferences.

### Reliability
- **Uptime:** Production-critical components of the system shall achieve 99.5% uptime.
- **Error Handling:** The system shall gracefully handle data quality issues and sensor failures without crashing.
- **Disaster Recovery:** A disaster recovery plan shall be in place, with a Recovery Time Objective (RTO) of 4 hours and a Recovery Point Objective (RPO) of 1 hour.

### Maintainability
- **Code Quality:** All custom-developed code must follow industry best practices and pass automated quality gates.
- **Documentation:** All system components, APIs, and data models must be thoroughly documented.
- **APIs:** The system shall expose well-documented RESTful APIs for integration with other enterprise systems.

## 9. Technical Architecture
### System Components
- **Edge Layer:** 25 Edge Computing Nodes for local data ingestion, preprocessing, and low-latency inference. 500+ IoT sensors (vibration, temperature, pressure) and 15 industrial cameras.
- **Data Ingestion & Streaming:** Apache Kafka for handling high-volume real-time data streams from the edge to the cloud.
- **Cloud Platform:** Microsoft Azure will serve as the primary cloud platform.
- **Data Storage:** Azure Data Lake Storage for raw data, Azure SQL Database for structured data, and Azure Time Series Insights for time-series data.
- **Data Processing:** Azure Databricks (Apache Spark) for large-scale batch processing and feature engineering.
- **AI/ML Platform:** Azure Machine Learning for model training, deployment, versioning, and monitoring (MLOps).
- **Application & Visualization:** A web-based dashboard built with modern frameworks (e.g., React) and hosted on Azure App Service.
- **Integration Layer:** Azure API Management for exposing APIs and an on-premises data gateway for integrating with the legacy SCADA system.

### Technology Stack
- **Cloud:** Azure
- **IoT:** Azure IoT Hub, Azure IoT Edge
- **Data:** Azure Data Lake, Azure SQL DB, Apache Kafka, Apache Spark
- **AI/ML:** Azure ML, TensorFlow/PyTorch
- **Web App:** React, .NET Core
- **Database:** Azure SQL, Time Series DB

### Integration Points
- **Legacy SCADA (2012):** Integration via an on-premises data gateway and custom middleware/OPC-UA adapters.
- **CMMS:** API-based integration for automated work order creation.
- **ERP (for scheduling):** API-based integration for pulling production orders and pushing schedules.

### Data Flow
1. Sensors/Cameras -> Edge Nodes (pre-processing) -> Azure IoT Hub -> Kafka Topic.
2. Kafka -> Azure Stream Analytics (real-time analytics) -> Power BI / Dashboard (alerts).
3. Kafka -> Data Lake (raw storage) -> Databricks/Spark (batch processing) -> Azure ML (model training).
4. Azure ML -> Deployed models as web services -> Called by Stream Analytics/App Service for inference.
5. App Service -> SQL DB (storing results, user data) -> Power BI / Dashboard.

### Deployment Architecture
A hybrid cloud model. Edge nodes and cameras on-premises. Data processing, storage, AI/ML, and dashboards hosted on Azure. The system will be deployed across multiple availability zones to ensure high availability.

## 10. Acceptance Criteria
- **AC-01:** A Maintenance Supervisor can view a list of equipment predicted to fail within the next 7 days, sorted by urgency.
- **AC-02:** The system correctly identifies and routes at least 95% of defective components during a 24-hour production run.
- **AC-03:** The end-to-end latency from a sensor event to a corresponding alert on a dashboard is under 5 seconds.
- **AC-04:** A Manufacturing Engineer can successfully run a simulation of a new product introduction and receive a report on predicted bottlenecks.
- **AC-05:** The Operations Director can view a real-time OEE metric for any production line, accurate within 2%.
- **AC-06:** The system maintains 99.5% uptime over a 30-day continuous period.
- **AC-07:** The predictive maintenance model demonstrates a prediction accuracy of >90% on a hold-out test dataset.
- **AC-08:** The system successfully ingests and stores data from the legacy SCADA system without data loss.
- **AC-09:** A user with "Production Manager" role cannot access maintenance scheduling functions.
- **AC-10:** The system generates a weekly performance report that quantifies cost savings from reduced downtime and scrap.

## 11. Success Metrics
### User Adoption Metrics
- **Daily Active Users (DAU):** Target >85% of target user base (Production, Quality, Maintenance staff) within 3 months of full rollout.
- **Feature Adoption Rate:** Track usage of key features (e.g., alert acknowledgment, simulation runs). Target >70% adoption for core features.

### Business Impact Metrics
- **Unplanned Downtime:** Reduction from 2,400 hours to <1,200 hours annually.
- **Overall Equipment Effectiveness (OEE):** Increase from 68% to >75%.
- **Defect Rate:** Reduction from 8.2% to <3%.
- **Inspection Time:** Reduction from 45 minutes to <5 minutes per batch.
- **Cost Savings:** Track $ saved from reduced maintenance, scrap, and energy costs. Target >$3M annually.
- **ROI:** Achieve a positive return on investment within 24 months.

### Technical Performance Metrics
- **System Uptime:** Maintain 99.5% uptime for critical components.
- **Data Latency:** Maintain <5 second latency for real-time analytics.
- **Model Accuracy:** Maintain >90% accuracy for predictive maintenance and >95% for quality inspection.
- **Data Integration:** 100% of identified data sources successfully integrated.

### User Satisfaction Metrics
- **Net Promoter Score (NPS):** Conduct quarterly surveys. Target NPS >+40.
- **User Support Tickets:** Monitor volume and type of support tickets. Target a reduction in "how-to" tickets over time.

## 12. Timeline & Milestones
### Phase 1: Foundation & Predictive Maintenance (Months 1-6)
- **Scope:** Infrastructure setup (Azure, networking), sensor installation on pilot equipment, data pipeline development, initial predictive maintenance model for top 5 critical machines, basic monitoring dashboard.
- **Milestones:**
  - M1: Cloud environment and data lake provisioned (Month 1).
  - M2: Sensors installed on pilot line and data streaming confirmed (Month 2).
  - M3: Initial predictive maintenance model deployed for testing (Month 3).
  - M4: Basic dashboard for OEE and equipment health live (Month 4).
  - M5: Pilot validation and model tuning complete (Month 5).
  - M6: Phase 1 go-live for pilot line (Month 6).

### Phase 2: Quality & Optimization (Months 7-18)
- **Scope:** Scale predictive maintenance to all critical equipment, implement automated quality inspection, develop production optimization models, enhance dashboard capabilities.
- **Milestones:**
  - M9: Automated quality inspection system deployed on one major line (Month 9).
  - M12: Predictive maintenance scaled to 80%