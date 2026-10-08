"""
Day 13 - Python Lambda Functions Masterclass
File 4: Advanced Lambda Patterns, Closure Traps, & PEP 8 Gotchas

This script covers:
1. The classic late-binding closure trap in loop-generated lambdas & its fixes.
2. Ternary and nested conditional expressions inside lambdas.
3. Replacing if/elif chains with Lambda Dispatch Tables (Strategy Pattern).
4. Inline multi-expression tricks (tuples/lists) vs. Clean Code rules.
5. PEP 8 rules, debugging stack traces, and when NOT to use lambda.
"""

import traceback
from typing import Callable, Dict, List


def print_section(title: str) -> None:
    print(f"\n{'=' * 70}\n  {title}\n{'=' * 70}")


# ==============================================================================
# 1. The Classic Late-Binding Closure Trap & Its Solution
# ==============================================================================
def section_1_late_binding_gotcha() -> None:
    print_section("1. Late-Binding Closure Trap in Loop Lambdas")

    # TRAP: Late binding causes all functions to reference the final loop variable value
    trap_funcs: List[Callable[[], int]] = []
    for i in range(5):
        trap_funcs.append(lambda: i)  # Binds variable `i` by reference, not value!

    print("The Late-Binding Trap:")
    results_trap = [f() for f in trap_funcs]
    print(f"  Expected: [0, 1, 2, 3, 4]")
    print(f"  Actual  : {results_trap}  <-- ALL return 4 because 'i' ended at 4!\n")

    # FIX 1: Default Parameter Value Binding (Evaluated at function definition time)
    fixed_funcs_1: List[Callable[[], int]] = []
    for i in range(5):
        fixed_funcs_1.append(lambda val=i: val)

    print("Fix 1 (Default Parameter Binding 'lambda val=i: val'):")
    results_fix_1 = [f() for f in fixed_funcs_1]
    print(f"  Actual  : {results_fix_1}  <-- CORRECT!\n")

    # FIX 2: Outer Closure Factory Function
    def make_getter(bound_val: int) -> Callable[[], int]:
        return lambda: bound_val

    fixed_funcs_2 = [make_getter(i) for i in range(5)]

    print("Fix 2 (Outer Closure Factory 'make_getter(i)'):")
    results_fix_2 = [f() for f in fixed_funcs_2]
    print(f"  Actual  : {results_fix_2}  <-- CORRECT!")


# ==============================================================================
# 2. Conditional Expressions inside Lambdas
# ==============================================================================
def section_2_conditional_expressions() -> None:
    print_section("2. Ternary & Nested Conditional Logic in Lambdas")

    # Single ternary condition
    classify_number: Callable[[int], str] = lambda x: "Zero" if x == 0 else ("Positive" if x > 0 else "Negative")

    print(f"classify_number(15)  = {classify_number(15)!r}")
    print(f"classify_number(-8)  = {classify_number(-8)!r}")
    print(f"classify_number(0)   = {classify_number(0)!r}")

    # Nested ternary grade evaluator
    grade_evaluator: Callable[[float], str] = lambda score: (
        "A+" if score >= 95 else (
            "A" if score >= 85 else (
                "B" if score >= 75 else (
                    "C" if score >= 60 else "F"
                )
            )
        )
    )

    print(f"\nGrade for 98% : {grade_evaluator(98)}")
    print(f"Grade for 87% : {grade_evaluator(87)}")
    print(f"Grade for 72% : {grade_evaluator(72)}")
    print(f"Grade for 54% : {grade_evaluator(54)}")


# ==============================================================================
# 3. Lambda Dispatch Tables (Replacing standard switch/if-elif)
# ==============================================================================
def section_3_dispatch_tables() -> None:
    print_section("3. Lambda Dispatch Tables (Strategy Pattern)")

    # Dispatch dictionary mapping arithmetic operation names to lambda implementations
    calculator_dispatch: Dict[str, Callable[[float, float], float]] = {
        "add": lambda a, b: a + b,
        "subtract": lambda a, b: a - b,
        "multiply": lambda a, b: a * b,
        "divide": lambda a, b: a / b if b != 0 else float("nan"),
        "power": lambda a, b: a ** b,
    }

    def execute_operation(op: str, x: float, y: float) -> float:
        # Fetch operation lambda with fallback default to zero function
        func = calculator_dispatch.get(op, lambda a, b: 0.0)
        return func(x, y)

    x_val, y_val = 10.0, 4.0
    print(f"Inputs: x = {x_val}, y = {y_val}")
    for op in ["add", "subtract", "multiply", "divide", "power", "unknown_op"]:
        res = execute_operation(op, x_val, y_val)
        print(f"  Operation {op:<12s} => Result: {res}")


# ==============================================================================
# 4. Multi-Expression Workarounds vs Clean Code
# ==============================================================================
def section_4_multi_expression_tricks() -> None:
    print_section("4. Multi-Expression Workarounds vs Clean Code")

    # Trick: Using tuples or lists to perform logging/side-effects before returning a value
    logging_multiplier = lambda x: (print(f"  [LOG] Processing item input = {x}"), x * 10)[1]

    print("Executing tuple side-effect trick:")
    result = logging_multiplier(5)
    print(f"  Final return value: {result}")

    print("\nWARNING / Clean Code Advisory:")
    print("  While tuple indexing enables multiple expressions, PEP 8 strongly discourages it.")
    print("  If a function requires side effects, state mutations, or multiple statements, use a standard 'def' function!")


# ==============================================================================
# 5. PEP 8 Anti-Patterns & Stack Trace Debugging
# ==============================================================================
def section_5_pep8_and_debugging() -> None:
    print_section("5. PEP 8 Anti-Patterns & Traceback Differences")

    print("PEP 8 Recommendation E731:")
    print("  DO NOT assign a lambda expression directly to an identifier like:")
    print("    f = lambda x: 2*x   # BAD (PEP 8 Anti-pattern)")
    print("  DO use a standard function definition instead:")
    print("    def f(x): return 2*x  # GOOD")

    print("\nComparing Stack Trace Tracebacks during exceptions:")

    def named_function_crash(x: int) -> float:
        return 100 / x

    lambda_crash = lambda x: 100 / x

    # 1. Exception in named function
    print("\n--- Exception Traceback for NAMED Function ---")
    try:
        named_function_crash(0)
    except ZeroDivisionError:
        traceback.print_exc(limit=1)

    # 2. Exception in lambda function
    print("\n--- Exception Traceback for LAMBDA Function ---")
    try:
        lambda_crash(0)
    except ZeroDivisionError:
        traceback.print_exc(limit=1)

    print("\nNotice how the named function traceback clearly shows function name 'named_function_crash',")
    print("whereas the lambda shows '<lambda>', making production log debugging much harder for complex pipelines!")


if __name__ == "__main__":
    section_1_late_binding_gotcha()
    section_2_conditional_expressions()
    section_3_dispatch_tables()
    section_4_multi_expression_tricks()
    section_5_pep8_and_debugging()
