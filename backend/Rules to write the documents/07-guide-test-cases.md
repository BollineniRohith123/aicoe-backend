# Guide to Writing Test Cases

## Table of Contents
1. [Overview](#overview)
2. [Purpose and Definition](#purpose-and-definition)
3. [Structure](#structure)
4. [Writing Guidelines](#writing-guidelines)
5. [Quality Checklist](#quality-checklist)
6. [Test Case Types](#test-case-types)
7. [Examples](#examples)
8. [Best Practices](#best-practices)
9. [Common Pitfalls](#common-pitfalls)
10. [Attributes Reference](#attributes-reference)

---

## Overview

Test Cases (TC) verify that Functional Requirements are correctly implemented and that the system meets Business Requirements. They provide step-by-step instructions for validating system behavior.

### Document Hierarchy
```
Business Requirements (BR)
    ↓ maps to
Functional Requirements (FR)
    ↓ maps to
Test Cases (TC)  ← YOU ARE HERE
```

### Naming Convention
- **Format**: TC1, TC2, TC3, TC4, ...
- **Rule**: Each Test Case must have a unique identifier
- **Best Practice**: Never reuse IDs, even for deleted test cases
- **Traceability**: Each TC must map to at least one FR

---

## Purpose and Definition

### What is a Test Case?

A Test Case is a set of conditions, steps, and expected results used to validate that a specific system function works correctly. It defines:
- **What** is being tested
- **How** to test it (step-by-step instructions)
- **What** the expected result should be
- **When** the test passes or fails

### What Test Cases Are NOT

Test Cases should NOT be:
- Vague or ambiguous
- Impossible to reproduce
- Dependent on other test cases
- Missing expected results
- Written without knowing the functional requirements

### Key Characteristics

Good Test Cases are:
1. **Explicit** - Clear, step-by-step instructions
2. **Reproducible** - Anyone can execute and get same results
3. **Independent** - Can be run in isolation
4. **Complete** - Covers all relevant scenarios
5. **Traceable** - Linked to Functional Requirements
6. **Maintainable** - Easy to update when requirements change

---

## Structure

Each Test Case should include the following components:

```markdown
**TC[#]: [Clear, Descriptive Test Case Title]**

- **Description**: What is being tested
- **Maps to FR**: FR[#], FR[#]
- **Test Type**: Functional / Integration / System / Acceptance / Regression
- **Priority**: High / Medium / Low
- **Preconditions**: Setup required before test execution
- **Test Data**: Specific data to be used
- **Test Steps**: Numbered, step-by-step instructions with expected results
- **Expected Results**: What should happen at each step (can be in table format)
- **Actual Results**: [To be filled during execution]
- **Status**: Not Run / Pass / Fail / Blocked
- **Notes**: Additional information, dependencies, or observations
```

### Component Descriptions

**Title**
- Clear, specific description of what's being tested
- Should indicate the scenario (positive/negative/edge case)
- Examples: "Successful Login with Valid Credentials", "Login Failure with Invalid Password"

**Description**
- Brief explanation of the test purpose
- What functionality is being validated
- Why this test is important

**Maps to FR**
- List all Functional Requirements this TC validates
- Required for traceability
- Example: FR1, FR2

**Test Type**
- **Functional**: Tests specific function or feature
- **Integration**: Tests interaction between components
- **System**: Tests complete end-to-end workflows
- **Acceptance**: Validates business requirements (UAT)
- **Regression**: Re-tests after changes to ensure no breaks
- **Smoke**: Quick validation that basic functions work
- **Performance**: Tests speed, load, scalability
- **Security**: Tests security controls and vulnerabilities
- **Usability**: Tests user experience and ease of use

**Priority**
- **High**: Critical functionality, must pass for release
- **Medium**: Important but not blocking
- **Low**: Nice-to-have, can defer if needed

**Preconditions**
- All setup needed before test starts
- Test data that must exist
- System state requirements
- User accounts, permissions
- Example: "User testuser01 with password Test@123 exists and is active"

**Test Data**
- Specific values to use in the test
- Must be concrete, not placeholders
- Include valid and invalid data as appropriate
- Format: "Field Name: Value"

**Test Steps**
- Numbered instructions (one action per step)
- Clear, explicit actions
- Include both user actions and system checks
- Can be formatted as table with Expected Results column

**Expected Results**
- What should happen at each step
- Observable, measurable outcomes
- Specific messages, states, or values
- Can be inline with steps or separate section

**Actual Results**
- Filled in during test execution
- What actually happened
- If different from expected, this is a defect
- Include screenshots or logs for failures

**Status**
- **Not Run**: Test not yet executed
- **Pass**: All steps passed, actual = expected
- **Fail**: One or more steps failed, actual ≠ expected
- **Blocked**: Cannot execute due to dependency or defect
- **Skipped**: Intentionally not run (e.g., not applicable to this release)

**Notes**
- Additional context
- Known issues or limitations
- Special instructions for testers
- Links to related defects or requirements

---

## Writing Guidelines

### 1. Be Explicit and Reproducible

Anyone should be able to execute the test and get the same results.

**Good Example:**
```markdown
**Test Steps:**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to https://app.example.com/login | Login page displays with username field, password field, and "Login" button |
| 2 | Enter "testuser01" in Username field | Text "testuser01" appears in field |
| 3 | Enter "Test@Pass123" in Password field | Password characters are masked (shown as dots or asterisks) |
| 4 | Click "Login" button | User redirected to https://app.example.com/dashboard within 2 seconds |
| 5 | Verify page header shows "Welcome, Test User" | Header displays "Welcome, Test User" in top-right corner |
```

**Bad Example:**
```markdown
**Test Steps:**

1. Go to login page
2. Log in
3. Check if it worked
```
*Why it's bad: Not specific, no details on URLs, credentials, or what "worked" means*

### 2. Use Specific Test Data

Never use placeholders or generic values.

**Good Example:**
```markdown
**Test Data:**
- Username: "testuser01"
- Password: "Test@Pass123"
- Email: "testuser01@example.com"
- First Name: "John"
- Last Name: "Smith"
- Phone: "+1-555-0100"
```

**Bad Example:**
```markdown
**Test Data:**
- Username: [valid username]
- Password: [valid password]
- Email: [user's email]
```
*Why it's bad: Not specific, tester has to guess what values to use*

### 3. Write Clear, Numbered Steps

One action per step.

**Good Example:**
```markdown
1. Click the "Add to Cart" button
2. Observe the cart icon in the top-right corner
3. Verify the cart badge shows "1"
4. Click the cart icon
5. Verify the cart drawer opens from the right side
6. Verify the product "Blue Widget" appears in cart list
7. Verify the quantity shows "1"
8. Verify the price shows "$29.99"
```

**Bad Example:**
```markdown
1. Add item to cart and check that it appears with the right quantity and price
```
*Why it's bad: Multiple actions and verifications in one step, not clear what to do*

### 4. Define Clear Expected Results

Observable, measurable outcomes.

**Good Example:**
```markdown
**Expected Result:**
- Error message displays: "Invalid username or password"
- Error message appears in red text below the login form
- Username field retains entered value "testuser01"
- Password field is cleared
- User remains on login page (URL: https://app.example.com/login)
- Focus moves to password field
```

**Bad Example:**
```markdown
**Expected Result:**
- Shows error
- Doesn't work
```
*Why it's bad: Not specific, no details on what error or what "doesn't work" means*

### 5. Cover Both Positive and Negative Scenarios

Test what should work AND what should be rejected.

**Positive Test:**
```markdown
**TC1: Successful User Registration with Valid Data**
- Tests that users can register with all valid, required data
```

**Negative Tests:**
```markdown
**TC2: User Registration Fails with Missing Required Field**
**TC3: User Registration Fails with Invalid Email Format**
**TC4: User Registration Fails with Weak Password**
**TC5: User Registration Fails with Duplicate Username**
```

### 6. Include Edge Cases and Boundary Conditions

Test limits and unusual but valid inputs.

**Examples:**
```markdown
**TC10: Password with Exactly 8 Characters (Minimum Boundary)**
**TC11: Password with 128 Characters (Maximum Boundary)**
**TC12: Username with Special Characters**
**TC13: Profile Update with All Optional Fields Empty**
**TC14: Shopping Cart with 99 Items (Maximum Quantity)**
```

### 7. Keep Tests Independent

Each test should stand alone and not depend on other tests.

**Good Practice:**
```markdown
**TC5: Add Item to Cart**

**Preconditions:**
- User "testuser01" is logged in
- Shopping cart is empty
- Product "Blue Widget" (ID: 12345) exists and is in stock

**Test Steps:**
1. Navigate to product page: https://app.example.com/product/12345
2. Click "Add to Cart" button
3. Verify success message displays
...
```

**Bad Practice:**
```markdown
**TC5: Add Item to Cart**

**Preconditions:**
- TC4 (User Login) has been executed successfully
- Use the same session from TC4

**Test Steps:**
1. From the dashboard (where TC4 ended), click Products
...
```
*Why it's bad: Depends on TC4 being run first; if TC4 fails, TC5 can't run*

---

## Quality Checklist

Before finalizing a Test Case, verify:

- [ ] **Are test steps clear and unambiguous?**
  - Each step describes one specific action
  - No room for interpretation

- [ ] **Can the test be executed by someone unfamiliar with the feature?**
  - All necessary information provided
  - No assumed knowledge

- [ ] **Are expected results specific and measurable?**
  - Observable outcomes
  - Specific values, messages, or states

- [ ] **Does it test a specific scenario or condition?**
  - Focused on one path or case
  - Not trying to test multiple things

- [ ] **Is test data clearly specified?**
  - Concrete values provided
  - No placeholders or generic terms

- [ ] **Are preconditions clearly stated?**
  - All setup requirements documented
  - Test data existence confirmed

- [ ] **Does it map to at least one Functional Requirement?**
  - Traceability established
  - Validates specific FR

- [ ] **Is the test independent?**
  - Can be run in isolation
  - Doesn't depend on other tests

- [ ] **Is the priority appropriate?**
  - Aligns with FR priority
  - Reflects business criticality

- [ ] **Are all fields completed?**
  - No TBD or blank sections
  - Ready for execution

---

## Test Case Types

### 1. Functional Test Cases

Test specific features or functions against functional requirements.

**Example:**
```markdown
**TC1: User Profile Update with Valid Data**
- **Maps to FR**: FR7 (User Profile Management)
- **Test Type**: Functional
- Tests that profile updates work correctly with valid inputs
```

### 2. Positive Test Cases

Test expected, valid behavior (happy path).

**Example:**
```markdown
**TC5: Successful Payment with Valid Credit Card**
- Valid card number, valid expiration, valid CVV
- Expected: Payment processes successfully
```

### 3. Negative Test Cases

Test invalid inputs or error conditions.

**Example:**
```markdown
**TC6: Payment Fails with Expired Credit Card**
- Valid card number, expired date, valid CVV
- Expected: Error message "Card has expired"
```

### 4. Boundary Test Cases

Test minimum, maximum, and edge values.

**Examples:**
```markdown
**TC10: Username with 6 Characters (Minimum Boundary)**
**TC11: Username with 50 Characters (Maximum Boundary)**
**TC12: Username with 5 Characters (Below Minimum - Should Fail)**
**TC13: Username with 51 Characters (Above Maximum - Should Fail)**
```

### 5. Integration Test Cases

Test interaction between multiple components or systems.

**Example:**
```markdown
**TC20: Order Confirmation Email Sent After Payment**
- **Maps to FR**: FR15 (Payment Processing), FR23 (Email Service)
- **Test Type**: Integration
- Validates that payment system triggers email system correctly
```

### 6. End-to-End Test Cases

Test complete user workflows from start to finish.

**Example:**
```markdown
**TC50: Complete Shopping Journey - Browse to Order Confirmation**
- **Test Type**: System / End-to-End
- Tests full flow: browse products → add to cart → checkout → payment → confirmation
```

### 7. Regression Test Cases

Re-test after changes to ensure no existing functionality broke.

**Example:**
```markdown
**TC100: Login Regression After Profile Update Feature**
- **Test Type**: Regression
- Ensures login still works after profile update changes were deployed
```

### 8. Security Test Cases

Test authentication, authorization, data protection.

**Examples:**
```markdown
**TC200: Unauthorized User Cannot Access Admin Dashboard**
**TC201: SQL Injection Prevention in Search Field**
**TC202: Password Not Visible in Page Source or Network Tab**
```

### 9. Performance Test Cases

Test speed, load handling, scalability.

**Examples:**
```markdown
**TC300: Search Results Display Within 2 Seconds**
**TC301: System Supports 1000 Concurrent Users**
**TC302: Page Load Time Under 3 Seconds**
```

### 10. Usability Test Cases

Test user experience and ease of use.

**Examples:**
```markdown
**TC400: Error Messages Are Clear and Helpful**
**TC401: Form Can Be Completed Using Only Keyboard**
**TC402: Mobile Navigation Is Touch-Friendly**
```

---

## Examples

### Example 1: Successful Login (Positive Test)

```markdown
**TC1: Successful Login with Valid Credentials**

- **Description**: Verify that a user can successfully log in with correct username and password
- **Maps to FR**: FR1 (User Authentication)
- **Test Type**: Functional
- **Priority**: High
- **Preconditions**:
  - Test user account exists with username "testuser01" and password "Test@Pass123"
  - Account is active (not locked, suspended, or deleted)
  - User is logged out
  - Browser cookies cleared
- **Test Data**:
  - Username: "testuser01"
  - Password: "Test@Pass123"
  - URL: https://app.example.com/login

**Test Steps and Expected Results:**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Open browser and navigate to https://app.example.com/login | Login page displays with "Username" field, "Password" field, "Remember Me" checkbox, and "Login" button |
| 2 | Enter "testuser01" in the Username field | Text "testuser01" appears in the field |
| 3 | Enter "Test@Pass123" in the Password field | Password is masked, showing dots or asterisks instead of characters |
| 4 | Click the "Login" button | User is redirected to https://app.example.com/dashboard within 2 seconds |
| 5 | Verify page title is "Dashboard" | Page title in browser tab shows "Dashboard" |
| 6 | Verify welcome message displays in header | Header shows "Welcome, Test User" in top-right corner |
| 7 | Verify navigation menu includes "Home", "Profile", "Settings", "Logout" | All four menu items are visible in left sidebar |
| 8 | Open browser developer tools and check session storage | Session token exists and is a valid UUID format |
| 9 | Verify user can access protected page: navigate to https://app.example.com/profile | Profile page loads successfully without redirecting to login |
| 10 | Click "Logout" button | User is redirected to login page, welcome message disappears |

- **Actual Results**: [To be filled during test execution]
- **Status**: Not Run
- **Execution Date**: [TBD]
- **Executed By**: [TBD]
- **Notes**: Test in Chrome, Firefox, and Safari. Ensure browser cache cleared before each run.
```

### Example 2: Login Failure (Negative Test)

```markdown
**TC2: Login Failure with Invalid Password**

- **Description**: Verify that the system rejects login attempt with incorrect password and displays appropriate error message
- **Maps to FR**: FR1 (User Authentication), FR2 (Failed Login Handling)
- **Test Type**: Functional (Negative)
- **Priority**: High
- **Preconditions**:
  - Test user account exists with username "testuser01" and password "Test@Pass123"
  - Account is active and not locked
  - Failed login counter for testuser01 is 0
  - User is logged out
- **Test Data**:
  - Username: "testuser01" (correct)
  - Password: "WrongPassword123" (incorrect)

**Test Steps and Expected Results:**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to https://app.example.com/login | Login page displays |
| 2 | Enter "testuser01" in Username field | Username "testuser01" appears in field |
| 3 | Enter "WrongPassword123" in Password field | Password is masked |
| 4 | Click "Login" button | Page does not redirect, error message appears |
| 5 | Verify error message text | Error displays: "Invalid username or password" (generic message for security) |
| 6 | Verify error message styling | Error appears in red text with warning icon, below login form |
| 7 | Verify Username field value | Username field still contains "testuser01" (retained) |
| 8 | Verify Password field value | Password field is empty (cleared) |
| 9 | Verify cursor focus | Focus is set to Password field |
| 10 | Verify URL has not changed | URL is still https://app.example.com/login |
| 11 | Check database: query failed_login_attempts table for testuser01 | Failed attempt count = 1, timestamp logged, IP address recorded |
| 12 | Verify user is not authenticated | Attempt to navigate to https://app.example.com/dashboard redirects to login |

- **Actual Results**: [To be filled during test execution]
- **Status**: Not Run
- **Execution Date**: [TBD]
- **Executed By**: [TBD]
- **Notes**: Verify error message does NOT reveal whether username or password was incorrect (security best practice)
```

### Example 3: Account Lockout (Security Test)

```markdown
**TC3: Account Lockout After 5 Failed Login Attempts**

- **Description**: Verify that user account is automatically locked after 5 consecutive failed login attempts within 15 minutes
- **Maps to FR**: FR2 (Failed Login Attempt Handling), FR18 (Account Security)
- **Test Type**: Functional, Security
- **Priority**: High
- **Preconditions**:
  - Test user account exists: username "testuser02", password "Test@Pass456"
  - Account is active and not locked
  - Failed login counter is 0
  - Email service is configured and accessible
  - Test email address testuser02@example.com can receive emails
- **Test Data**:
  - Username: "testuser02"
  - Correct Password: "Test@Pass456"
  - Incorrect Password: "WrongPassword"
  - Email: testuser02@example.com

**Test Steps and Expected Results:**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Record current time for timestamp verification | Time noted: [HH:MM:SS] |
| 2 | Navigate to login page | Login page displays |
| 3 | Attempt login with username "testuser02" and password "WrongPassword" | Error message: "Invalid username or password" |
| 4 | Check database: SELECT failed_attempts FROM login_attempts WHERE username='testuser02' | failed_attempts = 1, timestamp within last minute |
| 5 | Repeat login attempt with wrong password (Attempt 2) | Error message: "Invalid username or password" |
| 6 | Check database: SELECT failed_attempts FROM login_attempts WHERE username='testuser02' | failed_attempts = 2 |
| 7 | Repeat login attempt with wrong password (Attempt 3) | Error message: "Invalid username or password" |
| 8 | Check database: SELECT failed_attempts FROM login_attempts WHERE username='testuser02' | failed_attempts = 3 |
| 9 | Repeat login attempt with wrong password (Attempt 4) | Error message: "Invalid username or password" |
| 10 | Check database: SELECT failed_attempts FROM login_attempts WHERE username='testuser02' | failed_attempts = 4 |
| 11 | Repeat login attempt with wrong password (Attempt 5) | Error message changes to: "Account temporarily locked. Please try again in 30 minutes" |
| 12 | Check database: SELECT status, locked_until FROM users WHERE username='testuser02' | status = 'locked', locked_until = [current time + 30 minutes] |
| 13 | Check email inbox for testuser02@example.com | Email received within 2 minutes with subject "Account Security Alert - Account Locked" |
| 14 | Verify email content | Email contains: account locked notification, timestamp, IP address, "If this wasn't you" warning, support contact |
| 15 | Attempt login with CORRECT password "Test@Pass456" | Login denied, same error: "Account temporarily locked. Please try again in 30 minutes" |
| 16 | Verify user cannot access protected pages | Direct navigation to https://app.example.com/dashboard redirects to login |
| 17 | **[OPTION A]** Wait 30 minutes for lockout to expire | Time elapses |
| 17 | **[OPTION B]** Manually clear lockout in database: UPDATE users SET status='active', locked_until=NULL WHERE username='testuser02' | Database updated (for test efficiency) |
| 18 | Attempt login with CORRECT password "Test@Pass456" | Login succeeds, user redirected to dashboard |
| 19 | Verify dashboard displays welcome message | "Welcome, Test User 02" appears |
| 20 | Check database: SELECT failed_attempts FROM login_attempts WHERE username='testuser02' | failed_attempts = 0 (reset after successful login) |

- **Actual Results**: [To be filled during test execution]
- **Status**: Not Run
- **Execution Date**: [TBD]
- **Executed By**: [TBD]
- **Notes**:
  - For time efficiency in testing, use Option B (manual database unlock) instead of waiting 30 minutes
  - Verify that lockout resets automatically after 30 minutes in at least one test run
  - Test should be run during non-peak hours to avoid impacting real users
  - Document actual IP address used during test for security audit trail
```

### Example 4: Password Validation (Boundary Test)

```markdown
**TC4: Password Validation - Minimum Length Boundary**

- **Description**: Verify that system rejects passwords shorter than 8 characters and accepts passwords with exactly 8 characters
- **Maps to FR**: FR3 (Password Security Requirements)
- **Test Type**: Functional (Negative and Boundary)
- **Priority**: Medium
- **Preconditions**:
  - User is on registration page or password reset page
  - All other required fields are filled with valid data
- **Test Data**:
  - Invalid Password (7 chars): "Test@1A"
  - Valid Password (8 chars minimum): "Test@1Ab"
  - Test Username: "newuser01"
  - Test Email: "newuser01@example.com"

**Test Steps and Expected Results:**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to registration page: https://app.example.com/register | Registration form displays |
| 2 | Enter "newuser01" in Username field | Username accepted |
| 3 | Enter "newuser01@example.com" in Email field | Email accepted, no error |
| 4 | Enter "Test@1A" (7 characters) in Password field | Password field shows masked characters |
| 5 | Click in another field or tab out of Password field | Inline error message displays below password field |
| 6 | Verify error message text | Error displays: "Password must be at least 8 characters" |
| 7 | Verify error message styling | Error in red text with warning icon |
| 8 | Click "Register" button | Form does not submit, same error persists |
| 9 | Verify user remains on registration page | URL still https://app.example.com/register |
| 10 | Clear Password field | Error message disappears |
| 11 | Enter "Test@1Ab" (8 characters - minimum boundary) in Password field | Password field shows masked characters |
| 12 | Tab out of Password field | No error message displays |
| 13 | Enter "Test@1Ab" in Confirm Password field | Password fields match, no error |
| 14 | Click "Register" button | Form submits successfully |
| 15 | Verify success message or redirect | User redirected to dashboard or receives confirmation email |

- **Actual Results**: [To be filled during test execution]
- **Status**: Not Run
- **Execution Date**: [TBD]
- **Executed By**: [TBD]
- **Notes**:
  - Test both inline validation (on blur) and form submission validation
  - Verify validation works the same on registration, password reset, and password change pages
  - Test with 6, 7, 8, 9 character passwords to confirm boundary is exactly 8
```

### Example 5: E-Commerce Add to Cart (Integration Test)

```markdown
**TC5: Add Product to Cart and Verify Cart Update**

- **Description**: Verify that clicking "Add to Cart" successfully adds the product to cart, updates cart count, and reflects correct price
- **Maps to FR**: FR10 (Shopping Cart Management), FR11 (Inventory Tracking)
- **Test Type**: Functional, Integration
- **Priority**: High
- **Preconditions**:
  - Test user "testuser01" is logged in
  - Shopping cart is empty (0 items)
  - Product "Blue Widget" (Product ID: 12345, SKU: BW-BLUE-M) exists
  - Product is published, active, and in stock (available quantity ≥ 5)
  - Current product price is $29.99
- **Test Data**:
  - Product ID: 12345
  - Product Name: "Blue Widget"
  - SKU: BW-BLUE-M
  - Selected Quantity: 2
  - Price: $29.99
  - Expected Line Total: $59.98

**Test Steps and Expected Results:**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to product page: https://app.example.com/product/12345 | Product page displays with product image, name "Blue Widget", price "$29.99", "Add to Cart" button |
| 2 | Verify initial cart badge count | Cart icon in header shows "0" or no badge |
| 3 | Verify "Quantity" field default value | Quantity field shows "1" |
| 4 | Change Quantity field value to "2" | Field updates to show "2" |
| 5 | Click "Add to Cart" button | Button shows loading state briefly (spinner or disabled) |
| 6 | Wait for operation to complete | Loading state ends within 1 second |
| 7 | Verify success message | Green notification appears: "Blue Widget added to cart" |
| 8 | Verify cart badge update | Cart icon badge updates to show "2" (quantity of items) |
| 9 | Verify message includes action buttons | Notification includes "View Cart" and "Continue Shopping" buttons |
| 10 | Click "View Cart" button in notification | User redirected to https://app.example.com/cart |
| 11 | Verify cart page displays | Cart page title is "Shopping Cart" |
| 12 | Verify product appears in cart | Cart shows one line item with product "Blue Widget" |
| 13 | Verify cart item details | Row shows: Product image, Name "Blue Widget", SKU "BW-BLUE-M", Quantity "2", Unit Price "$29.99", Line Total "$59.98" |
| 14 | Verify cart subtotal | Cart subtotal displays "$59.98" |
| 15 | Verify quantity controls | Plus/minus buttons and quantity input field are present |
| 16 | Verify "Remove" button present | Each cart item has a "Remove" or trash icon button |
| 17 | Check database: SELECT * FROM cart_items WHERE user_id=[testuser01_id] AND product_id=12345 | Cart item record exists with quantity=2, price=29.99 |
| 18 | Verify inventory was not decremented | Product inventory still shows original quantity (inventory only decremented at checkout, not add-to-cart) |

- **Actual Results**: [To be filled during test execution]
- **Status**: Not Run
- **Execution Date**: [TBD]
- **Executed By**: [TBD]
- **Notes**:
  - Also test with anonymous (not logged in) user - cart should use session storage
  - Verify cart persists after logout and re-login for authenticated users
  - Test with product that has variants (size, color) in separate test case
  - Verify analytics event is logged for "add_to_cart" action
```

---

## Best Practices

### 1. Write Tests During Requirements Phase

**Benefits:**
- Identifies requirement ambiguities early
- Ensures requirements are testable
- Prevents rework later
- Improves requirement quality

**Process:**
1. Review Business Requirement
2. Review Functional Requirement
3. Write test cases
4. If you can't write clear test case, FR is not clear enough
5. Refine FR based on test case questions

### 2. Use Test Case Templates

**Standard template ensures:**
- Consistency across all test cases
- No missing information
- Easier to review and maintain
- Faster test case creation

### 3. Organize Test Cases by Feature

**Structure:**
```
Login Feature
├── TC1: Successful login with valid credentials
├── TC2: Login failure with invalid password
├── TC3: Login failure with invalid username
├── TC4: Account lockout after failed attempts
├── TC5: Password visibility toggle
└── TC6: Remember me functionality

Password Reset Feature
├── TC10: Request password reset with valid email
├── TC11: Password reset email received
├── TC12: Reset password with valid token
└── TC13: Reset token expires after 24 hours
```

### 4. Maintain Test Data

**Create test data management strategy:**
- **Dedicated test accounts** - Don't use production data
- **Known state** - Test data should have predictable values
- **Reusable** - Same test data for consistent results
- **Documented** - Maintain test data inventory
- **Automated setup** - Scripts to create/reset test data

**Example Test Data Registry:**
```markdown
## User Accounts

| Username | Password | Email | Role | Status | Purpose |
|----------|----------|-------|------|--------|---------|
| testuser01 | Test@Pass123 | testuser01@example.com | Customer | Active | Standard user tests |
| testuser02 | Test@Pass456 | testuser02@example.com | Customer | Active | Security/lockout tests |
| adminuser01 | Admin@Pass789 | admin01@example.com | Admin | Active | Admin function tests |
| lockeduser01 | Locked@Pass321 | locked01@example.com | Customer | Locked | Locked account tests |
```

### 5. Review and Update Test Cases

**When to update test cases:**
- When functional requirements change
- When bugs are found (add regression tests)
- When new scenarios are discovered
- After usability testing reveals edge cases
- When technology changes affect test execution

**Review checklist:**
- Are preconditions still valid?
- Is test data still available?
- Are expected results still accurate?
- Are steps still reproducible?
- Is priority still appropriate?

### 6. Track Test Execution Results

**Maintain execution log:**
```markdown
| TC# | Test Case | Execution Date | Tester | Status | Defect ID | Notes |
|-----|-----------|---------------|--------|--------|-----------|-------|
| TC1 | Successful Login | 2025-01-15 | J. Smith | Pass | - | All steps passed |
| TC2 | Login Failure | 2025-01-15 | J. Smith | Fail | DEF-101 | Error message missing |
| TC3 | Account Lockout | 2025-01-15 | J. Smith | Blocked | - | Email service down |
| TC4 | Password Min Length | 2025-01-16 | M. Johnson | Pass | - | Boundary test passed |
```

### 7. Link Test Cases to Defects

**When test fails:**
1. Document failure in "Actual Results"
2. Take screenshots/videos
3. Collect logs
4. Create defect report
5. Link defect ID to test case
6. Update test case status to "Fail"
7. Re-run test after defect fixed
8. Update status to "Pass" if fixed

### 8. Automate Where Appropriate

**Good candidates for automation:**
- Regression tests (run repeatedly)
- Smoke tests (quick sanity checks)
- Data-driven tests (same steps, different data)
- Performance tests (require measurement)
- API tests (no UI involved)

**Keep manual for:**
- Exploratory testing
- Usability testing
- Visual validation
- Complex user journeys
- Tests that change frequently

### 9. Use Test Management Tools

**Benefits of test management tools:**
- Centralized test case repository
- Traceability matrix automation
- Test execution tracking
- Reporting and metrics
- Integration with defect tracking

**Popular tools:**
- TestRail
- Zephyr
- qTest
- PractiTest
- Azure Test Plans
- JIRA + Xray

### 10. Perform Peer Reviews

**Test case review checklist:**
- [ ] Clear and unambiguous steps
- [ ] Specific expected results
- [ ] Complete preconditions
- [ ] Concrete test data
- [ ] Correct FR mapping
- [ ] Appropriate priority
- [ ] Independent (not dependent on other TCs)
- [ ] Reproducible by others
- [ ] Proper grammar and formatting

---

## Common Pitfalls

### Pitfall 1: Vague Test Steps

**Bad Example:**
```markdown
1. Log in to the system
2. Navigate to the profile page
3. Update information
4. Save changes
5. Verify it worked
```

**Why it's bad:** Not specific, no concrete actions or values

**Good Alternative:**
```markdown
1. Navigate to https://app.example.com/login
2. Enter "testuser01" in Username field
3. Enter "Test@Pass123" in Password field
4. Click "Login" button
5. Click "Profile" link in navigation menu
6. Change "First Name" field from "John" to "Jonathan"
7. Click "Save Changes" button
8. Verify success message displays: "Profile updated successfully"
9. Verify "First Name" field now shows "Jonathan"
```

### Pitfall 2: Multiple Actions Per Step

**Bad Example:**
```markdown
1. Enter username, password, and email, then click Submit
```

**Why it's bad:** Can't identify which action caused a failure

**Good Alternative:**
```markdown
1. Enter "testuser01" in Username field
2. Enter "Test@Pass123" in Password field
3. Enter "test@example.com" in Email field
4. Click "Submit" button
```

### Pitfall 3: No Expected Results

**Bad Example:**
```markdown
1. Click the "Add to Cart" button
2. Check the cart
```

**Why it's bad:** Doesn't specify what "check" means or what should happen

**Good Alternative:**
```markdown
1. Click the "Add to Cart" button
   - Expected: Success message displays "Item added to cart"
2. Click the cart icon in header
   - Expected: Cart drawer opens from right side
3. Verify product "Blue Widget" appears in cart list
   - Expected: Product name "Blue Widget" is visible in cart
4. Verify quantity shows "1"
   - Expected: Quantity field displays "1"
```

### Pitfall 4: Generic or Placeholder Test Data

**Bad Example:**
```markdown
**Test Data:**
- Username: [any valid username]
- Password: [user's password]
- Email: [valid email]
```

**Why it's bad:** Tester has to guess, results not reproducible

**Good Alternative:**
```markdown
**Test Data:**
- Username: "testuser01"
- Password: "Test@Pass123"
- Email: "testuser01@example.com"
- First Name: "John"
- Last Name: "Smith"
```

### Pitfall 5: Dependent Test Cases

**Bad Example:**
```markdown
**TC5: Add Item to Cart**

**Preconditions:**
- TC1, TC2, TC3, TC4 must be executed first
- Use the session from TC4
```

**Why it's bad:** Can't run TC5 independently; if TC4 fails, TC5 is blocked

**Good Alternative:**
```markdown
**TC5: Add Item to Cart**

**Preconditions:**
- User "testuser01" is logged in
- Cart is empty
- Product ID 12345 exists and is in stock
```

### Pitfall 6: Testing Multiple Things in One Test Case

**Bad Example:**
```markdown
**TC10: User Registration and Login and Profile Update**

Tests that user can register, log in, update profile, change password, and log out
```

**Why it's bad:** If step 3 fails, you never test steps 4-5; hard to identify what broke

**Good Alternative:**
Split into separate test cases:
- TC10: User Registration with Valid Data
- TC11: Login with Newly Created Account
- TC12: Profile Update for New User
- TC13: Password Change
- TC14: Logout

### Pitfall 7: No Actual Results Field

**Bad Example:**
```markdown
**Expected Result:** Login succeeds
```

**Why it's bad:** Nowhere to document what actually happened during execution

**Good Alternative:**
```markdown
**Expected Result:** Login succeeds, user redirected to dashboard

**Actual Result:** [To be filled during execution]
- 2025-01-15: Pass - User redirected to dashboard as expected
- 2025-01-22: Fail - Error 500, user not redirected (DEF-105)
- 2025-01-25: Pass - Defect fixed, test passed
```

### Pitfall 8: Ambiguous Pass/Fail Criteria

**Bad Example:**
```markdown
**Expected Result:** Page loads quickly
```

**Why it's bad:** "Quickly" is subjective - 1 second? 5 seconds? 30 seconds?

**Good Alternative:**
```markdown
**Expected Result:** Page loads completely within 3 seconds
**Measurement:** Time from clicking link to "Page Loaded" event in browser
```

---

## Attributes Reference

### Complete Test Case Attributes

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| **ID** | String | Yes | Unique identifier | TC1, TC2, TC3 |
| **Title** | String | Yes | Clear description of test | Successful Login with Valid Credentials |
| **Description** | Text | Yes | What is being tested | Verify user can log in with correct credentials |
| **Maps to FR** | List | Yes | Related Functional Requirements | FR1, FR2 |
| **Test Type** | Enum | Yes | Type of test | Functional / Integration / System / etc. |
| **Priority** | Enum | Yes | Criticality | High / Medium / Low |
| **Preconditions** | List | Yes | Setup required | User testuser01 exists |
| **Test Data** | List | Yes | Specific values | Username: "testuser01", Password: "Test@123" |
| **Test Steps** | List | Yes | Step-by-step actions | 1. Navigate to... |
| **Expected Results** | Text/Table | Yes | What should happen | User redirected to dashboard |
| **Actual Results** | Text | No | What actually happened | [Filled during execution] |
| **Status** | Enum | Yes | Current state | Not Run / Pass / Fail / Blocked |
| **Version** | String | Yes | Version number | 1.0, 1.1, 2.0 |
| **Created Date** | Date | Yes | When TC was created | 2025-01-15 |
| **Created By** | String | Yes | Author name | John Smith |
| **Last Modified Date** | Date | Yes | Last update date | 2025-01-20 |
| **Last Modified By** | String | Yes | Who made last change | Jane Doe |
| **Execution Date** | Date | No | When last executed | 2025-01-25 |
| **Executed By** | String | No | Who executed | Mike Johnson |
| **Execution Duration** | Duration | No | Time to execute | 5 minutes |
| **Environment** | String | No | Test environment | QA, Staging, Production |
| **Build Version** | String | No | Software version tested | v1.2.3 |
| **Browser/Platform** | String | No | Test platform | Chrome 120, Windows 11 |
| **Defect IDs** | List | No | Related defects | DEF-101, DEF-105 |
| **Notes** | Text | No | Additional info | Run after hours due to email delays |
| **Attachments** | Files | No | Screenshots, logs | screenshot.png, error.log |

### Status Definitions

| Status | Definition | Next Status | Action |
|--------|------------|-------------|--------|
| **Not Run** | Test not yet executed | Pass / Fail / Blocked | Execute test |
| **Pass** | All steps passed, actual = expected | Not Run (after change) | Mark as regression test |
| **Fail** | One or more steps failed | Pass (after fix) | Create defect, re-test after fix |
| **Blocked** | Cannot execute due to dependency | Pass / Fail | Remove blocker, execute |
| **Skipped** | Intentionally not run | Not Run | Document reason |
| **In Progress** | Currently being executed | Pass / Fail / Blocked | Complete execution |

---

## Document Templates

### Minimal Test Case Template

```markdown
**TC[#]: [Title]**

- **Description**: [What is being tested]
- **Maps to FR**: FR[#]
- **Test Type**: [Type]
- **Priority**: High / Medium / Low
- **Preconditions**:
  - [Precondition 1]
  - [Precondition 2]
- **Test Data**:
  - [Field: Value]
  - [Field: Value]

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | [Action] | [Expected outcome] |
| 2 | [Action] | [Expected outcome] |

- **Actual Results**: [To be filled during execution]
- **Status**: Not Run
- **Notes**: [Additional information]
```

### Extended Test Case Template

```markdown
**TC[#]: [Title]**

**Version**: 1.0
**Status**: Not Run
**Created**: YYYY-MM-DD by [Author]
**Last Modified**: YYYY-MM-DD by [Author]

---

**Description**
[Detailed explanation of what functionality is being tested and why]

**Maps to FR**
- FR[#]: [Functional Requirement Title]
- FR[#]: [Functional Requirement Title]

**Test Type**
[Functional / Integration / System / Acceptance / Regression / Performance / Security / Usability]

**Priority**
[High / Medium / Low]

**Test Objective**
[Specific goal of this test - what are we validating?]

**Preconditions**
- [Precondition 1]
- [Precondition 2]
- [Precondition 3]

**Test Data**
- [Field Name]: [Specific Value]
- [Field Name]: [Specific Value]
- [Field Name]: [Specific Value]

**Test Environment**
- URL: [Test environment URL]
- Browser: [Chrome / Firefox / Safari / Edge]
- OS: [Windows / macOS / Linux]
- Database: [Test database name]

**Test Steps and Expected Results**

| Step | Action | Expected Result | Actual Result | Pass/Fail |
|------|--------|----------------|---------------|-----------|
| 1 | [Specific action] | [Specific expected outcome] | [To be filled] | [ ] |
| 2 | [Specific action] | [Specific expected outcome] | [To be filled] | [ ] |
| 3 | [Specific action] | [Specific expected outcome] | [To be filled] | [ ] |

**Post-Conditions**
[State of system after test completes]

**Actual Results Summary**
[To be filled during execution]

**Overall Status**
[ ] Not Run
[ ] Pass
[ ] Fail
[ ] Blocked
[ ] Skipped

**Execution Details**
- **Executed By**: [Tester name]
- **Execution Date**: YYYY-MM-DD
- **Execution Time**: [HH:MM]
- **Duration**: [X minutes]
- **Build Version**: [v1.2.3]

**Defects**
[If test failed, list defect IDs]
- DEF-[#]: [Brief description]

**Notes**
[Any additional observations, recommendations, or issues encountered]

**Attachments**
[Screenshots, logs, videos]
- [filename.png] - [Description]
- [errorlog.txt] - [Description]

---

**Change History**

| Version | Date | Author | Changes | Impact |
|---------|------|--------|---------|--------|
| 1.0 | YYYY-MM-DD | [Name] | Initial creation | None |

**Review & Approval**

| Role | Name | Status | Date |
|------|------|--------|------|
| Test Case Author | | Complete | |
| QA Lead | | Approved | |
| Test Manager | | Approved | |
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-04 | [Your Name] | Initial document creation |

---

**End of Test Cases Guide**
