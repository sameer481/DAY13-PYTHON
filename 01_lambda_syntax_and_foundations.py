"""
Day 13 - Python Lambda Functions Masterclass
File 1: Lambda Syntax, Foundations & Signature Variations

This script covers:
1. Concept of Anonymous (Lambda) Functions vs standard `def` functions.
2. Syntax: `lambda arguments: expression` and implicit returns.
3. Parameter variations: No args, single, multiple, default values, *args, **kwargs, keyword-only args.
4. Immediately Invoked Function Expressions (IIFE) in Python.
5. Inspection & Bytecode disassembly (`dis` module) comparing `def` vs `lambda`.
6. Type hinting lambdas using `typing.Callable`.
"""

import dis
from typing import Callable


def print_section(title: str) -> None:
    print(f"\n{'=' * 70}\n  {title}\n{'=' * 70}")


# ==============================================================================
# 1. Def vs Lambda: Basic Concept & Syntax Comparison
# ==============================================================================
def section_1_def_vs_lambda() -> None:
    print_section("1. Standard Function (def) vs Lambda Function")

    # Standard function definition
    def square_def(x: int) -> int:
        """Returns the square of x."""
        return x * x

    # Equivalent Lambda function (Anonymous function bound to a variable)
    square_lambda = lambda x: x * x

    val = 5
    print(f"Square using def function   : square_def({val})    = {square_def(val)}")
    print(f"Square using lambda function: square_lambda({val}) = {square_lambda(val)}")

    # Inspecting function names and attributes
    print(f"\nFunction metadata comparison:")
    print(f"  square_def.__name__    : {square_def.__name__!r}")
    print(f"  square_lambda.__name__ : {square_lambda.__name__!r}")
    print(f"  square_def.__doc__     : {square_def.__doc__!r}")
    print(f"  square_lambda.__doc__  : {square_lambda.__doc__!r}")


# ==============================================================================
# 2. Parameter Signature Variations in Lambdas
# ==============================================================================
def section_2_parameter_variations() -> None:
    print_section("2. Parameter Signature Variations in Lambdas")

    # No arguments
    get_pi: Callable[[], float] = lambda: 3.1415926535
    print(f"[No Args]           get_pi()                  = {get_pi()}")

    # Single argument
    double: Callable[[int], int] = lambda x: x * 2
    print(f"[Single Arg]        double(7)                 = {double(7)}")

    # Multiple arguments
    multiply: Callable[[int, int], int] = lambda x, y: x * y
    print(f"[Multiple Args]     multiply(6, 7)            = {multiply(6, 7)}")

    # Default argument values
    greet: Callable[[str, str], str] = lambda name, greeting="Hello": f"{greeting}, {name}!"
    print(f"[Default Args]      greet('Alice')            = {greet('Alice')!r}")
    print(f"[Default Args Override] greet('Bob', 'Welcome') = {greet('Bob', 'Welcome')!r}")

    # Variable positional arguments (*args)
    sum_all: Callable[..., int] = lambda *args: sum(args)
    print(f"[Var Positional]    sum_all(1, 2, 3, 4, 5)    = {sum_all(1, 2, 3, 4, 5)}")

    # Variable keyword arguments (**kwargs)
    build_dict: Callable[..., dict] = lambda **kwargs: {k.upper(): v for k, v in kwargs.items()}
    print(f"[Var Keywords]      build_dict(name='Sam', role='Dev') = {build_dict(name='Sam', role='Dev')}")

    # Keyword-only arguments (using * separator)
    calculate_tax: Callable[..., float] = lambda amount, *, rate=0.18: amount * rate
    print(f"[Keyword-only]      calculate_tax(1000, rate=0.20)     = {calculate_tax(1000, rate=0.20)}")


# ==============================================================================
# 3. Immediately Invoked Function Expressions (IIFE)
# ==============================================================================
def section_3_iife_pattern() -> None:
    print_section("3. Immediately Invoked Function Expressions (IIFE)")

    # Invoking a lambda immediately upon definition without assigning it to a variable name
    result_1 = (lambda x, y: x**2 + y**2)(3, 4)
    print(f"IIFE (3^2 + 4^2)                           = {result_1}")

    result_2 = (lambda text: f"*** {text.strip().upper()} ***")("  python lambda mastery  ")
    print(f"IIFE String Formatting                      = {result_2!r}")

    # Using IIFE for inline scope isolation / computation
    config = (lambda env: {"host": "localhost" if env == "dev" else "api.prod.com", "port": 8080 if env == "dev" else 443})("prod")
    print(f"IIFE Dynamic Config Generation              = {config}")


# ==============================================================================
# 4. Bytecode & Internal Inspection: def vs lambda
# ==============================================================================
def section_4_bytecode_inspection() -> None:
    print_section("4. CPython Bytecode Disassembly: def vs lambda")

    def def_add(a: int, b: int) -> int:
        return a + b

    lambda_add = lambda a, b: a + b

    print("Bytecode for 'def def_add(a, b)':")
    dis.dis(def_add)

    print("\nBytecode for 'lambda_add = lambda a, b: a + b':")
    dis.dis(lambda_add)

    print("\nObservation: Standard functions and Lambdas generate virtually IDENTICAL bytecode instructions!")
    print("Both create code objects with code flags, local variable counts, and stack operations.")
    print("The only difference lies in metadata (__name__ = '<lambda>' vs function name).")


# ==============================================================================
# 5. Type Hinting with typing.Callable
# ==============================================================================
def section_5_type_hinting() -> None:
    print_section("5. Type Hinting Lambdas with typing.Callable")

    # Defining typed aliases for function signatures
    TransformFunc = Callable[[float], float]

    celsius_to_fahrenheit: TransformFunc = lambda c: (c * 9 / 5) + 32
    fahrenheit_to_celsius: TransformFunc = lambda f: (f - 32) * 5 / 9

    def convert_temperature(temp: float, transformer: TransformFunc) -> float:
        return round(transformer(temp), 2)

    c_val = 25.0
    f_val = 77.0
    print(f"{c_val} deg C to Fahrenheit : {convert_temperature(c_val, celsius_to_fahrenheit)} deg F")
    print(f"{f_val} deg F to Celsius    : {convert_temperature(f_val, fahrenheit_to_celsius)} deg C")


if __name__ == "__main__":
    section_1_def_vs_lambda()
    section_2_parameter_variations()
    section_3_iife_pattern()
    section_4_bytecode_inspection()
    section_5_type_hinting()
