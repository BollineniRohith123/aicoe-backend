# Guide to Writing Functional Requirements

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

Functional Requirements (FR) define **how** the system will fulfill the business requirements. They specify the specific behaviors, features, and functions the system must provide to meet business needs.

### Document Hierarchy
```
Business Requirements (BR)
    ↓ maps to
Functional Requirements (FR)  ← YOU ARE HERE
    ↓ maps to
Test Cases (TC)
```

### Naming Convention
- **Format**: FR1, FR2, FR3, FR4, ...
- **Rule**: Each Functional Requirement must have a unique identifier
- **Best Practice**: Never reuse IDs, even for deleted requirements
- **Traceability**: Each FR must map to at least one BR

---

## Purpose and Definition

### What is a Functional Requirement?

A Functional Requirement describes a specific function or behavior the system must exhibit. It defines:
- **How** the system will work
- **What** the system will do
- **Who** will interact with it
- **When** and **where** actions occur
- **What** inputs are needed and outputs produced

### What Functional Requirements Are NOT

Functional Requirements should NOT include:
- Design specifications (UI/UX mockups belong in design docs)
- Implementation details (specific code, database schemas)
- Technology choices (programming languages, frameworks)
- Non-functional requirements (performance, security, scalability)

### Key Characteristics

Good Functional Requirements are:
1. **Specific** - Clearly defined with no ambiguity
2. **Testable** - Can be objectively verified
3. **Traceable** - Linked to Business Requirements
4. **Complete** - Covers all scenarios (normal, alternative, exceptional)
5. **Consistent** - No conflicts with other requirements
6. **Feasible** - Technically achievable

---

## Structure

Each Functional Requirement should include the following components:

```markdown
**FR[#]: [Clear, Descriptive Requirement Title]**

- **Description**: Detailed description of the function or feature
- **Maps to BR**: BR[#], BR[#]
- **Actors**: Who interacts with this function (user roles, systems)
- **Preconditions**: What must be true before this function executes
- **Input**: What data/actions are required
- **Process**: What the system does (step-by-step)
- **Output**: What result is produced
- **Priority**: High / Medium / Low
- **Dependencies**: Other FRs or systems this depends on
```

### Component Descriptions

**Title**
- Clear, concise description of the function (5-10 words)
- Action-oriented, specific to the feature
- Examples: "User Profile Update", "Payment Processing", "Order Confirmation Email"

**Description**
- Detailed explanation of what the system does
- Use standard format: "The system shall..."
- 2-4 sentences providing context

**Maps to BR**
- List all Business Requirements this FR supports
- Required for traceability
- Example: BR1, BR3

**Actors**
- All user roles or external systems that interact with this function
- Be specific: "Registered Customer", "Admin User", "Payment Gateway API"
- Not vague: "User", "System"

**Preconditions**
- State that must be true before execution
- System state, user state, data conditions
- Examples: "User is logged in", "Shopping cart contains at least one item"

**Input**
- All data required for the function
- Include data types, formats, validation rules
- Specify required vs. optional fields
- Examples: "Email Address (required, valid email format, max 255 characters)"

**Process**
- Step-by-step description of system behavior
- Use numbered steps for clarity
- Include decision points, validations, calculations
- Cover normal flow first, then alternatives and exceptions

**Output**
- All results produced by the function
- UI responses, data changes, notifications, logs
- Include success and error outputs
- Be specific about what user sees/receives

**Priority**
- **High**: Critical functionality, must have for release
- **Medium**: Important but not blocking
- **Low**: Nice-to-have, can be deferred

**Dependencies**
- Other FRs required for this to work
- External systems or APIs
- Specific versions or configurations
- Example: "FR15 (Authentication System), Payment Gateway API v2.0"

---

## Writing Guidelines

### 1. Be Specific and Detailed

Functional Requirements describe exact system behavior.

**Good Example:**
```markdown
**FR1: User Profile Update**

- **Description**: The system shall allow authenticated users to update their
  profile information including name, email, and phone number with real-time
  validation and confirmation
- **Actors**: Registered Customer
- **Input**:
  - First Name (required, alphabetic characters only, 2-50 characters)
  - Last Name (required, alphabetic characters only, 2-50 characters)
  - Email Address (required, valid email format per RFC 5322, max 255 characters)
  - Phone Number (optional, E.164 format, 10-15 digits)
```

**Bad Example:**
```markdown
**FR1: User Updates Profile**

- **Description**: Users can change their information
- **Input**: Personal data
```
*Why it's bad: Too vague, lacks detail on validation, formats, and constraints*

### 2. Use Clear, Action-Oriented Language

Use standard format: "The system shall..."

**Good Examples:**
- "The system shall display an error message if..."
- "The system shall validate the email format before..."
- "The system shall send a confirmation email to..."
- "The system shall update the database record when..."

**Bad Examples:**
- "There should be validation" (passive, vague)
- "Emails need to be checked" (unclear who does what)
- "The user validates input" (incorrect actor)

### 3. Include All Scenarios

Cover normal flow, alternative flows, and exceptions.

**Good Example:**
```markdown
**Process**:
1. System validates all input fields
2. If validation fails:
   a. Display inline error messages next to invalid fields
   b. Keep valid field values populated
   c. Set focus to first invalid field
3. If email address changed:
   a. Check if new email already exists in database
   b. If exists, display error: "Email address already in use"
   c. If unique, proceed
4. If validation succeeds:
   a. Update user record in database
   b. If email changed, send verification email to new address
   c. Update session with new user data
   d. Display success message: "Profile updated successfully"
```

**Bad Example:**
```markdown
**Process**:
1. Validate input
2. Update database
3. Show success message
```
*Why it's bad: Doesn't cover error cases, validation failures, or conditional logic*

### 4. Avoid Design Constraints

Focus on functionality, not implementation or design.

**Good Example:**
```markdown
**Output**:
  - Success: Display confirmation message to user
  - Error: Display specific error message describing validation failure
```

**Bad Example:**
```markdown
**Output**:
  - Success: Show green toast notification in top-right corner using Material-UI
  - Error: Display red modal dialog with Helvetica 14pt font
```
*Why it's bad: Specifies UI design details (colors, position, libraries, fonts)*

### 5. Make It Testable

Each FR should be objectively verifiable.

**Good Example:**
```markdown
**FR5: Password Strength Validation**

- **Process**:
  1. System checks password meets all criteria:
     - Minimum 8 characters
     - At least 1 uppercase letter (A-Z)
     - At least 1 lowercase letter (a-z)
     - At least 1 number (0-9)
     - At least 1 special character (!@#$%^&*)
  2. If any criterion not met, display specific error message
  3. System rejects passwords found in common password list (top 10,000)
```
*Testable: Can verify each criterion with specific test inputs*

**Bad Example:**
```markdown
**FR5: Strong Password Required**

- **Process**: System ensures password is secure enough
```
*Not testable: "Secure enough" is subjective and unmeasurable*

### 6. Use Consistent Terminology

Maintain a project glossary and use terms consistently.

**Good Practice:**
```markdown
- Use "Registered Customer" throughout (not "User", "Customer", "Member" interchangeably)
- Use "Shopping Cart" consistently (not "Basket", "Cart", "Order")
- Use "Order Confirmation" (not "Purchase Confirmation", "Order Receipt")
```

---

## Quality Checklist

Before finalizing a Functional Requirement, verify:

- [ ] **Does it describe a specific system function or behavior?**
  - Not a business goal or technical implementation

- [ ] **Is it clearly mapped to at least one Business Requirement?**
  - Traceability to BR# established

- [ ] **Can it be tested objectively?**
  - Specific, measurable criteria for validation

- [ ] **Is it unambiguous and complete?**
  - No room for multiple interpretations
  - All scenarios covered (normal, alternative, error)

- [ ] **Does it avoid specifying design/implementation details?**
  - No UI mockups, specific technologies, or code

- [ ] **Are all actors clearly defined?**
  - Specific user roles or systems identified

- [ ] **Are inputs and outputs fully specified?**
  - Data types, formats, validation rules, constraints

- [ ] **Are preconditions clearly stated?**
  - What must be true before execution

- [ ] **Are all dependencies identified?**
  - Other FRs, external systems, APIs

- [ ] **Is the process flow complete?**
  - Step-by-step logic including validations and error handling

- [ ] **Is it consistent with other requirements?**
  - No conflicts or contradictions

- [ ] **Is it feasible to implement?**
  - Technically achievable with reasonable effort

---

## Examples

### Example 1: User Authentication

```markdown
**FR1: User Login with Username and Password**

- **Description**: The system shall authenticate users using username and password
  credentials with validation, session creation, and failed attempt tracking
- **Maps to BR**: BR1 (Secure User Authentication)
- **Actors**: Registered User, System Administrator
- **Preconditions**:
  - User has a registered account
  - Account status is active (not locked, suspended, or deleted)
  - User is not currently logged in
- **Input**:
  - Username (required, 6-50 alphanumeric characters, case-insensitive)
  - Password (required, 8-128 characters, case-sensitive)
  - "Remember Me" checkbox (optional, boolean)
- **Process**:
  1. System validates input format:
     a. Username is not empty and meets length requirements
     b. Password is not empty
  2. System queries database for username (case-insensitive match)
  3. If username not found:
     a. Log failed attempt with timestamp and IP address
     b. Display generic error: "Invalid username or password"
     c. Exit process
  4. System verifies password using bcrypt hash comparison
  5. If password incorrect:
     a. Increment failed attempt counter for account
     b. If failed attempts ≥ 5 within 15 minutes:
        - Set account status to "locked"
        - Set lockout expiration to current time + 30 minutes
        - Send email notification to account owner
        - Display error: "Account temporarily locked. Please try again in 30 minutes"
     c. Else display generic error: "Invalid username or password"
     d. Log failed attempt with timestamp and IP address
     e. Exit process
  6. System checks account status:
     a. If locked and lockout expired, unlock account and continue
     b. If locked and lockout not expired, display error and exit
     c. If suspended or deleted, display "Account not available" and exit
  7. System creates session:
     a. Generate unique session token (UUID v4)
     b. Store session in database with user ID, token, creation time, IP address
     c. If "Remember Me" checked, set expiration to 30 days; else 24 hours
     d. Set session cookie with token
  8. System resets failed attempt counter to 0
  9. System logs successful login event
  10. System redirects user to dashboard or original requested page
- **Output**:
  - Success:
    - User redirected to appropriate page
    - Session established
    - Welcome message displayed
    - Navigation shows user as logged in
  - Failure:
    - Error message displayed (generic for security)
    - User remains on login page
    - Input fields cleared (password only)
    - Failed attempt logged
    - Email sent if account locked
- **Priority**: High
- **Dependencies**:
  - FR12 (Session Management)
  - FR18 (Account Management)
  - FR23 (Email Notification Service)
  - Database: Users table, Sessions table, LoginAttempts table
```

### Example 2: E-Commerce Shopping Cart

```markdown
**FR2: Add Product to Shopping Cart**

- **Description**: The system shall allow users to add products to their shopping
  cart with quantity selection, variant options, and inventory validation
- **Maps to BR**: BR5 (Enable Online Shopping), BR6 (Manage Inventory)
- **Actors**: Anonymous User, Registered Customer
- **Preconditions**:
  - Product exists and is published
  - Product is not archived or deleted
  - At least one product variant is available (if product has variants)
- **Input**:
  - Product ID (required, positive integer)
  - Quantity (required, positive integer, default: 1, max: 99)
  - Variant Options (conditional based on product):
    - Size (if applicable, string from predefined list)
    - Color (if applicable, string from predefined list)
    - Custom Options (if applicable, key-value pairs)
- **Process**:
  1. System validates Product ID:
     a. Query database for product
     b. If not found, display error: "Product not available" and exit
  2. System checks product status:
     a. If not published, display error: "Product not available" and exit
     b. If archived/deleted, display error: "Product no longer available" and exit
  3. If product has variants:
     a. Validate all required variant options are provided
     b. If missing, display error: "Please select [option name]" and exit
     c. Query for specific variant SKU based on options
     d. If variant not found, display error: "Selected options not available" and exit
  4. System validates quantity:
     a. If quantity < 1, set to 1
     b. If quantity > 99, set to 99 and display warning: "Maximum quantity is 99"
  5. System checks inventory:
     a. Query current available stock for product/variant
     b. If stock = 0, display error: "Product out of stock" and exit
     c. If quantity > stock:
        - Display warning: "Only [stock] available. Quantity adjusted."
        - Set quantity to available stock
  6. System retrieves or creates cart:
     a. If user logged in, query cart from database by user ID
     b. If anonymous, check session for cart ID or create new cart
     c. If no cart exists, create new cart record
  7. System checks if item already in cart:
     a. Search cart items for matching product ID and variant options
     b. If found, update quantity (existing + new, max 99)
     c. If not found, add new cart item record
  8. System calculates cart item totals:
     a. Get current product price
     b. Calculate line total: price × quantity
     c. Update cart item record with price and total
  9. System updates cart totals:
     a. Sum all cart item line totals
     b. Update cart record with subtotal and timestamp
  10. System saves cart:
      a. If logged in user, update cart in database
      b. If anonymous, store cart ID in session
  11. System logs add-to-cart event for analytics
- **Output**:
  - Success:
    - Confirmation message: "[Product Name] added to cart"
    - Cart icon badge updates with item count
    - Option to "View Cart" or "Continue Shopping"
    - If quantity adjusted, display adjustment message
  - Failure:
    - Specific error message displayed
    - Product remains on product page
    - Cart unchanged
  - Updated Values:
    - Cart item count
    - Cart subtotal
    - Last modified timestamp
- **Priority**: High
- **Dependencies**:
  - FR10 (Product Catalog Management)
  - FR11 (Inventory Management)
  - FR13 (Session Management for Anonymous Users)
  - FR14 (User Cart Management)
  - Database: Products, ProductVariants, Inventory, Carts, CartItems tables
```

### Example 3: Payment Processing

```markdown
**FR3: Process Credit Card Payment**

- **Description**: The system shall process credit card payments through payment
  gateway with validation, fraud detection, and transaction logging
- **Maps to BR**: BR8 (Enable Secure Payment Processing)
- **Actors**: Customer, Payment Gateway (external system), Admin User (for refunds)
- **Preconditions**:
  - User has items in cart with total > $0
  - Shipping address is provided and validated
  - Billing address is provided and validated
  - Payment gateway integration is active
  - SSL/TLS encryption is active
- **Input**:
  - Card Number (required, 13-19 digits, Luhn algorithm validated)
  - Expiration Month (required, 01-12)
  - Expiration Year (required, current year or future, 4 digits)
  - CVV (required, 3-4 digits depending on card type)
  - Cardholder Name (required, alphabetic with spaces, 2-100 characters)
  - Billing Address (required, structured address object)
  - Save Card (optional, boolean, for registered users only)
- **Process**:
  1. System validates card number format:
     a. Check length (13-19 digits)
     b. Validate using Luhn algorithm
     c. Identify card type (Visa, Mastercard, Amex, Discover)
     d. If invalid, display error: "Invalid card number" and exit
  2. System validates expiration date:
     a. Check month is 01-12
     b. Check year is current year or future
     c. If current year, check month is current month or future
     d. If expired, display error: "Card has expired" and exit
  3. System validates CVV:
     a. For Amex: 4 digits required
     b. For other cards: 3 digits required
     c. If invalid, display error: "Invalid security code" and exit
  4. System performs pre-authorization checks:
     a. Calculate order total (subtotal + tax + shipping - discounts)
     b. Verify total matches displayed amount
     c. Check for duplicate transaction (same amount within 5 minutes)
     d. If duplicate detected, prompt user for confirmation
  5. System creates payment transaction record:
     a. Generate unique transaction ID
     b. Store masked card number (last 4 digits only)
     c. Store card type, expiration date
     d. Set status to "Pending"
     e. Log timestamp, IP address, user agent
  6. System prepares payment gateway request:
     a. Format data per gateway API specification
     b. Include transaction ID, amount, currency
     c. Include customer billing information
     d. Include order reference number
     e. Do NOT log or store full card details
  7. System sends payment request to gateway:
     a. Use HTTPS POST to gateway API endpoint
     b. Include authentication credentials in header
     c. Set timeout to 30 seconds
     d. If timeout or connection error:
        - Set transaction status to "Failed"
        - Display error: "Payment could not be processed. Please try again."
        - Exit process
  8. System receives gateway response:
     a. Parse response JSON/XML
     b. Extract authorization code, gateway transaction ID, status
  9. If payment declined:
     a. Update transaction status to "Declined"
     b. Log decline reason code
     c. Display user-friendly message based on decline reason:
        - "Card declined. Please check your card details or use another card."
        - "Insufficient funds. Please use another payment method."
     d. Exit process
  10. If payment approved:
      a. Update transaction status to "Authorized"
      b. Store gateway transaction ID and authorization code
      c. Update order status to "Payment Received"
      d. Trigger order fulfillment workflow (FR25)
      e. Send order confirmation email (FR23)
      f. If "Save Card" checked and user logged in:
         - Tokenize card with payment gateway
         - Store token and masked card details in database
         - Set card as default if it's user's first card
  11. System logs complete transaction:
      a. Record all transaction details (excluding full card number)
      b. Include timestamps, status changes, gateway responses
      c. Flag for fraud review if suspicious patterns detected
  12. System clears shopping cart
  13. System generates receipt
- **Output**:
  - Success:
    - Order confirmation page with order number
    - Transaction receipt with masked card details
    - Confirmation email sent
    - Order status updated in database
    - Cart cleared
    - Redirect to order tracking page
  - Failure:
    - User-friendly error message (never expose technical details)
    - User remains on payment page
    - Card fields cleared for security
    - Order status remains "Pending Payment"
    - Option to try again or use different payment method
  - Transaction Record:
    - Transaction ID
    - Status (Authorized/Declined/Failed)
    - Timestamp
    - Amount
    - Masked card number
    - Gateway response
- **Priority**: High
- **Dependencies**:
  - FR15 (Cart Management)
  - FR20 (Address Validation)
  - FR23 (Email Notification Service)
  - FR25 (Order Fulfillment Workflow)
  - FR30 (Fraud Detection)
  - External: Payment Gateway API (Stripe/PayPal/etc.)
  - External: PCI DSS compliance requirements
  - Database: Orders, Transactions, SavedPaymentMethods tables
```

### Example 4: Report Generation

```markdown
**FR4: Generate Sales Report by Date Range**

- **Description**: The system shall generate sales reports for specified date
  ranges with filtering, sorting, and export options for authorized users
- **Maps to BR**: BR12 (Enable Data-Driven Decision Making)
- **Actors**: Admin User, Sales Manager, Finance Manager
- **Preconditions**:
  - User is authenticated
  - User has "Reports.View" permission
  - At least one completed sale exists in database
- **Input**:
  - Start Date (required, date format YYYY-MM-DD, cannot be future date)
  - End Date (required, date format YYYY-MM-DD, must be ≥ Start Date, cannot be future date)
  - Group By (optional, enum: Daily/Weekly/Monthly, default: Daily)
  - Filters (optional):
    - Product Category (multi-select, list of category IDs)
    - Sales Channel (multi-select: Online/In-Store/Mobile App)
    - Region (multi-select, list of region IDs)
    - Customer Type (multi-select: New/Returning/VIP)
  - Sort By (optional, enum: Date/Revenue/Units, default: Date)
  - Sort Order (optional, enum: Ascending/Descending, default: Descending)
  - Export Format (optional, enum: PDF/Excel/CSV, default: PDF)
- **Process**:
  1. System validates user permissions:
     a. Check if user has "Reports.View" permission
     b. If not, display error: "Access denied" and exit
     c. Check if user has "Reports.Export" permission (needed for export)
  2. System validates date inputs:
     a. Verify dates are in valid format (YYYY-MM-DD)
     b. Verify dates are not future dates
     c. Verify End Date ≥ Start Date
     d. If date range > 2 years, display warning: "Large date range may take longer to process"
     e. If validation fails, display specific error and exit
  3. System builds database query:
     a. Base query: SELECT from Orders table
     b. Add date range filter: WHERE order_date BETWEEN start AND end
     c. Add status filter: AND status = 'Completed'
     d. Add optional filters if provided:
        - Product category joins and filters
        - Sales channel filter
        - Region filter
        - Customer type filter
  4. System executes query with timeout:
     a. Set query timeout to 60 seconds
     b. Execute query
     c. If timeout, display error: "Report generation taking too long. Please narrow your criteria."
  5. System processes results:
     a. Group data by specified grouping (Daily/Weekly/Monthly)
     b. Calculate metrics for each group:
        - Total Revenue
        - Total Units Sold
        - Average Order Value
        - Number of Orders
        - Number of Unique Customers
     c. Calculate summary totals across all groups
     d. Apply sorting based on Sort By and Sort Order
  6. System calculates additional insights:
     a. Period-over-period comparison (vs. previous equivalent period)
     b. Top 5 products by revenue
     c. Top 5 products by units
     d. Growth rate percentage
  7. System generates report output:
     a. If viewing in browser:
        - Render HTML report with responsive table
        - Include charts/graphs using charting library
        - Add print-friendly stylesheet
     b. If exporting:
        - Generate file in requested format
        - Include company logo and branding
        - Add report metadata (generated date, user, filters applied)
  8. System logs report generation:
     a. Record user ID, report type, parameters
     b. Record execution time
     c. If exported, record file format and size
  9. If export requested:
     a. Generate unique filename: "Sales_Report_YYYY-MM-DD_to_YYYY-MM-DD.[ext]"
     b. Create file in temp storage
     c. Trigger download to user's browser
     d. Schedule file deletion after 24 hours
- **Output**:
  - Success (View):
    - Report displayed in browser with:
      - Summary metrics at top
      - Detailed breakdown table
      - Visual charts/graphs
      - Filter tags showing applied filters
      - Export button
      - Print button
  - Success (Export):
    - File download initiated
    - Confirmation message: "Report exported successfully"
    - File contains:
      - Report title and date range
      - Filters applied
      - Summary metrics
      - Detailed data table
      - Generated timestamp
      - Page numbers (for PDF)
  - Failure:
    - Specific error message
    - User remains on report criteria page
    - No file generated
  - No Data:
    - Message: "No sales data found for specified criteria"
    - Suggestion to adjust filters
- **Priority**: Medium
- **Dependencies**:
  - FR8 (User Authentication and Authorization)
  - FR9 (Permission Management)
  - Database: Orders, OrderItems, Products, Categories, Customers tables
  - Library: PDF generation library (e.g., wkhtmltopdf)
  - Library: Excel generation library (e.g., Apache POI)
  - Library: Chart generation library (e.g., Chart.js)
```

---

## Best Practices

### 1. Start with Business Requirements

- **Review all related BRs** before writing FRs
- **Ensure each FR maps to at least one BR**
- **Get BR approval** before creating FRs
- **Validate understanding** with stakeholders

### 2. Use Standard Format

**Consistent structure** makes requirements easier to:
- Read and understand
- Review and approve
- Trace and test
- Maintain and update

**Template adherence:**
- All FRs follow the same structure
- Required fields are always completed
- Optional fields are used consistently

### 3. Be Thorough with Process Flows

**Cover all paths:**
- Normal/happy path
- Alternative flows
- Error conditions
- Edge cases
- Boundary conditions

**Use clear numbering:**
```markdown
1. Main step
   a. Sub-step
   b. Sub-step
      i. Detailed sub-step
2. Next main step
```

### 4. Define Clear Acceptance Criteria

Each FR should answer: "How will we know this is correctly implemented?"

**Good acceptance criteria:**
```markdown
**Acceptance Criteria:**
- User can successfully update profile with valid data
- System displays specific error messages for each validation failure
- Email verification sent when email address is changed
- Changes persist after logout and re-login
- Audit log records profile changes with timestamp and user ID
```

### 5. Collaborate Across Teams

**Involve:**
- **Business Analysts** - Ensure alignment with business needs
- **Developers** - Confirm technical feasibility
- **Testers** - Verify testability
- **UX Designers** - Coordinate on user experience (without dictating design)
- **Security Team** - Address security requirements
- **Operations** - Consider deployment and operational aspects

### 6. Handle Dependencies Explicitly

**Document all dependencies:**
- Other functional requirements
- External systems and APIs
- Database tables and schemas
- Third-party services
- Specific versions or configurations

**Dependency format:**
```markdown
**Dependencies**:
- FR15 (User Authentication) - Required for user identification
- FR23 (Email Service) - Required for sending notifications
- Payment Gateway API v2.1 - Must be configured and accessible
- Database: Users, Orders, Transactions tables must exist
```

### 7. Version Control

**Track changes:**
- Use version numbers (1.0, 1.1, 2.0)
- Document change history
- Note impact on dependent FRs and test cases
- Get approval for changes

**Change template:**
```markdown
**Change History**

| Version | Date | Author | Changes | Impact |
|---------|------|--------|---------|--------|
| 1.0 | 2025-01-15 | J. Smith | Initial creation | None |
| 1.1 | 2025-01-22 | J. Smith | Added password complexity rules | TC3, TC4 |
| 2.0 | 2025-02-05 | M. Johnson | Changed lockout from 3 to 5 attempts | TC5, TC6 |
```

### 8. Review and Validate

**Peer review checklist:**
- Completeness - All fields filled, all scenarios covered
- Clarity - Unambiguous, easy to understand
- Consistency - Aligns with other FRs, uses standard terminology
- Correctness - Accurately reflects business need
- Testability - Can be objectively verified
- Traceability - Links to BRs established

**Stakeholder validation:**
- Walkthrough sessions with business stakeholders
- Developer feasibility review
- QA testability review
- Security review (for sensitive functions)

---

## Common Pitfalls

### Pitfall 1: Too Vague or High-Level

**Bad Example:**
```markdown
**FR1: User Management**

- **Description**: The system handles user accounts
- **Process**: Users are managed
```

**Why it's bad:** Doesn't specify what the system does

**Good Alternative:**
```markdown
**FR1: Create New User Account**

- **Description**: The system shall allow administrators to create new user
  accounts with role assignment and email notification
- **Process**:
  1. Admin enters user details (username, email, first name, last name, role)
  2. System validates all required fields and email format
  3. System checks username and email are unique
  4. System creates user record with "Pending" status
  5. System generates random temporary password
  6. System sends welcome email with login credentials
  7. System logs account creation event
```

### Pitfall 2: Specifying Implementation Technology

**Bad Example:**
```markdown
**FR2: User Authentication Using JWT Tokens**

- **Description**: The system shall use JSON Web Tokens (JWT) stored in localStorage
  to authenticate users, with token refresh implemented using React Context API
```

**Why it's bad:** Specifies technical implementation (JWT, localStorage, React)

**Good Alternative:**
```markdown
**FR2: User Session Management**

- **Description**: The system shall maintain authenticated user sessions with
  secure session tokens, automatic timeout, and session renewal capability
- **Process**:
  1. Upon successful login, system creates unique session identifier
  2. Session remains active for 24 hours of activity
  3. System refreshes session on each user action
  4. Session expires after 30 minutes of inactivity
  5. User can manually end session via logout
```

### Pitfall 3: Missing Error Conditions

**Bad Example:**
```markdown
**FR3: Process Payment**

- **Process**:
  1. Collect payment information
  2. Submit to payment gateway
  3. Complete order
```

**Why it's bad:** No error handling, validation, or alternative flows

**Good Alternative:**
```markdown
**FR3: Process Payment**

- **Process**:
  1. Validate payment information format
     a. If invalid, display specific error and exit
  2. Submit payment request to gateway with 30-second timeout
     a. If timeout or connection error, display error and exit
  3. Receive gateway response
  4. If payment declined:
     a. Display user-friendly decline message
     b. Log decline reason
     c. Allow user to retry with different payment method
  5. If payment approved:
     a. Update order status
     b. Send confirmation email
     c. Clear shopping cart
```

### Pitfall 4: Unclear or Ambiguous Language

**Bad Example:**
```markdown
- **Input**: Username (reasonable length)
- **Process**: System validates the input appropriately
- **Output**: User sees a message
```

**Why it's bad:** "Reasonable", "appropriately", "a message" are not specific

**Good Alternative:**
```markdown
- **Input**: Username (6-50 alphanumeric characters, case-insensitive)
- **Process**: System validates username is between 6-50 characters and contains
  only letters and numbers
- **Output**: If valid, display "Username available"; if invalid, display
  "Username must be 6-50 alphanumeric characters"
```

### Pitfall 5: No Traceability to Business Requirements

**Bad Example:**
```markdown
**FR10: Implement Dark Mode**

- **Maps to BR**: None
```

**Why it's bad:** Not linked to any business need or value

**Good Alternative:**
```markdown
**FR10: Theme Preference Selection**

- **Maps to BR**: BR15 (Improve User Experience and Accessibility)
- **Description**: The system shall allow users to select their preferred display
  theme to accommodate different viewing preferences and accessibility needs
```

### Pitfall 6: Combining Multiple Functions

**Bad Example:**
```markdown
**FR5: User Management System**

- **Description**: Users can register, login, update profiles, reset passwords,
  delete accounts, and manage preferences
```

**Why it's bad:** Too broad, should be separate FRs

**Good Alternative:**
- FR5: User Registration
- FR6: User Login
- FR7: User Profile Update
- FR8: Password Reset
- FR9: Account Deletion
- FR10: User Preferences Management

### Pitfall 7: Not Testable

**Bad Example:**
```markdown
**FR12: Fast Search**

- **Output**: Search results appear quickly
```

**Why it's bad:** "Quickly" is subjective and not measurable

**Good Alternative:**
```markdown
**FR12: Product Search with Performance Requirements**

- **Output**: Search results display within 2 seconds for 95% of queries
- **Measurement**: Response time measured from Enter key press to results display
```

---

## Attributes Reference

### Complete Functional Requirement Attributes

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| **ID** | String | Yes | Unique identifier | FR1, FR2, FR3 |
| **Title** | String | Yes | Brief, descriptive name | User Profile Update |
| **Description** | Text | Yes | Detailed explanation | The system shall allow... |
| **Maps to BR** | List | Yes | Related Business Requirements | BR1, BR3 |
| **Actors** | List | Yes | Who interacts with function | Registered Customer, Admin |
| **Preconditions** | List | Yes | Required state before execution | User is logged in |
| **Input** | List | Yes | Required data and format | Email (required, valid format) |
| **Process** | Text | Yes | Step-by-step system behavior | 1. Validate input... |
| **Output** | Text | Yes | Results and responses | Success message displayed |
| **Priority** | Enum | Yes | High / Medium / Low | High |
| **Dependencies** | List | No | Related FRs and systems | FR15, Payment Gateway API |
| **Version** | String | Yes | Version number | 1.0, 1.1, 2.0 |
| **Status** | Enum | Yes | Current state | Draft / Approved / Implemented |
| **Created Date** | Date | Yes | When FR was created | 2025-01-15 |
| **Created By** | String | Yes | Author name | John Smith |
| **Last Modified Date** | Date | Yes | Last update date | 2025-01-20 |
| **Last Modified By** | String | Yes | Who made last change | Jane Doe |
| **Acceptance Criteria** | List | No | How to verify completion | User can successfully... |
| **Assumptions** | List | No | Key assumptions | Users have valid email |
| **Constraints** | List | No | Technical or business limits | Must complete in <5 seconds |
| **Related Test Cases** | List | No | Linked TCs | TC1, TC2, TC5 |
| **Notes** | Text | No | Additional information | Security review required |

### Status Definitions

| Status | Definition | Who Can Set | Next Status |
|--------|------------|-------------|-------------|
| **Draft** | Being written, not yet reviewed | Business Analyst | Approved |
| **Approved** | Reviewed and approved | Product Owner | In Development |
| **In Development** | Being implemented by dev team | Developer | Implemented |
| **Implemented** | Development complete, code committed | Developer | Tested |
| **Tested** | All related test cases passed | QA Engineer | Deployed |
| **Deployed** | Live in production | DevOps | N/A |
| **Deferred** | Postponed to future release | Product Owner | Draft (when revisited) |
| **Deprecated** | No longer valid or replaced | Business Analyst | N/A |

---

## Document Templates

### Minimal Functional Requirement Template

```markdown
**FR[#]: [Title]**

- **Description**: [What the system does]
- **Maps to BR**: BR[#]
- **Actors**: [Who interacts]
- **Preconditions**: [Required state]
- **Input**: [Required data with formats]
- **Process**: [Step-by-step behavior]
- **Output**: [Results produced]
- **Priority**: High / Medium / Low
- **Dependencies**: [Related FRs/systems]
```

### Extended Functional Requirement Template

```markdown
**FR[#]: [Title]**

**Version**: 1.0
**Status**: Draft
**Created**: YYYY-MM-DD by [Author]
**Last Modified**: YYYY-MM-DD by [Author]

---

**Description**
[Detailed explanation of what the system does]

**Maps to BR**
- BR[#]: [Business Requirement Title]
- BR[#]: [Business Requirement Title]

**Actors**
- [Actor 1 - Role/System]
- [Actor 2 - Role/System]

**Preconditions**
- [Precondition 1]
- [Precondition 2]
- [Precondition 3]

**Input**
- [Field Name] (required/optional, data type, format, validation rules)
- [Field Name] (required/optional, data type, format, validation rules)

**Process**
1. [Main step 1]
   a. [Sub-step]
   b. [Sub-step]
2. If [condition]:
   a. [Action]
   b. [Action]
3. Else:
   a. [Alternative action]
4. [Main step 2]

**Output**
- Success:
  - [Output item 1]
  - [Output item 2]
- Failure:
  - [Error message]
  - [System state]

**Priority**: High / Medium / Low

**Dependencies**
- FR[#] ([FR Title])
- [External System/API]
- Database: [Required tables]

**Acceptance Criteria**
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

**Assumptions**
- [Assumption 1]
- [Assumption 2]

**Constraints**
- [Constraint 1]
- [Constraint 2]

**Security Considerations**
- [Security requirement 1]
- [Security requirement 2]

**Performance Requirements**
- [Performance requirement 1]
- [Performance requirement 2]

**Notes**
[Additional information, open questions, or clarifications needed]

---

**Change History**

| Version | Date | Author | Changes | Impact |
|---------|------|--------|---------|--------|
| 1.0 | YYYY-MM-DD | [Name] | Initial creation | None |

**Review & Approval**

| Role | Name | Status | Date |
|------|------|--------|------|
| Business Analyst | | Pending | |
| Product Owner | | Pending | |
| Tech Lead | | Pending | |
| QA Lead | | Pending | |
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-04 | [Your Name] | Initial document creation |

---

**End of Functional Requirements Guide**
