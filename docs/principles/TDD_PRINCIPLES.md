# Generic Test-Driven Development Principles

## Test-Driven Development (TDD) Protocol

### The Red-Green-Refactor Cycle

**MANDATORY**: All development must follow the strict TDD cycle:

1. **RED** - Write a failing test first
   - Write the smallest possible test that fails
   - Test should describe the desired behavior
   - Run tests to confirm the new test fails
   - Do not write any production code yet

2. **GREEN** - Make the test pass with minimal code
   - Write only enough production code to make the test pass
   - Use the simplest solution possible (even if ugly)
   - No premature optimization or over-engineering
   - Run tests to confirm all tests pass

3. **REFACTOR** - Improve the code while keeping tests green
   - Clean up production code without changing behavior
   - Remove duplication and improve readability
   - Ensure all tests still pass after each refactor step
   - Apply clean code principles

### TDD Rules (Uncle Bob's Laws)

1. **Do not write production code unless it makes a failing test pass**
2. **Do not write more of a test than is sufficient to fail**
3. **Do not write more production code than is sufficient to pass the failing test**

## Test Quality Standards

### Test Structure
```
def test_feature_description():
    calculator = Calculator()
    first_number = 5
    second_number = 3

    result = calculator.add(first_number, second_number)

    assert result == 8
```

### Test Naming Convention
- Use descriptive names that focus on **behavior**, not implementation
- Format: `test_[behavior_being_tested]_[given_conditions]`
- Examples:
  - `test_returns_sum_when_adding_positive_numbers`
  - `test_raises_exception_when_dividing_by_zero`
  - `test_returns_positive_when_multiplying_negatives`
  - `test_returns_zero_when_multiplying_by_zero`
  - `test_maintains_precision_with_floating_point_arithmetic`

### What NOT to do in test names:
- ❌ `test_add_method` - focuses on method name
- ❌ `test_calculator_divide` - focuses on class/method
- ❌ `test_multiply_function` - focuses on implementation
- ✅ `test_calculates_product_correctly` - focuses on behavior
- ✅ `test_handles_negative_input_appropriately` - focuses on behavior

### Test Categories to Include
1. **Happy Path Tests** - Normal, expected usage
2. **Edge Case Tests** - Boundary conditions, limits
3. **Error Case Tests** - Invalid inputs, exceptions
4. **Integration Tests** - Multiple components working together

### Test Independence
- Each test must be completely independent
- Tests should not depend on execution order
- Use setup methods for test fixtures
- Clean up after tests if needed

### Test Data Management
- Use descriptive test data that reveals intent
- Avoid magic numbers in tests
- Create test data builders for complex objects
- Use parameterized tests for multiple similar scenarios

## TDD Best Practices

### Starting a TDD Session
1. **Understand the requirement completely**
   - Break down complex requirements into smaller behaviors
   - Identify the simplest behavior to implement first
   - Think about edge cases and error conditions

2. **Choose the right granularity**
   - Start with the simplest possible test
   - Don't try to test everything at once
   - Focus on one behavior per test

3. **Write the test first**
   - The test should fail for the right reason
   - The test should compile/parse (if applicable)
   - The test should describe the desired behavior clearly

### During the GREEN Phase
- **Write the simplest code that passes**
  - Don't worry about elegance or efficiency
  - Hardcode values if it makes the test pass
  - Resist the urge to write "extra" functionality

- **Make only the failing test pass**
  - Don't break existing tests
  - Don't implement features not covered by tests
  - Focus solely on the current failing test

### During the REFACTOR Phase
- **Improve code quality without changing behavior**
  - Remove duplication
  - Improve naming
  - Extract methods and classes
  - Apply design patterns where appropriate

- **Refactor both production and test code**
  - Tests are first-class citizens
  - Remove duplication in test code
  - Improve test readability and maintainability

- **Run tests after each refactoring step**
  - Ensure all tests still pass
  - If tests fail, revert and try smaller steps
  - Commit after successful refactoring

## Test Design Principles

### Test Structure Pattern
- Set up test data and initial conditions
- Execute the behavior being tested
- Verify the expected outcome

### One Assertion Per Test (Generally)
- Focus each test on one specific behavior
- Use multiple assertions only when they test the same logical concept
- Split tests if they're verifying different behaviors

### Test Readability
- Tests should read like specifications
- Anyone should be able to understand what's being tested
- Use descriptive variable names in tests
- Keep test logic simple and straightforward

### Test Maintainability
- Avoid complex test logic
- Don't test implementation details
- Focus on public interfaces and behaviors
- Make tests resilient to refactoring

## TDD Workflow Patterns

### Triangulation
When you have one test passing with hardcoded values:
1. Add a second test with different inputs
2. Generalize the implementation to handle both cases
3. Continue adding tests until you have confidence in the implementation

### Obvious Implementation
When the implementation is simple and obvious:
1. Write the test
2. Implement the obvious solution directly
3. Refactor if needed

### Fake It Till You Make It
When the implementation is complex or unclear:
1. Start with hardcoded return values
2. Add more tests to force generalization
3. Gradually make the implementation more generic

## Common TDD Mistakes to Avoid

### Writing Too Much at Once
- Don't write multiple tests before making any pass
- Don't implement more than needed to pass current tests
- Take smaller steps when in doubt

### Testing Implementation Details
- Test behavior, not internal implementation
- Tests should survive refactoring
- Focus on what the code does, not how it does it

### Skipping the Refactor Step
- Always clean up after making tests pass
- Technical debt accumulates quickly without refactoring
- Refactoring is not optional - it's part of the cycle

### Poor Test Organization
- Don't let test code become messy
- Apply the same quality standards to test code
- Organize tests logically and consistently

### Creating Unnecessary Files
- **NEVER create example files** - work only with the actual codebase
- **NEVER create temporary executable files** to test if changes are effective
- **NEVER create test files that are not explicitly requested by the user**
- Rely on text analysis and existing tests to verify changes
- Use the actual test suite to validate functionality
- Keep the workspace clean and focused

## TDD and Design

### Emergent Design
- Let the design emerge from the tests
- Don't over-design upfront
- Allow the tests to drive the API design

### Dependency Management
- Use dependency injection for testability
- Isolate external dependencies
- Use test doubles (mocks, stubs, fakes) appropriately

### Interface Discovery
- Tests help discover what interfaces you need
- Start with the client code (the test)
- Design APIs that are easy to use and test

## Measuring TDD Success

### Test Coverage
- Aim for high test coverage (but not 100% obsession)
- Focus on covering important behaviors
- Use coverage tools to identify untested areas

### Test Quality Metrics
- Number of tests per feature
- Test execution time
- Test failure rate
- Time to fix broken tests

### Design Quality Indicators
- Ease of adding new features
- Frequency of bugs in production
- Time to understand and modify code
- Coupling and cohesion metrics

## TDD in Different Contexts

### Legacy Code
- Start by adding characterization tests
- Identify seams where tests can be inserted
- Refactor to make code more testable
- Use "approval testing" for complex outputs

### Greenfield Projects
- Start with TDD from day one
- Establish testing conventions early
- Build CI/CD pipeline with tests
- Make failing tests break the build

### Team Adoption
- Start with team agreement on TDD practices
- Provide training and mentoring
- Pair programming to spread knowledge
- Regular retrospectives on TDD practices

---

**Remember**: TDD is not just about testing - it's a design technique that helps you write better, cleaner, more maintainable code. The tests are a beneficial side effect of a good design process.
