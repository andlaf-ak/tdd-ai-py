# Generic Coding Principles

## Clean Code Principles

### Naming Conventions

#### Functions and Methods
- Use verbs that clearly describe what the function does
- Be specific and descriptive
- Examples: `calculateSum()`, `validateInput()`, `formatCurrency()`

#### Variables
- Use intention-revealing names
- Avoid abbreviations and mental mapping
- Use searchable names for important variables
```
// Bad
d = 5  // elapsed time in days

// Good
elapsedTimeInDays = 5
```

#### Classes
- Use nouns that represent the concept
- Examples: `Calculator`, `PaymentProcessor`, `UserRepository`

### Function Design Rules

#### Single Responsibility Principle
- Functions should do one thing and do it well
- If you can describe the function with "and" or "or", it's doing too much

#### Function Size
- Keep functions small (ideally 5-20 lines)
- Functions should be readable at a single level of abstraction
- Extract complex logic into well-named helper functions

#### Function Arguments
- Prefer 0-3 arguments maximum
- Use meaningful parameter names
- Consider using data structures for multiple related parameters

#### No Side Effects
- Functions should not have hidden side effects
- If a function modifies state, make it clear in the name
- Prefer pure functions when possible

### Self-Explanatory Code Over Comments

#### Write Code That Explains Itself
**Principle**: Good code is self-documenting. Comments should explain "why", not "what" or "how".

#### Prefer Expressive Code Over Comments
```
// Bad - Comments explaining obvious code
function calc(x, y) {
    // Add x and y together
    result = x + y
    // Return the result
    return result
}

// Good - Self-explanatory code
function calculateTotalPrice(basePrice, taxAmount) {
    return basePrice + taxAmount
}
```

#### Extract Methods to Eliminate Comments
```
// Bad - Comments breaking up complex logic
function processOrder(order) {
    // Validate customer information
    if (!order.customerEmail || !order.customerEmail.includes('@')) {
        throw new Error("Invalid email")
    }

    // Calculate total with tax
    subtotal = sum(order.items.map(item => item.price * item.quantity))
    tax = subtotal * 0.08
    total = subtotal + tax

    // Send confirmation email
    sendEmail(order.customerEmail, `Order total: $${total}`)
}

// Good - Extract methods with descriptive names
function processOrder(order) {
    validateCustomerInformation(order)
    total = calculateOrderTotal(order)
    sendOrderConfirmation(order.customerEmail, total)
}

function validateCustomerInformation(order) {
    if (!order.customerEmail || !order.customerEmail.includes('@')) {
        throw new Error("Invalid email")
    }
}

function calculateOrderTotal(order) {
    subtotal = sum(order.items.map(item => item.price * item.quantity))
    tax = subtotal * TAX_RATE
    return subtotal + tax
}

function sendOrderConfirmation(email, total) {
    sendEmail(email, `Order total: $${total}`)
}
```

#### Use Meaningful Variable Names
```
// Bad - Requires comments to understand
function calculateMonthlyPayment(p, r, n) {
    // p = principal amount
    // r = monthly interest rate
    // n = number of payments
    monthlyRate = r / 12
    return p * (monthlyRate * Math.pow(1 + monthlyRate, n)) / (Math.pow(1 + monthlyRate, n) - 1)
}

// Good - Self-explanatory variable names
function calculateMonthlyPayment(principalAmount, annualInterestRate, totalPayments) {
    monthlyInterestRate = annualInterestRate / 12
    rateFactor = Math.pow(1 + monthlyInterestRate, totalPayments)
    return principalAmount * (monthlyInterestRate * rateFactor) / (rateFactor - 1)
}
```

#### When Comments Are Appropriate
Comments should explain **WHY**, not **WHAT**:

```
// Good - Explains business reasoning
function applyDiscount(price, customerType) {
    // Premium customers get 15% discount due to loyalty program agreement
    if (customerType === "premium") {
        return price * 0.85
    }

    // Students get 10% discount as per company social responsibility policy
    if (customerType === "student") {
        return price * 0.90
    }

    return price
}

// Good - Explains complex algorithms or non-obvious solutions
function calculateLeapYear(year) {
    // Gregorian calendar rules: divisible by 4, except century years
    // must be divisible by 400 (not just 100)
    return year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0)
}

// Good - Explains workarounds or temporary solutions
function processLegacyData(data) {
    // TODO: Remove this workaround once legacy system is upgraded (ticket #1234)
    // Legacy system sends malformed JSON with trailing commas
    cleanedData = data.replace(/,\s*}/, '}')
    return JSON.parse(cleanedData)
}
```

#### Comment Anti-Patterns to Avoid
```
// Bad - Obvious comments
age = age + 1  // Increment age by 1

// Bad - Commented-out code (use version control instead)
function calculateTotal(items) {
    total = sum(items.map(item => item.price))
    // total = total * 1.08  // Old tax calculation
    return total
}

// Bad - Misleading or outdated comments
function calculateDiscount(price) {
    // Apply 10% discount for all customers
    return price * 0.85  // Actually 15% discount!
}

// Bad - Comments that repeat the code
// Create a new list
items = []
// Loop through each product
for (product in products) {
    // Add product to list
    items.push(product)
}
```

#### Code Documentation Hierarchy (Preferred Order)
1. **Self-explanatory code** - Descriptive names, clear structure
2. **Type annotations** - Document interfaces and expected data types
3. **API documentation** - Document public APIs and complex functions
4. **Strategic comments** - Explain business logic, algorithms, workarounds
5. **External documentation** - Architecture, setup, deployment guides

### Error Handling

#### Use Specific Exceptions
```
// Bad
throw new Error("Something went wrong")

// Good
throw new TypeError("Both arguments must be numbers")
throw new Error("Cannot divide by zero")
```

#### Fail Fast Principle
- Validate inputs at the beginning of functions
- Don't let invalid data propagate through the system

### Functional Programming Principles

#### Prefer Pure Functions
- Functions should not modify external state
- Same inputs should always produce same outputs
- No side effects (file I/O, network calls, etc.)

#### Immutable Data Structures
- Prefer immutable objects over mutable ones
- Return new objects instead of modifying existing ones
- Use defensive copying when necessary

#### Function Composition
- Break complex operations into smaller, composable functions
- Each function should have a single, clear purpose
- Combine functions to build more complex behavior

#### Higher-Order Functions
- Use functions that operate on other functions
- Enable code reuse and abstraction
- Examples: map, filter, reduce operations

### Refactoring Guidelines

#### When to Refactor
- When you notice code duplication
- When functions become too long or complex
- When adding new features to existing code
- When code becomes difficult to understand

#### Refactoring Safety Rules
1. **Make small, incremental changes**
2. **Keep behavior unchanged**
3. **One refactoring technique at a time**

#### Common Refactoring Patterns
- **Extract Method** - Pull complex logic into named functions
- **Extract Variable** - Name intermediate calculations
- **Remove Duplication** - DRY (Don't Repeat Yourself)
- **Simplify Conditionals** - Use guard clauses and early returns

## Code Organization

### Module/Package Structure
- Group related functionality together
- Separate concerns into different modules
- Use clear, descriptive module names
- Minimize dependencies between modules

### Import/Include Organization
- Group imports by type (standard library, third-party, local)
- Sort imports alphabetically within groups
- Remove unused imports
- Use explicit imports rather than wildcards

### Class/Type Design
- Single Responsibility Principle
- Open/Closed Principle (open for extension, closed for modification)
- Dependency Inversion (depend on abstractions, not concretions)

## Anti-Patterns to Avoid

### Code Anti-Patterns
- **God classes** - Classes that do too much
- **Long parameter lists** - Functions with too many arguments
- **Magic numbers** - Unexplained numeric constants
- **Deep nesting** - Too many nested if/for statements
- **Comments that lie** - Comments that don't match the code
- **Copy-paste programming** - Duplicating code instead of creating reusable functions

### Design Anti-Patterns
- **Tight coupling** - Components that are too dependent on each other
- **Global state** - Shared mutable state accessible from anywhere
- **Premature optimization** - Optimizing before measuring performance
- **Over-engineering** - Adding complexity that isn't needed

## Development Workflow

### Before Writing Code
1. Understand the requirement completely
2. Think about the design and architecture
3. Consider edge cases and error conditions
4. Start with the simplest solution

### During Development
1. Write clear, readable code first
2. Refactor to improve design
3. Write meaningful commit messages
4. Keep changes small and focused

### Code Review Checklist
- [ ] Function and variable names are descriptive
- [ ] Functions are small and focused
- [ ] No code duplication
- [ ] Error cases are handled appropriately
- [ ] Code is self-explanatory with minimal comments
- [ ] No magic numbers or hardcoded values

### Git Commit Strategy
- Make small, atomic commits
- Use clear, descriptive commit messages
- Commit early and often
- Use conventional commit format when appropriate

## Continuous Improvement

### Regular Reviews
- Weekly code review sessions
- Retrospectives on coding practices
- Identify and eliminate technical debt
- Share learnings and best practices

### Metrics to Track
- Code complexity metrics
- Code coverage
- Technical debt ratio
- Code review feedback patterns

---

**Remember**: The goal is not just working code, but clean, maintainable, well-structured code that can evolve over time. These principles are investments in the future of the codebase.
