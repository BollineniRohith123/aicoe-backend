# JD Edwards Data Structure Guide
**A Comprehensive Guide to Creating JD Edwards EnterpriseOne Data Structures for AI Use Cases**

**Published by:** AICOE (aicoe.io)
**Copyright:** © 2025 AICOE. All rights reserved.

---

## Table of Contents
1. [Document Metadata](#1-document-metadata)
2. [Data Source Configuration](#2-data-source-configuration)
3. [Business Modules](#3-business-modules)
4. [Data Tables (Structured Data)](#4-data-tables-structured-data)
5. [Data Objects (Unstructured Data)](#5-data-objects-unstructured-data)
6. [AI Use Case Mappings](#6-ai-use-case-mappings)
7. [Data Quality Rules](#7-data-quality-rules)
8. [Integration Specifications](#8-integration-specifications)
9. [JDE-Specific Conventions](#9-jde-specific-conventions)

---

## 1. Document Metadata

### Purpose
Define high-level information about the JD Edwards data structure template, including version control, source system identification, and compliance requirements.

### Sections

#### 1.1 Template Identification
**What to Include:**
- Template version number (semantic versioning)
- Creation and update dates (ISO 8601: YYYY-MM-DD)
- Description of template purpose
- Source system identification (JD Edwards EnterpriseOne)

**Example:**
```xml
<metadata>
  <template_version>1.0</template_version>
  <created_date>2025-01-16</created_date>
  <description>
    Machine-readable template for defining JDE data structures
    for AI use cases and HTML mockups
  </description>
  <based_on>JD Edwards EnterpriseOne Data Structure</based_on>
</metadata>
```

**What NOT to Include:**
- Specific JDE version numbers (e.g., "9.2.3.1")
- Environment details (development, test, production)
- Server names or instance identifiers
- Client-specific customization details

#### 1.2 Tags and Categorization
**What to Include:**
- JDE-specific tags
- Industry focus tags (pharmaceutical, manufacturing)
- Data structure categories
- AI integration tags

**Example:**
```yaml
tags:
  - "jd-edwards"
  - "erp-data"
  - "pharmaceutical"
  - "manufacturing"
  - "sales-orders"
  - "quality-control"
  - "ai-integration"
```

**What NOT to Include:**
- Client company names
- Project code names
- Implementation partner names
- Competitive system references

#### 1.3 Compliance and Regulatory Requirements
**What to Include:**
- Industry-specific regulations (FDA, GMP)
- Data protection regulations (GDPR)
- Audit trail requirements
- Record retention policies

**Example:**
```yaml
compliance:
  - "FDA 21 CFR Part 11"
  - "GMP Compliance"
  - "GDPR"
  - "ISO 13485 (Medical Devices)"
```

**What NOT to Include:**
- Audit findings or compliance gaps
- Legal interpretations
- Pending regulatory changes
- Company-specific compliance scores

---

## 2. Data Source Configuration

### Purpose
Define JD Edwards as the data source with connection methods, update frequency, and compliance requirements.

### Sections

#### 2.1 Source System Identification
**What to Include:**
- Unique source identifier
- System name (JD Edwards EnterpriseOne)
- Source type (ERP_DATABASE)
- Connection type

**Example:**
```xml
<data_source>
  <source_id>jde_erp_system</source_id>
  <source_name>JD Edwards EnterpriseOne</source_name>
  <source_type>ERP_DATABASE</source_type>
  <connection_type>DATABASE</connection_type>
</data_source>
```

**What NOT to Include:**
- Database server names (e.g., "JDEPROD01")
- Database instance names
- Connection strings or JDBC URLs
- IP addresses or hostnames

#### 2.2 Data Refresh and Update Patterns
**What to Include:**
- Real-time vs. batch processing
- Update frequency (hourly, daily, real-time)
- Data retention period (typically 7 years for pharma)
- Archival strategies

**Example:**
```xml
<is_real_time>false</is_real_time>
<update_frequency>BATCH_HOURLY</update_frequency>
<data_retention_years>7</data_retention_years>
```

**What NOT to Include:**
- Specific batch job names (e.g., "R55814")
- Cron expressions or scheduler configurations
- Processing window times
- Infrastructure capacity details

#### 2.3 Compliance Requirements
**What to Include:**
- FDA 21 CFR Part 11 (electronic records/signatures)
- GMP (Good Manufacturing Practice)
- GDPR (data protection)
- Industry-specific standards

**Example:**
```xml
<compliance_requirements>
  <requirement>FDA_21_CFR_PART_11</requirement>
  <requirement>GMP_COMPLIANCE</requirement>
  <requirement>GDPR</requirement>
  <requirement>DATA_INTEGRITY_ALCOA_PLUS</requirement>
</compliance_requirements>
```

**What NOT to Include:**
- Validation protocol numbers
- Internal SOP references
- Audit schedules
- Remediation plans

---

## 3. Business Modules

### Purpose
Organize JD Edwards data by business module (Sales Order Management, Manufacturing, Procurement, etc.) following JDE's functional organization.

### Sections

#### 3.1 JDE Module Definition
**What to Include:**
- Module identifier (matching JDE terminology)
- Module name (JDE functional area)
- Business description
- Relationship to JDE menu/application codes

**Example:**
```xml
<module>
  <module_id>sales_order_mgmt</module_id>
  <module_name>Sales Order Management</module_name>
  <module_description>
    Customer orders, pricing, and sales process management
    (JDE System Code 42)
  </module_description>
  <jde_system_code>42</jde_system_code>
</module>
```

**What NOT to Include:**
- Specific UBE (batch) or application numbers
- User-defined codes (UDCs) unless generic
- Custom menu paths
- Security roles or permissions

#### 3.2 Common JDE Business Modules
**What to Include (Select Relevant):**

| Module ID | Module Name | JDE System Code | Description |
|-----------|-------------|-----------------|-------------|
| `sales_order_mgmt` | Sales Order Management | 42 | Order processing, pricing |
| `manufacturing_mgmt` | Manufacturing Management | 31/48 | Work orders, shop floor |
| `procurement_mgmt` | Procurement Management | 43 | Purchase orders, suppliers |
| `inventory_mgmt` | Inventory Management | 41 | Stock, warehousing |
| `distribution_mgmt` | Distribution Management | 46 | Shipping, logistics |
| `financial_mgmt` | Financial Management | 09 | GL, AP, AR |
| `hr_payroll` | Human Resources & Payroll | 08 | Employee records |
| `quality_mgmt` | Quality Management | Custom | QC, testing, COA |

**Example:**
```xml
<business_modules>
  <module id="sales_order_mgmt">Sales Order Management (42)</module>
  <module id="manufacturing_mgmt">Manufacturing Management (31/48)</module>
  <module id="procurement_mgmt">Procurement Management (43)</module>
  <module id="inventory_mgmt">Inventory Management (41)</module>
</business_modules>
```

**What NOT to Include:**
- Custom module names specific to one implementation
- Deprecated or unused modules
- Third-party add-on modules
- Client-specific customizations

---

## 4. Data Tables (Structured Data)

### Purpose
Define JD Edwards database tables (F-tables) with columns, data types, and relationships following JDE naming conventions.

### Sections

#### 4.1 Table Metadata
**What to Include:**
- Unique table identifier (logical name)
- JDE table name with F-number (e.g., F4201)
- Table type (STRUCTURED)
- Master data vs. transactional classification
- Primary key specification

**Example:**
```xml
<table>
  <table_id>sales_orders_header</table_id>
  <table_name>Sales Orders (F4201)</table_name>
  <jde_table_code>F4201</jde_table_code>
  <table_type>STRUCTURED</table_type>
  <is_master_data>false</is_master_data>
  <is_transactional>true</is_transactional>
  <primary_key>order_number</primary_key>
</table>
```

**What NOT to Include:**
- Physical table names in database (e.g., "PRODDTA.F4201")
- Database owner/schema names
- Table space allocations
- Index definitions

#### 4.2 Common JDE Tables Reference

| Table ID | JDE Table | Description | Module |
|----------|-----------|-------------|--------|
| `sales_orders_header` | F4201 | Sales Order Header | 42 |
| `sales_orders_detail` | F4211 | Sales Order Detail | 42 |
| `customer_master` | F0301 | Customer Master | 03 |
| `address_book` | F0101 | Address Book Master | 01 |
| `work_orders` | F4801 | Work Order Master | 48 |
| `item_master` | F4101 | Item Master | 41 |
| `inventory_balance` | F4102 | Item Branch | 41 |
| `purchase_orders_header` | F4301 | Purchase Order Header | 43 |
| `account_ledger` | F0911 | Account Ledger | 09 |
| `batch_master` | F3111 | Lot Master | 31 |

#### 4.3 Column Definitions
**What to Include:**
- Column identifier (logical/business name)
- Column name (descriptive)
- JDE data dictionary item (optional but recommended)
- Data type (VARCHAR, DATE, DECIMAL, INTEGER)
- Length/precision specifications
- Nullable constraints
- Unique constraints
- Format patterns (JDE-style)
- Business description
- Allowed values (from UDCs if applicable)

**Example:**
```xml
<column>
  <column_id>order_number</column_id>
  <column_name>Order Number</column_name>
  <jde_data_item>DOCO</jde_data_item>
  <data_type>VARCHAR</data_type>
  <max_length>20</max_length>
  <is_nullable>false</is_nullable>
  <is_unique>true</is_unique>
  <format_pattern>SO[0-9]{8}</format_pattern>
  <business_description>
    Unique identifier for sales order (JDE Order Number)
  </business_description>
</column>

<column>
  <column_id>order_status</column_id>
  <column_name>Order Status</column_name>
  <jde_data_item>NXTR</jde_data_item>
  <data_type>VARCHAR</data_type>
  <max_length>2</max_length>
  <is_nullable>false</is_nullable>
  <allowed_values>
    <value code="10">Open</value>
    <value code="20">In Progress</value>
    <value code="30">Shipped</value>
    <value code="99">Completed</value>
  </allowed_values>
  <jde_udc>42/SS</jde_udc>
  <business_description>
    Current status of the order (UDC 42/SS)
  </business_description>
</column>
```

**What NOT to Include:**
- JDE internal field names (e.g., "SDDOCO", "SDNXTR")
- Database column physical names
- Display decimals or edit codes
- Form/application references
- Sample data values

#### 4.4 JDE Data Types Guide

| Data Type | JDE Type | Use For | Example |
|-----------|----------|---------|---------|
| VARCHAR | CHAR | Alphanumeric codes, IDs | "CUST000123" |
| INTEGER | N (no decimals) | Counts, codes | 42 |
| DECIMAL | N (with decimals) | Amounts, quantities | 1234.56 |
| DATE | JDE Date | Dates | 2025-01-16 (stored as Julian) |
| TIMESTAMP | JDE Date+Time | Audit timestamps | ISO8601 |

**JDE Date Convention:**
- JDE stores dates in Julian format (CYYDDD)
- For AI use cases, convert to ISO 8601 (YYYY-MM-DD)
- Always specify format as: `<format_pattern>YYYY-MM-DD</format_pattern>`

#### 4.5 Relationships Between Tables
**What to Include:**
- Relationship type (FOREIGN_KEY, ONE_TO_MANY)
- Related table reference
- Local and foreign column mapping
- Relationship name/description

**Example:**
```xml
<relationships>
  <relationship>
    <relationship_type>FOREIGN_KEY</relationship_type>
    <related_table>customer_master</related_table>
    <related_jde_table>F0301</related_jde_table>
    <local_column>customer_id</local_column>
    <foreign_column>customer_id</foreign_column>
    <relationship_name>order_to_customer</relationship_name>
    <jde_relationship>F4201.SDSHAN → F0301.ABAN8</jde_relationship>
  </relationship>
</relationships>
```

**What NOT to Include:**
- Database foreign key constraint names
- Index names used for joins
- Join strategies or optimization hints

---

## 5. Data Objects (Unstructured Data)

### Purpose
Define unstructured or semi-structured data that supplements JDE transactional data, particularly for pharmaceutical quality control, batch records, and compliance documents.

### Sections

#### 5.1 Object Metadata
**What to Include:**
- Unique object identifier
- Object name (business-friendly)
- Object type (UNSTRUCTURED)
- Storage format (JSON, XML, DOCUMENT_DB)
- Real-time vs. batch processing
- Relationship to JDE tables

**Example:**
```xml
<data_object>
  <object_id>quality_control_results</object_id>
  <object_name>Quality Control Test Results</object_name>
  <object_type>UNSTRUCTURED</object_type>
  <storage_format>JSON</storage_format>
  <is_real_time>false</is_real_time>
  <related_jde_table>F4801</related_jde_table>
</data_object>
```

**What NOT to Include:**
- File system paths or URLs
- Document management system details
- Storage bucket names
- Encryption specifications

#### 5.2 Pharmaceutical-Specific Data Objects

**Common Objects for Pharma/Manufacturing:**

| Object ID | Object Name | Purpose | Related JDE Table |
|-----------|-------------|---------|-------------------|
| `quality_control_results` | QC Test Results | Lab test data | F4801 (Work Orders) |
| `certificate_of_analysis` | Certificate of Analysis (COA) | Batch release documentation | F3111 (Lot Master) |
| `batch_manufacturing_record` | Batch Manufacturing Record | Production documentation | F4801 |
| `deviation_report` | Manufacturing Deviation | Quality deviations | F4801 |
| `stability_study_data` | Stability Study Results | Product stability testing | F4101 (Item Master) |
| `supplier_coa` | Supplier COA | Raw material certification | F4301 (PO Header) |

#### 5.3 Schema Definition for Unstructured Data
**What to Include:**
- Field names (JSON-style)
- Data types (string, number, boolean, array, object, datetime)
- Required field indicators
- Nested schemas for complex objects
- Format specifications
- Descriptions
- References to JDE tables

**Example:**
```xml
<schema_definition>
  <field>
    <field_name>batch_number</field_name>
    <data_type>string</data_type>
    <required>true</required>
    <description>
      Reference to manufacturing batch (links to F4801.DOCO)
    </description>
    <jde_reference>F4801.LITM</jde_reference>
  </field>

  <field>
    <field_name>test_date</field_name>
    <data_type>datetime</data_type>
    <required>true</required>
    <format>ISO8601</format>
    <description>Date and time when test was performed</description>
  </field>

  <field>
    <field_name>test_results</field_name>
    <data_type>array</data_type>
    <required>true</required>
    <description>Array of test result objects</description>
    <nested_schema>
      <field>
        <field_name>test_name</field_name>
        <data_type>string</data_type>
        <description>
          Name of quality test (e.g., "Dissolution", "Assay")
        </description>
      </field>
      <field>
        <field_name>result_value</field_name>
        <data_type>number</data_type>
        <description>Numeric test result</description>
      </field>
      <field>
        <field_name>specification_min</field_name>
        <data_type>number</data_type>
        <description>Lower specification limit</description>
      </field>
      <field>
        <field_name>specification_max</field_name>
        <data_type>number</data_type>
        <description>Upper specification limit</description>
      </field>
      <field>
        <field_name>pass_fail</field_name>
        <data_type>boolean</data_type>
        <description>Whether test passed specifications</description>
      </field>
      <field>
        <field_name>test_method</field_name>
        <data_type>string</data_type>
        <description>
          Standard test method (e.g., "USP 711", "Ph. Eur. 2.9.3")
        </description>
      </field>
    </nested_schema>
  </field>

  <field>
    <field_name>technician_id</field_name>
    <data_type>string</data_type>
    <required>true</required>
    <description>
      ID of technician who performed tests (links to F0101.AN8)
    </description>
    <jde_reference>F0101.AN8</jde_reference>
  </field>

  <field>
    <field_name>certificate_of_analysis</field_name>
    <data_type>object</data_type>
    <description>COA document metadata</description>
    <nested_schema>
      <field>
        <field_name>document_id</field_name>
        <data_type>string</data_type>
        <description>COA document identifier</description>
      </field>
      <field>
        <field_name>file_path</field_name>
        <data_type>string</data_type>
        <description>File system path to COA document</description>
      </field>
      <field>
        <field_name>digital_signature</field_name>
        <data_type>string</data_type>
        <description>
          Digital signature for FDA 21 CFR Part 11 compliance
        </description>
      </field>
      <field>
        <field_name>approval_date</field_name>
        <data_type>datetime</data_type>
        <format>ISO8601</format>
        <description>Date COA was approved by QA</description>
      </field>
    </nested_schema>
  </field>
</schema_definition>
```

**What NOT to Include:**
- Actual test results or sample data
- Employee names (use IDs only)
- Actual file paths or document locations
- Signature images or biometric data

#### 5.4 Relationships to JDE Tables
**What to Include:**
- Reference type relationships
- Related JDE table (F-number)
- Local field to JDE field mapping
- Relationship description

**Example:**
```xml
<relationships>
  <relationship>
    <relationship_type>REFERENCE</relationship_type>
    <related_table>work_orders</related_table>
    <related_jde_table>F4801</related_jde_table>
    <local_field>batch_number</local_field>
    <foreign_field>batch_number</foreign_field>
    <jde_field_reference>F4801.LOTN</jde_field_reference>
    <relationship_name>quality_to_batch</relationship_name>
  </relationship>
</relationships>
```

**What NOT to Include:**
- Query syntax for joins
- Application integration points
- Middleware configurations

---

## 6. AI Use Case Mappings

### Purpose
Define how JD Edwards data supports specific AI/ML use cases, including required tables, columns, and transformations.

### Sections

#### 6.1 Use Case Identification
**What to Include:**
- Unique use case identifier
- Descriptive use case name
- Business problem statement
- AI technique classification
- Expected business outcomes

**Example:**
```xml
<use_case>
  <use_case_id>demand_forecasting</use_case_id>
  <use_case_name>Product Demand Forecasting</use_case_name>
  <description>
    Predict future product demand using historical sales data
    from JDE to optimize inventory levels and production planning
  </description>
  <ai_technique>TIME_SERIES_ANALYSIS</ai_technique>
  <business_impact>
    Reduce stockouts by 30%, decrease excess inventory by 20%
  </business_impact>
</use_case>
```

**What NOT to Include:**
- Model architecture details (neural networks, layers)
- Specific algorithms or libraries
- Implementation timelines
- Cost estimates

#### 6.2 Common AI Use Cases for JD Edwards

| Use Case ID | Use Case Name | AI Technique | JDE Modules |
|-------------|---------------|--------------|-------------|
| `demand_forecasting` | Demand Forecasting | Time Series | Sales (42), Inventory (41) |
| `quality_prediction` | Quality Outcome Prediction | ML Classification | Manufacturing (48), QC |
| `customer_churn` | Customer Churn Prediction | ML Classification | Sales (42), AR (03) |
| `inventory_optimization` | Inventory Optimization | Optimization | Inventory (41), Sales (42) |
| `predictive_maintenance` | Equipment Maintenance | Time Series, Anomaly | Manufacturing (48) |
| `price_optimization` | Dynamic Pricing | Regression | Sales (42) |
| `supplier_risk` | Supplier Risk Assessment | ML Classification | Procurement (43) |
| `production_scheduling` | Smart Scheduling | Optimization | Manufacturing (31/48) |

#### 6.3 Required Data Sources
**What to Include:**
- JDE table identifiers with F-numbers
- Specific columns needed from each table
- JDE data dictionary items (optional)
- Rationale for data selection

**Example:**
```xml
<required_data_sources>
  <data_source>
    <table_id>sales_orders_header</table_id>
    <jde_table>F4201</jde_table>
    <columns>
      <column>order_date</column>
      <column>total_amount</column>
      <column>customer_id</column>
      <column>order_status</column>
    </columns>
    <jde_fields>
      <field>TRDJ (Order Date)</field>
      <field>AEXP (Extended Amount)</field>
      <field>AN8 (Customer Number)</field>
      <field>NXTR (Next Status)</field>
    </jde_fields>
  </data_source>

  <data_source>
    <table_id>customer_master</table_id>
    <jde_table>F0301</jde_table>
    <columns>
      <column>customer_name</column>
      <column>customer_id</column>
      <column>credit_limit</column>
    </columns>
  </data_source>

  <data_source>
    <table_id>sales_orders_detail</table_id>
    <jde_table>F4211</jde_table>
    <columns>
      <column>item_number</column>
      <column>quantity_ordered</column>
      <column>unit_price</column>
    </columns>
  </data_source>
</required_data_sources>
```

**What NOT to Include:**
- SQL queries or extraction code
- Sample datasets
- Training/test split specifications
- Model hyperparameters

#### 6.4 Data Transformations
**What to Include:**
- Transformation type (AGGREGATION, TIME_SERIES, FEATURE_ENGINEERING)
- Business logic description
- JDE-specific considerations (date conversions, UDC lookups)

**Example:**
```xml
<data_transformations>
  <transformation>
    <type>DATE_CONVERSION</type>
    <description>
      Convert JDE Julian dates (CYYDDD) to ISO 8601 format
      for time series analysis
    </description>
  </transformation>

  <transformation>
    <type>AGGREGATION</type>
    <description>
      Group sales by month, product (F4211.LITM), and customer
      to create monthly demand patterns
    </description>
  </transformation>

  <transformation>
    <type>UDC_LOOKUP</type>
    <description>
      Translate JDE UDC codes (e.g., 42/SS for order status)
      to human-readable descriptions
    </description>
  </transformation>

  <transformation>
    <type>TIME_SERIES</type>
    <description>
      Create rolling window features (7-day, 30-day, 90-day)
      for demand patterns and seasonality detection
    </description>
  </transformation>

  <transformation>
    <type>FEATURE_ENGINEERING</type>
    <description>
      Calculate lead time variance, order fulfillment rate,
      and on-time delivery percentage from F4211/F4311
    </description>
  </transformation>
</data_transformations>
```

**What NOT to Include:**
- Python/SQL transformation code
- Tool-specific syntax (Spark, Pandas)
- Performance optimization details
- Infrastructure specifications

---

## 7. Data Quality Rules

### Purpose
Define validation rules specific to JD Edwards data to ensure integrity, compliance, and fitness for AI use cases.

### Sections

#### 7.1 Rule Definition
**What to Include:**
- Unique rule identifier
- Rule name
- Business rationale
- Rule type (COMPLETENESS, ACCURACY, CONSISTENCY, RANGE_CHECK)
- Scope (specific JDE table.column)
- Validation logic (pseudo-code)
- Compliance linkage (FDA, GMP, etc.)

**Example:**
```xml
<rule>
  <rule_id>batch_traceability</rule_id>
  <rule_name>Batch Traceability Completeness</rule_name>
  <description>
    Every manufactured batch must have complete traceability
    to comply with FDA 21 CFR Part 11 and GMP requirements
  </description>
  <rule_type>COMPLETENESS</rule_type>
  <applies_to>work_orders.batch_number</applies_to>
  <jde_reference>F4801.LOTN</jde_reference>
  <validation_logic>NOT NULL AND LENGTH >= 10</validation_logic>
  <compliance_framework>FDA_21_CFR_PART_11, GMP</compliance_framework>
</rule>
```

**What NOT to Include:**
- Implementation code (SQL, PL/SQL)
- Error message text
- Remediation procedures
- Specific validation programs (e.g., R55814)

#### 7.2 JDE-Specific Data Quality Rules

**Common Rules for JD Edwards:**

```xml
<data_quality_rules>
  <!-- Date Range Validation -->
  <rule>
    <rule_id>order_date_validity</rule_id>
    <rule_name>Order Date Range Validation</rule_name>
    <description>
      Order dates must be within reasonable business range
      and properly converted from JDE Julian format
    </description>
    <rule_type>RANGE_CHECK</rule_type>
    <applies_to>sales_orders_header.order_date</applies_to>
    <jde_reference>F4201.TRDJ</jde_reference>
    <validation_logic>
      order_date >= CURRENT_DATE - 5 YEARS AND
      order_date <= CURRENT_DATE
    </validation_logic>
  </rule>

  <!-- Master Data Integrity -->
  <rule>
    <rule_id>customer_reference_integrity</rule_id>
    <rule_name>Customer Reference Integrity</rule_name>
    <description>
      All customer IDs in orders must exist in customer master
    </description>
    <rule_type>REFERENTIAL_INTEGRITY</rule_type>
    <applies_to>sales_orders_header.customer_id</applies_to>
    <jde_reference>F4201.AN8 → F0301.AN8</jde_reference>
    <validation_logic>
      customer_id IN (SELECT customer_id FROM customer_master)
    </validation_logic>
  </rule>

  <!-- UDC Validation -->
  <rule>
    <rule_id>status_code_validation</rule_id>
    <rule_name>Order Status Code Validation</rule_name>
    <description>
      Order status must be valid JDE UDC value from 42/SS
    </description>
    <rule_type>REFERENTIAL_INTEGRITY</rule_type>
    <applies_to>sales_orders_header.order_status</applies_to>
    <jde_reference>F4201.NXTR (UDC 42/SS)</jde_reference>
    <validation_logic>
      order_status IN ('10', '20', '30', '40', '99')
    </validation_logic>
  </rule>

  <!-- Quantity Validation -->
  <rule>
    <rule_id>quantity_consistency</rule_id>
    <rule_name>Manufacturing Quantity Consistency</rule_name>
    <description>
      Actual quantity should not exceed planned quantity by more than 10%
    </description>
    <rule_type>CONSISTENCY</rule_type>
    <applies_to>work_orders.actual_quantity</applies_to>
    <jde_reference>F4801.UORG (Actual) vs F4801.UORG (Planned)</jde_reference>
    <validation_logic>
      actual_quantity <= planned_quantity * 1.10
    </validation_logic>
  </rule>

  <!-- Pharmaceutical Compliance -->
  <rule>
    <rule_id>lot_expiry_validation</rule_id>
    <rule_name>Lot Expiration Date Validation</rule_name>
    <description>
      Pharmaceutical lots must have valid expiration dates
      (manufactured date + shelf life)
    </description>
    <rule_type>RANGE_CHECK</rule_type>
    <applies_to>lot_master.expiry_date</applies_to>
    <jde_reference>F3111.EXP</jde_reference>
    <validation_logic>
      expiry_date >= manufacture_date AND
      expiry_date <= manufacture_date + max_shelf_life
    </validation_logic>
    <compliance_framework>GMP, FDA</compliance_framework>
  </rule>

  <!-- Monetary Validation -->
  <rule>
    <rule_id>order_amount_validation</rule_id>
    <rule_name>Order Amount Validation</rule_name>
    <description>
      Order amounts must be positive and within credit limit
    </description>
    <rule_type>RANGE_CHECK</rule_type>
    <applies_to>sales_orders_header.total_amount</applies_to>
    <jde_reference>F4201.AEXP</jde_reference>
    <validation_logic>
      total_amount > 0 AND
      total_amount <= customer.credit_limit
    </validation_logic>
  </rule>
</data_quality_rules>
```

**What NOT to Include:**
- Specific threshold values (use business constants)
- Exception handling logic
- Workflow approval processes
- Alert recipients or notification rules

---

## 8. Integration Specifications

### Purpose
Define how to integrate with JD Edwards through APIs, ETL pipelines, and data extraction methods.

### Sections

#### 8.1 API Endpoint Specifications
**What to Include:**
- Endpoint identifier
- Endpoint name
- URL pattern (generic)
- HTTP method
- Authentication method
- Rate limiting
- Response format
- Caching strategy

**Example:**
```xml
<api_endpoint>
  <endpoint_id>sales_data_api</endpoint_id>
  <endpoint_name>Sales Data API</endpoint_name>
  <endpoint_url>/api/v1/sales/orders</endpoint_url>
  <method>GET</method>
  <authentication>OAuth2</authentication>
  <jde_integration_method>ORCHESTRATOR_REST</jde_integration_method>
  <rate_limit>1000_per_hour</rate_limit>
  <response_format>JSON</response_format>
  <caching_strategy>5_minutes</caching_strategy>
</api_endpoint>
```

**What NOT to Include:**
- Actual endpoint URLs or server names
- API keys or credentials
- Internal service names
- Orchestrator or Form Service URLs

#### 8.2 JDE Integration Methods

**Common Integration Approaches:**

| Method | Description | Use Case |
|--------|-------------|----------|
| `ORCHESTRATOR_REST` | JDE Orchestrator REST API | Real-time data access |
| `FORM_SERVICE` | JDE Form Service | Interactive form operations |
| `BSSV` | Business Service (Web Service) | Transactional operations |
| `TABLE_CONVERSION` | Table Conversion (Z-tables) | Batch data import |
| `UBE_EXPORT` | Report export to flat file | Batch data extraction |
| `JDBC_DIRECT` | Direct database access | Read-only analytics |
| `JDE_CONNECT` | Event-driven integration | Real-time triggers |

**Example:**
```xml
<integration_methods>
  <method>
    <method_id>orchestrator_sales</method_id>
    <method_name>Sales Order Orchestration</method_name>
    <integration_type>ORCHESTRATOR_REST</integration_type>
    <jde_module>Sales Order Management (P4210)</jde_module>
    <description>
      REST API for creating and querying sales orders
      via JDE Orchestrator
    </description>
    <authentication>OAuth2_Bearer_Token</authentication>
  </method>

  <method>
    <method_id>batch_extract_manufacturing</method_id>
    <method_name>Manufacturing Data Batch Extract</method_name>
    <integration_type>UBE_EXPORT</integration_type>
    <jde_module>Work Order Master (F4801)</jde_module>
    <description>
      Scheduled batch export of work order data to CSV
      for AI data lake ingestion
    </description>
    <frequency>HOURLY</frequency>
  </method>
</integration_methods>
```

#### 8.3 Data Pipeline Specifications
**What to Include:**
- Pipeline identifier and name
- Source system (JDE specific)
- Target system (generic)
- Execution frequency
- Transformation engine
- Data quality checks
- JDE-specific considerations

**Example:**
```xml
<data_pipeline>
  <pipeline_id>manufacturing_etl</pipeline_id>
  <pipeline_name>Manufacturing Data ETL Pipeline</pipeline_name>
  <source_system>JD_EDWARDS_E1</source_system>
  <target_system>AI_DATA_LAKE</target_system>
  <frequency>HOURLY</frequency>
  <transformation_engine>DATA_INTEGRATION_PLATFORM</transformation_engine>

  <extraction_method>
    <method>JDBC_DIRECT_READ</method>
    <tables>
      <table>F4801 (Work Orders)</table>
      <table>F4101 (Item Master)</table>
      <table>F3111 (Lot Master)</table>
    </tables>
  </extraction_method>

  <transformations>
    <transformation>Convert JDE Julian dates to ISO 8601</transformation>
    <transformation>Lookup UDC descriptions</transformation>
    <transformation>Join work orders with item master</transformation>
  </transformations>

  <data_quality_checks>
    <check>SCHEMA_VALIDATION</check>
    <check>BATCH_TRACEABILITY_COMPLETENESS</check>
    <check>REFERENTIAL_INTEGRITY</check>
    <check>DATE_RANGE_VALIDATION</check>
  </data_quality_checks>
</data_pipeline>
```

**What NOT to Include:**
- Database connection strings
- Server names or IP addresses
- Credentials or secrets
- Specific job names or scheduler IDs

---

## 9. JDE-Specific Conventions

### Purpose
Document JD Edwards-specific naming conventions, data types, and best practices for data structure definitions.

### Sections

#### 9.1 JDE Naming Conventions

**Table Naming:**
- JDE tables: Always prefix with "F" (e.g., F4201, F0101, F4801)
- Custom tables: Prefix with "F55" or "F56" (e.g., F55CUST)
- Include F-number in table name: `Sales Orders (F4201)`

**Column Naming:**
- Use business-friendly logical names: `customer_id`, not `AN8`
- Reference JDE data dictionary items in metadata: `<jde_data_item>AN8</jde_data_item>`
- For documentation, include both: "Customer ID (AN8)"

**Module Codes:**
- Always reference JDE system code: `<jde_system_code>42</jde_system_code>`
- Common codes: 01 (Address Book), 03 (AR), 04 (AP), 09 (GL), 31 (Inventory), 42 (Sales), 43 (Purchasing), 48 (Shop Floor)

#### 9.2 JDE Data Dictionary Items (Common)

| Data Item | Description | Type | Length |
|-----------|-------------|------|--------|
| AN8 | Address Book Number | Numeric | 8 |
| DOCO | Document Number (Order, WO) | Numeric | 8 |
| DCTO | Document Type | String | 2 |
| LITM | Item Number (Long) | String | 25 |
| ITM | Item Number (Short) | Numeric | 6 |
| LOTN | Lot/Serial Number | String | 30 |
| TRDJ | Transaction Date | Date | Julian |
| UORG | Original Quantity | Numeric | 15,4 |
| AEXP | Extended Amount | Numeric | 15,2 |
| NXTR | Next Status | String | 2 |
| MCU | Business Unit | String | 12 |

#### 9.3 JDE Date Handling

**JDE Julian Date Format (CYYDDD):**
- C = Century (0=19xx, 1=20xx, 2=21xx)
- YY = Year (00-99)
- DDD = Day of year (001-366)

**Example Conversions:**
- `125016` = January 16, 2025 (1=2000s, 25=2025, 016=16th day)
- `124365` = December 31, 2024

**Best Practice for AI Use Cases:**
```xml
<column>
  <column_id>order_date</column_id>
  <column_name>Order Date</column_name>
  <jde_data_item>TRDJ</jde_data_item>
  <jde_storage_format>JULIAN_CYYDDD</jde_storage_format>
  <data_type>DATE</data_type>
  <format_pattern>YYYY-MM-DD</format_pattern>
  <business_description>
    Order date (stored as JDE Julian, converted to ISO 8601)
  </business_description>
  <transformation>Convert CYYDDD to YYYY-MM-DD</transformation>
</column>
```

#### 9.4 JDE User Defined Codes (UDCs)

**UDC Format:** `System Code / User Code`

**Common UDC Categories:**
- `00/DT` - Document Types
- `00/SY` - System Codes
- `40/AT` - Category Codes
- `42/SS` - Order Status
- `43/LT` - Line Types
- `H00/ST` - Status Codes

**Example:**
```xml
<column>
  <column_id>order_status</column_id>
  <column_name>Order Status</column_name>
  <jde_data_item>NXTR</jde_data_item>
  <jde_udc>42/SS</jde_udc>
  <data_type>VARCHAR</data_type>
  <max_length>2</max_length>
  <allowed_values>
    <value code="10" udc="42/SS">Open</value>
    <value code="20" udc="42/SS">In Progress</value>
    <value code="30" udc="42/SS">Shipped</value>
    <value code="99" udc="42/SS">Completed</value>
  </allowed_values>
  <transformation>
    Lookup UDC description from F0005 where SY=42 and RT=SS
  </transformation>
</column>
```

#### 9.5 Pharmaceutical Manufacturing Extensions

**Additional Fields for Pharma:**

```xml
<pharmaceutical_extensions>
  <field>
    <field_name>manufacturing_campaign</field_name>
    <description>
      Campaign identifier grouping multiple batches
      for pharmaceutical production campaigns
    </description>
    <format_pattern>CAMP_[0-9]{6}</format_pattern>
  </field>

  <field>
    <field_name>batch_number</field_name>
    <description>
      FDA-compliant batch identifier for traceability
    </description>
    <jde_reference>F3111.LOTN</jde_reference>
    <format_pattern>BATCH[0-9]{10}</format_pattern>
    <compliance>FDA_21_CFR_PART_11, GMP</compliance>
  </field>

  <field>
    <field_name>quality_status</field_name>
    <description>GMP quality status (Pending, Released, Rejected)</description>
    <allowed_values>
      <value code="PENDING">Pending QC Test</value>
      <value code="PASSED">Quality Passed</value>
      <value code="FAILED">Quality Failed</value>
      <value code="RELEASED">Released for Sale</value>
      <value code="QUARANTINE">On Quarantine Hold</value>
      <value code="REJECTED">Rejected - Do Not Use</value>
    </allowed_values>
  </field>

  <field>
    <field_name>expiry_date</field_name>
    <description>
      Product expiration date (manufacture + shelf life)
    </description>
    <jde_reference>F3111.EXP</jde_reference>
    <format_pattern>YYYY-MM-DD</format_pattern>
    <calculation>manufacture_date + shelf_life_days</calculation>
  </field>
</pharmaceutical_extensions>
```

---

## Best Practices Summary

### DO:
1. **Use JDE F-numbers** - Always reference JDE table numbers (F4201, F0301, etc.)
2. **Include data dictionary items** - Reference JDE data items (AN8, DOCO, LITM)
3. **Document UDC codes** - Specify UDC categories for status codes
4. **Convert dates** - Transform JDE Julian dates to ISO 8601 for AI use
5. **Map relationships** - Show how tables relate via JDE foreign keys
6. **Reference system codes** - Include JDE module codes (42, 48, etc.)
7. **Consider pharma compliance** - Add FDA/GMP requirements where applicable
8. **Use business names** - Logical names like `customer_id`, not `AN8`
9. **Define both structured and unstructured** - QC data often lives outside JDE
10. **Plan for integration** - Specify Orchestrator, BSSV, or batch methods

### DON'T:
1. **Don't use JDE internal names** - Avoid SDDOCO, SDNXTR in business definitions
2. **Don't include credentials** - No passwords, connection strings
3. **Don't specify environments** - Keep production, test, dev generic
4. **Don't add physical details** - No server names, schemas (PRODDTA, TESTDTA)
5. **Don't include customizations** - Focus on standard JDE unless critical
6. **Don't specify versions** - Avoid JDE version numbers (9.2, Tools 9.2.x)
7. **Don't add sample data** - No actual customer data or PII
8. **Don't include UI details** - No form names (P4210) unless for context
9. **Don't mix concerns** - Keep data structure separate from workflow
10. **Don't forget relationships** - Always map table relationships

---

## Appendix A: JDE Table Quick Reference

### Master Data Tables
| F-Number | Table Name | Description |
|----------|------------|-------------|
| F0101 | Address Book Master | Customers, suppliers, employees |
| F0301 | Customer Master | Customer-specific data |
| F0411 | Supplier Master | Supplier-specific data |
| F4101 | Item Master | Product definitions |
| F0006 | Business Unit Master | Locations, warehouses |

### Transactional Tables
| F-Number | Table Name | Description |
|----------|------------|-------------|
| F4201 | Sales Order Header | Sales order master |
| F4211 | Sales Order Detail | Sales order line items |
| F4301 | Purchase Order Header | Purchase order master |
| F4311 | Purchase Order Detail | PO line items |
| F4801 | Work Order Master | Manufacturing orders |
| F0911 | Account Ledger | Financial transactions |
| F3111 | Lot Master | Batch/lot traceability |

### Reference Tables
| F-Number | Table Name | Description |
|----------|------------|-------------|
| F0005 | User Defined Codes | UDC definitions |
| F9861 | Data Dictionary | JDE data items |

---

## Appendix B: Sample Complete Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<data_structure_template>
  <metadata>
    <template_version>1.0</template_version>
    <created_date>2025-01-16</created_date>
    <description>
      JDE data structure for pharmaceutical manufacturing AI use cases
    </description>
    <based_on>JD Edwards EnterpriseOne</based_on>
  </metadata>

  <data_source>
    <source_id>jde_pharma_erp</source_id>
    <source_name>JD Edwards EnterpriseOne</source_name>
    <source_type>ERP_DATABASE</source_type>
    <connection_type>DATABASE</connection_type>
    <is_real_time>false</is_real_time>
    <update_frequency>BATCH_HOURLY</update_frequency>
    <data_retention_years>7</data_retention_years>
    <compliance_requirements>
      <requirement>FDA_21_CFR_PART_11</requirement>
      <requirement>GMP_COMPLIANCE</requirement>
      <requirement>GDPR</requirement>
    </compliance_requirements>
  </data_source>

  <business_modules>
    <module>
      <module_id>manufacturing_mgmt</module_id>
      <module_name>Manufacturing Management</module_name>
      <jde_system_code>48</jde_system_code>
      <module_description>
        Production orders, batch records, and quality control
      </module_description>

      <data_tables>
        <table>
          <table_id>work_orders</table_id>
          <table_name>Work Orders (F4801)</table_name>
          <jde_table_code>F4801</jde_table_code>
          <table_type>STRUCTURED</table_type>
          <is_master_data>false</is_master_data>
          <is_transactional>true</is_transactional>
          <primary_key>work_order_number</primary_key>

          <columns>
            <column>
              <column_id>work_order_number</column_id>
              <column_name>Work Order Number</column_name>
              <jde_data_item>DOCO</jde_data_item>
              <data_type>VARCHAR</data_type>
              <max_length>20</max_length>
              <is_nullable>false</is_nullable>
              <is_unique>true</is_unique>
              <format_pattern>WO[0-9]{8}</format_pattern>
              <business_description>
                Unique manufacturing order identifier
              </business_description>
            </column>

            <column>
              <column_id>batch_number</column_id>
              <column_name>Batch Number</column_name>
              <jde_data_item>LOTN</jde_data_item>
              <data_type>VARCHAR</data_type>
              <max_length>20</max_length>
              <is_nullable>false</is_nullable>
              <format_pattern>BATCH[0-9]{10}</format_pattern>
              <business_description>
                Pharmaceutical batch identifier for FDA traceability
              </business_description>
              <compliance>FDA_21_CFR_PART_11, GMP</compliance>
            </column>

            <column>
              <column_id>quality_status</column_id>
              <column_name>Quality Status</column_name>
              <jde_data_item>NXTR</jde_data_item>
              <jde_udc>48/QS</jde_udc>
              <data_type>VARCHAR</data_type>
              <max_length>10</max_length>
              <allowed_values>
                <value code="PENDING" udc="48/QS">Pending Test</value>
                <value code="PASSED" udc="48/QS">Quality Passed</value>
                <value code="RELEASED" udc="48/QS">Released for Sale</value>
              </allowed_values>
              <business_description>
                Quality control status of batch
              </business_description>
            </column>
          </columns>
        </table>
      </data_tables>
    </module>
  </business_modules>

  <ai_use_cases>
    <use_case>
      <use_case_id>quality_prediction</use_case_id>
      <use_case_name>Manufacturing Quality Prediction</use_case_name>
      <description>
        Predict quality outcomes based on manufacturing parameters
        from JDE work orders and QC test results
      </description>
      <ai_technique>MACHINE_LEARNING</ai_technique>

      <required_data_sources>
        <data_source>
          <table_id>work_orders</table_id>
          <jde_table>F4801</jde_table>
          <columns>
            <column>batch_number</column>
            <column>planned_quantity</column>
            <column>actual_quantity</column>
          </columns>
        </data_source>
      </required_data_sources>
    </use_case>
  </ai_use_cases>
</data_structure_template>
```

---

---

**Document Information:**
- **Version:** 1.0
- **Last Updated:** 2025-11-04
- **Published by:** AICOE (aicoe.io)
- **Template Source:** JD Edwards Data Structure Template v1.0
- **Target System:** JD Edwards EnterpriseOne (All versions)
- **Copyright:** © 2025 AICOE. All rights reserved.
- **Website:** https://aicoe.io
