# Oracle Cloud Services Inventory

**Document Version:** 1.0
**Last Updated:** November 4, 2025
**Purpose:** Comprehensive catalog of Oracle Cloud Infrastructure (IaaS), Platform (PaaS), and Application (SaaS) services

---

## Table of Contents

1. [Infrastructure Services (IaaS)](#infrastructure-services-iaas)
2. [Platform Services (PaaS)](#platform-services-paas)
3. [Application Services (SaaS)](#application-services-saas)
4. [Pricing Models](#pricing-models)
5. [Source References](#source-references)

---

## Infrastructure Services (IaaS)

### Compute Services

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-COMP-001 | Virtual Machine Instances | IaaS - Compute | Flexible compute instances with various shapes for general purpose workloads | OCPU per hour | Various by shape | [Oracle Compute](https://www.oracle.com/cloud/compute/) |
| OCI-COMP-002 | Bare Metal Instances - AMD | IaaS - Compute | Dedicated bare metal servers with AMD processors without hypervisor | OCPU per hour | Starting at $0.15/OCPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-COMP-003 | Bare Metal Instances - Intel | IaaS - Compute | Dedicated bare metal servers with Intel processors without hypervisor | OCPU per hour | Starting at $0.15/OCPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-COMP-004 | Bare Metal Instances - Ampere | IaaS - Compute | Arm-based bare metal servers with Ampere processors | OCPU per hour | Starting at $0.01/OCPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-COMP-005 | GPU Instances - H100 | IaaS - Compute | Hardware-accelerated GPU instances with NVIDIA H100 for AI/ML workloads | GPU per hour | $6.38/GPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-COMP-006 | GPU Instances - H200 | IaaS - Compute | Hardware-accelerated GPU instances with NVIDIA H200 for AI/ML workloads | GPU per hour | $7.47/GPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-COMP-007 | GPU Instances - B200 Blackwell | IaaS - Compute | Next-gen GPU instances with NVIDIA B200 Blackwell architecture | GPU per hour | $10.58/GPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-COMP-008 | Dense I/O Shapes | IaaS - Compute | High-performance instances with locally attached NVMe SSDs for big data | OCPU per hour | Various by shape | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-COMP-009 | HPC Shapes | IaaS - Compute | High-frequency processor cores for high-performance computing workloads | OCPU per hour | Various by shape | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-COMP-010 | Preemptible Instances | IaaS - Compute | Cost-optimized compute instances subject to reclamation with 30-second notice | OCPU per hour | 50% of regular instance | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-COMP-011 | Capacity Reservations | IaaS - Compute | Reserved compute capacity in specific availability domains | OCPU per hour | 85% of regular instance | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-COMP-012 | Compute Cloud@Customer | IaaS - Compute | On-premises compute cloud with OCI services in customer data center | OCPU per hour | $0.30-$0.60/OCPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-COMP-013 | Managed Service for Mac | IaaS - Compute | Managed macOS environments for iOS/macOS app development | Mac server per hour | $1.40-$2.00/Mac-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |

### Storage Services

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-STOR-001 | Object Storage | IaaS - Storage | Highly durable, scalable storage for unstructured data with API access | GB storage per month | $0.0255/GB-month | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-STOR-002 | Block Volume | IaaS - Storage | Persistent block storage volumes for compute instances with high IOPS | GB storage per month | $0.0255/GB-month | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-STOR-003 | Archive Storage | IaaS - Storage | Low-cost, long-term storage for data that is rarely accessed | GB storage per month | $0.004/GB-month | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-STOR-004 | File Storage | IaaS - Storage | Shared file system storage accessible from VCN instances via NFS | GB storage per month | Various pricing tiers | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-STOR-005 | Block Volume Performance Units | IaaS - Storage | Additional IOPS and throughput for block volumes | Performance unit-hour | Variable by tier | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |

### Network Services

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-NET-001 | Virtual Cloud Network (VCN) | IaaS - Network | Isolated private network with customizable subnets and routing | No charge | N/A - Free | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-NET-002 | Load Balancer | IaaS - Network | Automatic traffic distribution across instances with health checking | Base instance-hour + bandwidth | $0.025/hour + $0.0073/Mbps-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-NET-003 | Network Load Balancer | IaaS - Network | Layer 4 load balancing for ultra-high throughput and low latency | Base instance-hour + LCU | Variable pricing | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-NET-004 | FastConnect - 1 Gbps | IaaS - Network | Dedicated private connectivity from customer premises to OCI | Port-hour | $0.30/port-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-NET-005 | FastConnect - 10 Gbps | IaaS - Network | High-bandwidth dedicated private connectivity to OCI | Port-hour | $0.60/port-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-NET-006 | FastConnect - 100 Gbps | IaaS - Network | Ultra-high-bandwidth dedicated private connectivity to OCI | Port-hour | $2.00/port-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-NET-007 | Data Transfer - Outbound | IaaS - Network | Outbound data transfer from OCI to internet (first 10TB free monthly) | GB transferred | Free up to 10TB, then $0.0085/GB | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-NET-008 | DNS Service | IaaS - Network | Highly available and scalable domain name system with global anycast | Per million queries | $0.40/million queries | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-NET-009 | VPN Connect | IaaS - Network | IPSec VPN connectivity between on-premises networks and OCI VCN | Connection-hour | Variable pricing | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-NET-010 | Service Gateway | IaaS - Network | Private access to Oracle services without internet gateway | No charge | N/A - Free | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-NET-011 | Dynamic Routing Gateway (DRG) | IaaS - Network | Virtual router for private network connectivity between VCNs | No charge | N/A - Free | [OCI Documentation](https://docs.oracle.com/iaas/) |

---

## Platform Services (PaaS)

### Database Services

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-DB-001 | Autonomous Database - Data Warehouse | PaaS - Database | Self-driving, self-securing database optimized for analytics workloads | ECPU per hour | $0.80-$2.40/ECPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DB-002 | Autonomous Database - Transaction Processing | PaaS - Database | Self-managing database optimized for OLTP with automatic tuning | ECPU per hour | $0.80-$2.40/ECPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DB-003 | Autonomous Database - JSON | PaaS - Database | Document database with native JSON support and ACID transactions | ECPU per hour | $0.80-$2.40/ECPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DB-004 | Base Database Service - Standard | PaaS - Database | Oracle Database on VM or bare metal with Standard Edition features | ECPU per hour | B111585: $0.45/ECPU-hour | [Oracle Service Descriptions](https://www.oracle.com/contracts/docs/paas-iaas-public-cloud-2140609.pdf) |
| OCI-DB-005 | Base Database Service - Enterprise | PaaS - Database | Full-featured Oracle Database with Enterprise Edition capabilities | ECPU per hour | B111586: $0.90/ECPU-hour | [Oracle Service Descriptions](https://www.oracle.com/contracts/docs/paas-iaas-public-cloud-2140609.pdf) |
| OCI-DB-006 | Base Database Service - High Performance | PaaS - Database | Database with advanced performance, security, and availability features | ECPU per hour | B111587: $3.60/ECPU-hour | [Oracle Service Descriptions](https://www.oracle.com/contracts/docs/paas-iaas-public-cloud-2140609.pdf) |
| OCI-DB-007 | Base Database Service - BYOL | PaaS - Database | Bring Your Own License option for Oracle Database on OCI | ECPU per hour | B111588: $0.18/ECPU-hour | [Oracle Service Descriptions](https://www.oracle.com/contracts/docs/paas-iaas-public-cloud-2140609.pdf) |
| OCI-DB-008 | Exadata Database Service | PaaS - Database | Oracle Database on Exadata infrastructure with extreme performance | ECPU per hour | $0.36-$4.50/ECPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DB-009 | MySQL HeatWave | PaaS - Database | MySQL database with in-memory query acceleration for analytics | ECPU per hour | $0.90-$1.50/ECPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DB-010 | MySQL HeatWave Lakehouse | PaaS - Database | Query data across MySQL, object storage, and external databases | Capacity per hour | $1.50/capacity-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DB-011 | NoSQL Database Cloud | PaaS - Database | Fully managed NoSQL database for low-latency, high-scale applications | Read/write units + storage | Variable tiered pricing | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DB-012 | Database Migration | PaaS - Database | Tools and services for migrating databases to OCI | OCPU per hour | Variable pricing | [OCI Documentation](https://docs.oracle.com/iaas/) |

### AI and Machine Learning Services

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-AI-001 | Generative AI Service | PaaS - AI/ML | Access to foundation models for text generation, chat, and embeddings | Per token/character | $0.0000002/character | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-AI-002 | Generative AI Dedicated Clusters | PaaS - AI/ML | Private deployment of large language models with dedicated compute | Unit-hours | 744 unit-hour minimum | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-AI-003 | Data Science Service | PaaS - AI/ML | Collaborative platform for building, training, and deploying ML models | OCPU/GPU per hour | Variable by shape | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-AI-004 | Anomaly Detection | PaaS - AI/ML | Automated detection of anomalies in time-series data using ML | Data points processed | Free tier: 100M/month | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-AI-005 | Speech Service | PaaS - AI/ML | Speech-to-text transcription with speaker diarization | Per transaction (1000s) | Tiered pricing | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-AI-006 | Vision Service | PaaS - AI/ML | Image analysis, object detection, and document analysis with AI | Per transaction (1000s) | Tiered pricing | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-AI-007 | Language Service | PaaS - AI/ML | Natural language processing for text analysis and entity extraction | Per transaction (1000s) | Tiered pricing | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-AI-008 | Digital Assistant | PaaS - AI/ML | Platform for building conversational AI chatbots and virtual assistants | Per 5000 messages/hour | $0.24/5000 messages | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-AI-009 | Document Understanding | PaaS - AI/ML | Automated document classification, key-value extraction, and OCR | Per page processed | Tiered pricing | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |

### Analytics and Business Intelligence

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-ANLYT-001 | Oracle Analytics Cloud | PaaS - Analytics | Self-service analytics platform with visualization and data preparation | User per month OR OCPU per hour | Variable by edition | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-ANLYT-002 | Essbase | PaaS - Analytics | Multidimensional database for financial planning and analysis | OCPU per hour | Variable pricing | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-ANLYT-003 | Data Flow | PaaS - Analytics | Serverless Apache Spark service for big data processing | OCPU per hour | Variable pricing | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-ANLYT-004 | Data Catalog | PaaS - Analytics | Metadata management and data discovery service | No charge | N/A - Free | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-ANLYT-005 | Data Science Notebooks | PaaS - Analytics | Jupyter notebook environment for collaborative data science | OCPU per hour | Included with Data Science | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |

### Integration Services

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-INTG-001 | Oracle Integration Cloud (OIC) | PaaS - Integration | Pre-built adapters and process automation for application integration | Per 5000 messages/hour | $0.18-$0.36/5000 messages | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-INTG-002 | Data Integration | PaaS - Integration | ETL and data pipeline orchestration with visual designer | Workspace-hour + GB processed | $0.18/workspace-hour + $0.90/GB | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-INTG-003 | GoldenGate Cloud | PaaS - Integration | Real-time data replication and integration across heterogeneous systems | OCPU per hour | $0.45-$0.90/OCPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-INTG-004 | API Gateway | PaaS - Integration | Managed service for deploying, securing, and managing APIs | Per million requests | Tiered pricing | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-INTG-005 | Streaming with Kafka | PaaS - Integration | Managed Apache Kafka-compatible streaming service for real-time data | OCPU per hour | $0.0465/OCPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-INTG-006 | Process Automation | PaaS - Integration | Low-code workflow automation and business process management | Included with OIC | Part of OIC pricing | [Oracle Integration](https://www.jadeglobal.com/oracle/oracle-cloud-service/oracle-cloud-paas-and-integration-services) |
| OCI-INTG-007 | Service Bus | PaaS - Integration | Enterprise service bus for message routing and transformation | OCPU per hour | Legacy service | [Oracle Integration](https://www.jadeglobal.com/oracle/oracle-cloud-service/oracle-cloud-paas-and-integration-services) |
| OCI-INTG-008 | Managed File Transfer | PaaS - Integration | Secure file exchange between systems with tracking and monitoring | Included with OIC | Part of OIC pricing | [Oracle Integration](https://www.jadeglobal.com/oracle/oracle-cloud-service/oracle-cloud-paas-and-integration-services) |

### Developer Services

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-DEV-001 | Oracle APEX | PaaS - Developer | Low-code application development platform for database-centric apps | ECPU per hour | $0.18/ECPU-hour (free tier available) | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DEV-002 | Functions | PaaS - Developer | Serverless functions platform based on open-source Fn Project | Invocations + GB-seconds | First 2M invocations free + $0.00001417/GB-second | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DEV-003 | DevOps Service | PaaS - Developer | CI/CD pipelines, artifact repository, and deployment automation | Build minutes + storage | No compute charges for pipelines | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DEV-004 | Container Registry | PaaS - Developer | Private Docker registry for storing and distributing container images | GB storage per month | Included with OCI subscription | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-DEV-005 | Container Engine for Kubernetes (OKE) | PaaS - Developer | Managed Kubernetes service for container orchestration | Worker node compute only | Charged at compute rates | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-DEV-006 | Visual Builder | PaaS - Developer | Drag-and-drop development of web and mobile apps with REST APIs | Instance per hour | Variable pricing | [Oracle PaaS](https://xtglobal.com/oracle-cloud/paas/) |
| OCI-DEV-007 | Application Container Cloud | PaaS - Developer | Platform for deploying Java, Node.js, PHP, Python applications | OCPU per hour | Variable pricing | [Oracle PaaS](https://xtglobal.com/oracle-cloud/paas/) |
| OCI-DEV-008 | Mobile Cloud | PaaS - Developer | Backend services for mobile applications with offline sync | User per month | Variable pricing | [Oracle PaaS](https://xtglobal.com/oracle-cloud/paas/) |
| OCI-DEV-009 | Blockchain Platform | PaaS - Developer | Managed blockchain network with Hyperledger Fabric | OCPU per hour | Variable pricing | [Oracle Blockchain](https://docs.oracle.com/en/cloud/paas/blockchain-cloud/digitalassetsoci/) |

### Security and Identity Services

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-SEC-001 | Identity and Access Management (IAM) | PaaS - Security | User authentication, authorization, and federation | No charge | N/A - Free | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-SEC-002 | Data Safe | PaaS - Security | Security assessment, user assessment, and activity auditing for databases | Per target DB per month | $0.30-$0.90/target-month (tiered) | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-SEC-003 | Vault | PaaS - Security | Centralized key management and secrets storage with HSM backing | Per key version + crypto operations | Tiered pricing | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-SEC-004 | Web Application Firewall (WAF) | PaaS - Security | Protection against web attacks, DDoS, and bot traffic | Per million requests | Tiered pricing | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-SEC-005 | Cloud Guard | PaaS - Security | Automated threat detection and remediation for OCI resources | No charge | N/A - Free | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-SEC-006 | Security Zones | PaaS - Security | Policy-based security posture management preventing misconfigurations | No charge | N/A - Free | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-SEC-007 | Certificates | PaaS - Security | SSL/TLS certificate management and automatic renewal | Per certificate | Variable pricing | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-SEC-008 | Bastion | PaaS - Security | Secure access to private resources without public IPs | Session-hour | Variable pricing | [OCI Documentation](https://docs.oracle.com/iaas/) |

### Observability and Management

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-OBS-001 | Monitoring | PaaS - Observability | Metrics collection, alarming, and notification for OCI resources | Million datapoints | First 500M ingestion free + $0.018/M retrieval | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-OBS-002 | Logging | PaaS - Observability | Centralized log management with search and analysis | GB ingested + stored | First 10GB free + $0.05/GB | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-OBS-003 | Application Performance Monitoring (APM) | PaaS - Observability | End-to-end transaction tracing and diagnostics for applications | Per 10 monitored resources/hour | $0.09-$0.18/10 resources-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-OBS-004 | Stack Monitoring | PaaS - Observability | Application topology discovery and monitoring across stack | Per 10 monitored resources/hour | $0.09-$0.18/10 resources-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-OBS-005 | Notifications | PaaS - Observability | Event-driven notifications via email, SMS, Slack, PagerDuty | Per million messages | Tiered pricing | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-OBS-006 | Events | PaaS - Observability | Event-driven automation responding to OCI resource state changes | No charge | N/A - Free | [OCI Documentation](https://docs.oracle.com/iaas/) |

### Disaster Recovery and Backup

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-DR-001 | Full Stack Disaster Recovery | PaaS - DR | Orchestrated disaster recovery for entire application stacks | ECPU per hour | $0.045/ECPU-hour | [Oracle Price List](https://www.oracle.com/cloud/price-list/) |
| OCI-DR-002 | Database Backup | PaaS - DR | Automated backup for database services with point-in-time recovery | GB storage per month | Included with database service | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-DR-003 | Block Volume Backup | IaaS - DR | Automated backup of block volumes with incremental snapshots | GB storage per month | Same as block volume storage | [OCI Documentation](https://docs.oracle.com/iaas/) |
| OCI-DR-004 | Object Storage Replication | IaaS - DR | Cross-region replication of object storage buckets | GB replicated | Same as object storage + transfer | [OCI Documentation](https://docs.oracle.com/iaas/) |

### Content and Experience

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-CMS-001 | Content Management | PaaS - Content | Enterprise content management for digital experiences | User per month | Variable pricing | [Oracle PaaS](https://xtglobal.com/oracle-cloud/paas/) |
| OCI-CMS-002 | Sites Cloud Service | PaaS - Content | Web content management for creating responsive websites | User per month | Variable pricing | [Oracle PaaS](https://xtglobal.com/oracle-cloud/paas/) |

### Support Services

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-SUPP-001 | Cloud Priority Support - Base Fee | PaaS - Support | Enhanced technical support for PaaS services with faster response | Base fee | B85996 | [Oracle Service Descriptions](https://www.oracle.com/contracts/docs/paas-iaas-public-cloud-2140609.pdf) |
| OCI-SUPP-002 | Cloud Priority Support - Metered | PaaS - Support | Usage-based priority support charges for PaaS | Percentage of usage | B85997 | [Oracle Service Descriptions](https://www.oracle.com/contracts/docs/paas-iaas-public-cloud-2140609.pdf) |

---

## Application Services (SaaS)

### Enterprise Resource Planning (ERP)

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-ERP-001 | Fusion Financials Cloud | SaaS - ERP | Complete financial management including GL, AP, AR, and cash management | User per month | Variable by edition | [Oracle Fusion Price List](https://www.oracle.com/mx/a/ocom/docs/corporate/pricing/oracle-fusion-cloud-global-price-list.pdf) |
| OCI-ERP-002 | Fusion Procurement Cloud | SaaS - ERP | Source-to-pay procurement with supplier management and contracts | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-ERP-003 | Fusion Project Management Cloud | SaaS - ERP | Project planning, execution, and financial tracking | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-ERP-004 | Fusion Risk Management Cloud | SaaS - ERP | Enterprise risk management and compliance | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-ERP-005 | Fusion Enterprise Performance Management | SaaS - ERP | Financial planning, budgeting, and consolidation | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-ERP-006 | Accounting Hub Cloud | SaaS - ERP | Centralized accounting platform for subledger accounting | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-ERP-007 | Fusion AI Agents | SaaS - ERP | AI-powered automation agents for ERP processes | Additional tokens | B111575 | [Oracle Fusion Price List](https://www.oracle.com/mx/a/ocom/docs/corporate/pricing/oracle-fusion-cloud-global-price-list.pdf) |

### Human Capital Management (HCM)

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-HCM-001 | Fusion HCM - Core HR | SaaS - HCM | Complete HR management from hire to retire with employee records | Employee per month | Variable by edition | [Oracle Cloud HCM](https://en.wikipedia.org/wiki/Oracle_Cloud_HCM) |
| OCI-HCM-002 | Fusion HCM - Recruiting | SaaS - HCM | Talent acquisition with candidate tracking and interview scheduling | Employee per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-HCM-003 | Fusion HCM - Talent Management | SaaS - HCM | Performance management, goals, succession planning, and learning | Employee per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-HCM-004 | Fusion HCM - Payroll | SaaS - HCM | Global payroll processing with compliance and tax management | Employee per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-HCM-005 | Fusion HCM - Workforce Management | SaaS - HCM | Time tracking, absence management, and scheduling | Employee per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-HCM-006 | Fusion HCM - Compensation | SaaS - HCM | Total compensation planning and administration | Employee per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-HCM-007 | Fusion HCM - Benefits | SaaS - HCM | Benefits enrollment, administration, and employee self-service | Employee per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |

### Supply Chain Management (SCM)

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-SCM-001 | Fusion Supply Chain Planning | SaaS - SCM | Demand planning, supply planning, and sales & operations planning | User per month | Variable by edition | [Oracle Cloud SCM](https://www.oracle.com/scm/) |
| OCI-SCM-002 | Fusion Inventory Management | SaaS - SCM | Real-time inventory tracking and warehouse management | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-SCM-003 | Fusion Manufacturing | SaaS - SCM | Production scheduling, execution, and quality management | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-SCM-004 | Fusion Order Management | SaaS - SCM | Quote-to-cash order orchestration across channels | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-SCM-005 | Fusion Logistics | SaaS - SCM | Transportation management and global trade compliance | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-SCM-006 | Fusion Product Lifecycle Management | SaaS - SCM | Product design, change management, and collaboration | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |
| OCI-SCM-007 | Fusion Maintenance | SaaS - SCM | Asset management and predictive maintenance | User per month | Variable by edition | [Oracle Fusion Applications](https://docs.oracle.com/en/cloud/saas/index.html) |

### Customer Experience (CX)

| Service ID | Service Name | Category | Description | Procurement Metric | SKU/Part Number | Source |
|------------|--------------|----------|-------------|-------------------|-----------------|--------|
| OCI-CX-001 | Fusion Sales Cloud | SaaS - CX | Sales force automation with opportunity and pipeline management | User per month | Variable by edition | [Oracle Cloud CX](https://www.oracle.com/cx/) |
| OCI-CX-002 | Fusion Service Cloud | SaaS - CX | Customer service and support with case management and knowledge base | User per month | Variable by edition | [Oracle Customer Service](https://www.oracle.com/assets/rightnow-service-descriptions-1885273.pdf) |
| OCI-CX-003 | Fusion Marketing Cloud | SaaS - CX | Marketing automation, campaign management, and lead nurturing | Contact per month | Variable by edition | [Oracle Cloud CX](https://www.oracle.com/cx/) |
| OCI-CX-004 | Fusion Commerce Cloud | SaaS - CX | B2C and B2B e-commerce platform with order management | GMV or revenue-based | Variable by edition | [Oracle Commerce Cloud](https://docs.oracle.com/en/cloud/saas/cx-commerce/) |
| OCI-CX-005 | Fusion CPQ Cloud | SaaS - CX | Configure, price, quote for complex products and services | User per month | Variable by edition | [Oracle CPQ Cloud](https://www.oracle.com/assets/bmi-service-descriptions-2203257.pdf) |
| OCI-CX-006 | Fusion Loyalty Cloud | SaaS - CX | Customer loyalty program management with rewards | Member per month | Variable by edition | [Oracle Cloud CX](https://www.oracle.com/cx/) |
| OCI-CX-007 | Fusion Field Service Cloud | SaaS - CX | Field service management with scheduling and mobile workforce | User per month | Variable by edition | [Oracle Cloud CX](https://www.oracle.com/cx/) |

---

## Pricing Models

### Universal Credits Model

Oracle Universal Credits provide flexible consumption-based pricing:

| Pricing Model | Description | Commitment | Discount vs PAYG |
|---------------|-------------|------------|------------------|
| Pay As You Go (PAYG) | No minimum commitment, charged monthly for actual usage | None | Baseline (100%) |
| Annual Universal Credits | Prepaid credits with 12-month minimum commitment | 12 months | ~34% (66% of PAYG) |
| Multi-Year Universal Credits | Extended commitment with volume discounts | 2-5 years | Up to 50% |

### Key Pricing Metrics

| Metric | Description | Common Services |
|--------|-------------|-----------------|
| OCPU per hour | Oracle CPU (1 physical core = 2 vCPUs for x86) | Compute, PaaS services |
| ECPU per hour | Elastic CPU for databases (flexible sizing) | Autonomous DB, Base DB |
| GPU per hour | Graphics processing unit for AI/ML workloads | GPU Compute instances |
| GB per month | Gigabyte of storage capacity | Object, Block, Archive Storage |
| GB per hour | Gigabyte of memory per hour | Compute instances |
| User per month | Named or concurrent user license | SaaS applications |
| Transaction | API call, query, or processing operation | AI services, DNS |
| Message | Integration message or API invocation | OIC, Digital Assistant |

### Additional Cost Considerations

- **Data Transfer:** First 10 TB outbound per month is free
- **Support:** Enterprise-grade support included with base pricing (no extra technical support fees)
- **Support Rewards:** Earn $0.25-$0.33 in rewards per $1 spent on OCI
- **Global Pricing:** Same pricing across all regions (including government and dedicated regions)
- **BYOL:** Bring Your Own License options available for significant discounts

---

## Source References

### Primary Documentation Sources

1. **Oracle Cloud Price List**
   URL: https://www.oracle.com/cloud/price-list/
   Description: Official comprehensive pricing for all OCI services
   Access: Public

2. **Oracle PaaS and IaaS Public Cloud Services Pillar Document (September 2025)**
   URL: https://www.oracle.com/contracts/docs/paas_iaas_pub_cld_srvs_pillar_4021422.pdf
   Description: Technical service descriptions with SKU details
   Access: Public

3. **Oracle Fusion Cloud Global Price List (October 9, 2025)**
   URL: https://www.oracle.com/mx/a/ocom/docs/corporate/pricing/oracle-fusion-cloud-global-price-list.pdf
   Description: SaaS application pricing and SKUs
   Access: Public

4. **Oracle Cloud Infrastructure Documentation**
   URL: https://docs.oracle.com/iaas/
   Description: Complete technical documentation for IaaS services
   Access: Public

5. **Oracle Fusion Applications Documentation**
   URL: https://docs.oracle.com/en/cloud/saas/
   Description: Complete documentation for SaaS applications
   Access: Public

6. **Oracle Platform Services Documentation**
   URL: https://docs.oracle.com/en/cloud/paas/
   Description: Technical documentation for PaaS offerings
   Access: Public

### Additional Resources

7. **Oracle Universal Credits FAQ**
   URL: https://www.oracle.com/cloud/bring-your-own-license/faq/universal-credit-pricing.html
   Description: Detailed explanation of Universal Credits pricing model
   Access: Public

8. **Oracle Cloud Economics**
   URL: https://www.oracle.com/cloud/economics/
   Description: Cost comparison and ROI calculators
   Access: Public

9. **Oracle Service Descriptions - PaaS/IaaS (Non-UCM)**
   URL: https://www.oracle.com/contracts/docs/paas-iaas-public-cloud-2140609.pdf
   Description: Detailed SKU listings for PaaS and IaaS services
   Access: Public

10. **Oracle IaaS and PaaS Services Highlights**
    URL: https://www.oracle.com/cloud/iaas-paas/
    Description: Marketing overview of infrastructure and platform services
    Access: Public

---

## Document Maintenance

**Version History:**
- v1.0 (November 4, 2025): Initial comprehensive inventory created

**Update Frequency:** Quarterly or upon major Oracle Cloud releases

**Maintenance Notes:**
- SKU numbers may change; verify against current Oracle documentation
- Pricing is subject to change; check Oracle Price List for current rates
- New services are added regularly; this document should be updated quarterly
- Regional availability may vary for some services

**Document Owner:** [To be assigned]
**Last Verified:** November 4, 2025

---

*End of Document*
