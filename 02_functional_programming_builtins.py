"""
Day 13 - Python Lambda Functions Masterclass
File 2: Functional Programming Built-ins: map, filter, & reduce

This script covers:
1. Transforming elements with map() and lambdas (single & multi-iterable).
2. Filtering sequences with filter() and predicate lambdas.
3. Aggregating data with functools.reduce() and accumulation lambdas.
4. Lazy evaluation vs. List comprehensions (Memory & Performance comparison).
5. Building a multi-stage functional data processing pipeline.
"""

from functools import reduce
import sys
import timeit
from typing import Iterator, List, Tuple


def print_section(title: str) -> None:
    print(f"\n{'=' * 70}\n  {title}\n{'=' * 70}")


# ==============================================================================
# 1. Transforming Data with map() & Lambdas
# ==============================================================================
def section_1_map_transformations() -> None:
    print_section("1. Data Transformation with map() and Lambdas")

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Single-iterable mapping
    squared_map: Iterator[int] = map(lambda x: x**2, numbers)
    print(f"Original numbers        : {numbers}")
    print(f"map() iterator object   : {squared_map}")
    print(f"Evaluated list from map : {list(squared_map)}")

    # Multi-iterable mapping (parallel zip-like operation)
    list_a = [10, 20, 30, 40]
    list_b = [2, 4, 5, 8]
    list_c = [1, 1, 2, 3]

    combined = list(map(lambda x, y, z: (x * y) + z, list_a, list_b, list_c))
    print(f"\nMulti-iterable map: (a * b) + c")
    print(f"  List A: {list_a}\n  List B: {list_b}\n  List C: {list_c}")
    print(f"  Result: {combined}")

    # String normalization example
    raw_names = ["  alICE ", "  bOB  ", " CHARLIE", "dAVid "]
    clean_names = list(map(lambda name: name.strip().capitalize(), raw_names))
    print(f"\nString Normalization with map:")
    print(f"  Raw names  : {raw_names}")
    print(f"  Clean names: {clean_names}")


# ==============================================================================
# 2. Sequence Filtering with filter() & Predicate Lambdas
# ==============================================================================
def section_2_filter_predicates() -> None:
    print_section("2. Sequence Filtering with filter() and Predicate Lambdas")

    dataset = [12, -5, 0, 45, -18, 9, 30, -2, 100]

    # Filter positive numbers
    positives = list(filter(lambda x: x > 0, dataset))
    print(f"Dataset         : {dataset}")
    print(f"Positive numbers: {positives}")

    # Filter even numbers divisible by 3
    even_div_3 = list(filter(lambda x: x % 2 == 0 and x % 3 == 0, dataset))
    print(f"Even & div by 3 : {even_div_3}")

    # Filtering complex objects (dicts)
    employees = [
        {"name": "Alice", "dept": "Engineering", "salary": 95000},
        {"name": "Bob", "dept": "Sales", "salary": 60000},
        {"name": "Charlie", "dept": "Engineering", "salary": 110000},
        {"name": "Diana", "dept": "HR", "salary": 55000},
    ]

    high_earning_engineers = list(
        filter(lambda emp: emp["dept"] == "Engineering" and emp["salary"] >= 100000, employees)
    )
    print("\nFiltered High-Earning Engineers:")
    for emp in high_earning_engineers:
        print(f"  - {emp['name']} (${emp['salary']:,})")


# ==============================================================================
# 3. Aggregating Sequences with functools.reduce()
# ==============================================================================
def section_3_reduce_aggregations() -> None:
    print_section("3. Sequence Aggregation with functools.reduce()")

    numbers = [1, 2, 3, 4, 5]

    # Product of all elements
    product = reduce(lambda acc, val: acc * val, numbers)
    print(f"Product of {numbers} = {product}")

    # Sum with initial accumulator value
    total_with_bonus = reduce(lambda acc, val: acc + val, numbers, 50)
    print(f"Sum of {numbers} + initial 50 = {total_with_bonus}")

    # Finding maximum element using reduce
    data = [42, 17, 89, 23, 95, 61]
    max_val = reduce(lambda a, b: a if a > b else b, data)
    print(f"Max value of {data} = {max_val}")

    # Flattening nested list using reduce
    nested_lists = [[1, 2], [3, 4, 5], [6], [7, 8, 9]]
    flattened = reduce(lambda acc, curr: acc + curr, nested_lists, [])
    print(f"\nFlattening nested lists:")
    print(f"  Nested   : {nested_lists}")
    print(f"  Flattened: {flattened}")

    # Word count dictionary aggregation
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    word_counts = reduce(
        lambda counts, word: {**counts, word: counts.get(word, 0) + 1},
        words,
        {}
    )
    print(f"\nWord frequency dictionary via reduce:")
    print(f"  Words : {words}")
    print(f"  Counts: {word_counts}")


# ==============================================================================
# 4. Lazy Evaluation vs List Comprehensions (Memory & Speed Benchmark)
# ==============================================================================
def section_4_lazy_vs_eager_benchmark() -> None:
    print_section("4. Lazy Evaluation vs. List Comprehensions: Memory & Speed")

    N = 500_000

    # 1. Memory Usage Comparison
    # Map/Filter iterators are memory-efficient because they yield items on-demand
    eager_list = [x**2 for x in range(N) if x % 2 == 0]
    lazy_map_filter = map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(N)))

    eager_size = sys.getsizeof(eager_list)
    lazy_size = sys.getsizeof(lazy_map_filter)

    print(f"Memory footprint for {N:,} processed elements:")
    print(f"  List Comprehension (Eager) : {eager_size / (1024 * 1024):.4f} MB ({eager_size:,} bytes)")
    print(f"  map() + filter() (Lazy)    : {lazy_size / 1024:.4f} KB ({lazy_size:,} bytes)")
    print(f"  Memory Savings Ratio      : ~{eager_size / lazy_size:,.0f}x smaller footprint for iterator!")

    # 2. Execution Speed Benchmark
    setup_code = "data = list(range(100_000))"

    t_comp = timeit.timeit(
        "[x * 2 for x in data if x % 2 == 0]",
        setup=setup_code,
        number=100
    )

    t_map_filter = timeit.timeit(
        "list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, data)))",
        setup=setup_code,
        number=100
    )

    print(f"\nExecution Speed Benchmark (100 runs over 100,000 items):")
    print(f"  List Comprehension         : {t_comp:.4f} seconds")
    print(f"  list(map(filter(lambda)))  : {t_map_filter:.4f} seconds")
    print(f"  Takeaway: List comprehensions are generally faster in Python due to C-level bytecode optimization,")
    print(f"  whereas map/filter are ideal for lazy evaluation streams and infinite iterators.")


# ==============================================================================
# 5. Multi-Stage Functional Pipeline
# ==============================================================================
def section_5_functional_pipeline() -> None:
    print_section("5. Building a Multi-Stage Functional Data Pipeline")

    transactions = [
        {"id": "T1", "amount": 250.0, "status": "completed", "currency": "USD"},
        {"id": "T2", "amount": -50.0,  "status": "failed",    "currency": "USD"},
        {"id": "T3", "amount": 1200.0, "status": "completed", "currency": "EUR"},
        {"id": "T4", "amount": 450.0,  "status": "completed", "currency": "USD"},
        {"id": "T5", "amount": 80.0,   "status": "pending",   "currency": "USD"},
        {"id": "T6", "amount": 310.0,  "status": "completed", "currency": "USD"},
    ]

    # Pipeline Goal:
    # 1. Filter: Completed transactions in USD currency with amount > $100
    # 2. Map: Apply a 2% processing fee deduction to each valid amount
    # 3. Reduce: Calculate total revenue net balance

    # Step 1: Filter
    valid_txs = filter(
        lambda t: t["status"] == "completed" and t["currency"] == "USD" and t["amount"] > 100,
        transactions
    )

    # Step 2: Map to Net Amount (amount * 0.98)
    net_amounts = map(lambda t: t["amount"] * 0.98, valid_txs)

    # Step 3: Reduce to total balance
    total_net_revenue = reduce(lambda acc, amt: acc + amt, net_amounts, 0.0)

    print("Pipeline Processing Steps:")
    print(f"  Raw Transactions Count  : {len(transactions)}")
    print(f"  Total Net USD Revenue   : ${total_net_revenue:,.2f}")


if __name__ == "__main__":
    section_1_map_transformations()
    section_2_filter_predicates()
    section_3_reduce_aggregations()
    section_4_lazy_vs_eager_benchmark()
    section_5_functional_pipeline()
