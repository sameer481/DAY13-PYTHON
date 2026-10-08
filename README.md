# Day 13: Master Python Lambda Functions & Functional Programming 🐍

Welcome to **Day 13** of the Python Mastery Series! This repository contains comprehensive guides, production-grade runnable Python scripts, CPython bytecode disassembly comparisons, memory footprint benchmarks, closure mechanics, and **4 practical real-world mini-applications** covering **Lambda Functions (Anonymous Functions)**, **Functional Programming Built-ins (`map`, `filter`, `reduce`)**, **Custom Key Sorting**, **Higher-Order Functions**, **Late-Binding Traps**, and **PEP 8 Best Practices**.

---

## 📁 Repository Structure

```text
DAY13-PYTHON/
│
├── 01_lambda_syntax_and_foundations.py                 # Def vs Lambda, parameter variations, IIFE pattern, bytecode disassembly, typing.Callable
├── 02_functional_programming_builtins.py               # map(), filter(), functools.reduce(), lazy evaluation vs eager comprehensions, benchmarks
├── 03_sorting_custom_keys_and_higher_order_functions.py # Custom sorting keys, multi-attribute sorting, dataclass/dict sorting, lambda factories
├── 04_advanced_lambda_patterns_closures_and_gotchas.py # Late-binding closure traps, conditional logic, dispatch tables, PEP 8 E731, tracebacks
├── 05_practical_projects.py                           # 4 Production Projects: ETL Log Pipeline, Rule Validator, Table Sorter, Event Dispatcher
└── README.md                                          # Comprehensive masterclass documentation and execution guide
```

---

## 📚 Masterclass Breakdown

### 1. Syntax & Foundations (`01_lambda_syntax_and_foundations.py`)

- **What is a Lambda Function?**:
  An **anonymous, single-expression inline function** created using the `lambda` keyword. Unlike standard functions defined with `def`, lambdas do not require an explicit function name or a `return` statement; the result of evaluating the expression is returned implicitly.

- **Syntax Definition**:
  ```python
  lambda arguments: expression
  ```

- **Parameter Signature Variations**:
  - *No Arguments*: `lambda: 3.14159`
  - *Single Argument*: `lambda x: x * 2`
  - *Multiple Arguments*: `lambda x, y, z: x + y + z`
  - *Default Arguments*: `lambda x, y=10: x + y`
  - *Variable Positional (`*args`)*: `lambda *args: sum(args)`
  - *Variable Keyword (`**kwargs`)*: `lambda **kwargs: kwargs.get('key')`
  - *Keyword-only Arguments*: `lambda x, *, rate=0.18: x * rate`

- **Immediately Invoked Function Expressions (IIFE)**:
  Lambdas can be invoked directly at their declaration point:
  ```python
  result = (lambda a, b: a**2 + b**2)(3, 4)  # Evaluates to 25
  ```

- **CPython Bytecode Disassembly (`dis` module)**:
  Standard `def` functions and `lambda` expressions generate **identical opcode instructions**. Both create Python code objects; the primary difference is metadata (`__name__` evaluates to `'<lambda>'` vs the function identifier).

---

### 2. Functional Built-ins: `map`, `filter`, & `reduce` (`02_functional_programming_builtins.py`)

- **`map(function, *iterables)`**:
  Applies a function to each item of an iterable (or parallel iterables) and returns an iterator yielding transformed elements lazily.

- **`filter(function_or_none, iterable)`**:
  Constructs an iterator from elements of an iterable for which the predicate function returns `True`.

- **`functools.reduce(function, sequence[, initial])`**:
  Applies a function of two arguments cumulatively to the sequence items, reducing the sequence to a single aggregated value.

| Built-in Function | Return Type | Primary Purpose | Memory Behavior |
| :--- | :--- | :--- | :--- |
| **`map()`** | `map` iterator | Data Transformation ($x \rightarrow y$) | Lazy / Streamed |
| **`filter()`** | `filter` iterator | Sequence Selection ($x \rightarrow \text{bool}$) | Lazy / Streamed |
| **`reduce()`** | Single Object | Sequence Aggregation ($[x_1, x_2, \dots] \rightarrow Y$) | Eager reduction |

- **Lazy Evaluation vs. List Comprehension Benchmark**:
  Processing 500,000 items:
  - **List Comprehension**: ~1.96 MB RAM footprint (eager list allocation in memory).
  - **`map()` + `filter()` Iterator**: ~48 Bytes RAM footprint (**>40,000x memory savings**).
  - *Performance Tip*: Use list comprehensions for speed when loading small lists into memory; use `map`/`filter` iterators for memory efficiency on huge data streams.

---

### 3. Custom Sorting & Higher-Order Functions (`03_sorting_custom_keys_and_higher_order_functions.py`)

- **Custom Sorting Keys (`key=lambda`)**:
  Python's `sorted()` and `.sort()` accept a `key` function parameter to extract a comparison key from each element before sorting.

- **Multi-Attribute Compound Sorting**:
  Sorting by multiple criteria using tuple keys. Numeric fields can be inverted (`-val`) for reverse ordering within specific fields:
  ```python
  # Sort by Score (Descending), then Age (Ascending), then Name (Ascending)
  sorted_students = sorted(students, key=lambda s: (-s.score, s.age, s.name))
  ```

- **Lambda Function Factories (Higher-Order Functions)**:
  Functions that generate and return customized lambdas dynamically:
  ```python
  def make_multiplier(factor: float):
      return lambda x: x * factor

  double = make_multiplier(2)
  triple = make_multiplier(3)
  ```

---

### 4. Advanced Patterns, Closure Traps & Gotchas (`04_advanced_lambda_patterns_closures_and_gotchas.py`)

- **The Classic Late-Binding Closure Trap**:
  When lambdas are created inside a loop, they bind loop variables by reference rather than value. Calling them after the loop yields the final loop index value for all functions:

  ```python
  # TRAP: All lambdas return 4!
  funcs = [lambda: i for i in range(5)]

  # FIX 1: Default argument evaluation at definition time
  funcs = [lambda val=i: val for i in range(5)]

  # FIX 2: Outer closure factory function
  def make_getter(val):
      return lambda: val
  funcs = [make_getter(i) for i in range(5)]
  ```

- **Lambda Dispatch Tables (Strategy Pattern)**:
  Replacing nested `if/elif/else` blocks with a dictionary lookup mapping string command keys to lambda handlers:
  ```python
  dispatch = {
      "add": lambda a, b: a + b,
      "sub": lambda a, b: a - b,
      "mul": lambda a, b: a * b,
  }
  ```

- **PEP 8 Guidelines & Anti-Patterns (E731)**:
  - **Do NOT assign lambdas to named identifiers**: Avoid `f = lambda x: x * 2`. Use `def f(x): return x * 2`.
  - **Stack Trace Debugging**: Exceptions inside lambdas report line numbers as `<lambda>`, making log inspection harder compared to explicit function names.

---

## 🚀 Practical Mini-Projects (`05_practical_projects.py`)

1. **ETL Streaming Log Data Pipeline**:
   Parses raw server logs, filters critical warnings/errors, anonymizes client IP addresses, and computes aggregated latency metrics using `map()`, `filter()`, and `reduce()`.

2. **Dynamic Payload Validation Rule Engine**:
   Configurable schema validator verifying incoming JSON dictionaries against a rule dictionary of predicate lambdas.

3. **Multi-Column E-Commerce Inventory Sorter**:
   Compound table sorter handling custom field direction toggles (ascending/descending mix) across strings, floats, and integers.

4. **Event Listener & Functional Middleware Dispatcher**:
   Event emitter architecture supporting lambda listeners and a reduce-based middleware chain for payload transformations and audit logging.

---

## 💻 How to Run the Scripts

Execute any script directly from the project directory using Python 3.x:

```bash
# Run Foundations & Syntax
python 01_lambda_syntax_and_foundations.py

# Run Functional Built-ins & Benchmarks
python 02_functional_programming_builtins.py

# Run Custom Sorting & Lambda Factories
python 03_sorting_custom_keys_and_higher_order_functions.py

# Run Closure Traps & PEP 8 Gotchas
python 04_advanced_lambda_patterns_closures_and_gotchas.py

# Run Real-World Practical Mini-Projects
python 05_practical_projects.py
```

---

## 🌟 Key Takeaways

1. **Use Lambdas for Short, Disposable Inlines**: Lambdas excel as short callbacks in `map()`, `filter()`, `sorted()`, and event handlers.
2. **Prefer Standard Functions for Complex Logic**: If a function requires multiple statements, variable assignments, docstrings, or side effects, use `def`.
3. **Beware of Late-Binding**: Always capture loop variables with default argument values (`lambda x=i: ...`) inside loops.
4. **Leverage Lazy Iterators**: `map` and `filter` yield elements on demand, preserving memory when handling large streams.
