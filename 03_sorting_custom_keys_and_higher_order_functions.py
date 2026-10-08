"""
Day 13 - Python Lambda Functions Masterclass
File 3: Custom Sorting Keys, Higher-Order Functions & Lambda Factories

This script covers:
1. Custom sorting with sorted() / .sort() and key=lambda.
2. Multi-attribute compound sorting (ascending/descending mix).
3. Sorting dictionaries (by keys, values, nested fields) and Dataclass instances.
4. Using lambdas with min(), max(), and itertools.groupby().
5. Higher-Order Functions (HOF) & Dynamic Lambda Function Factories.
"""

from dataclasses import dataclass
from itertools import groupby
from typing import Callable, Dict, List, Tuple


def print_section(title: str) -> None:
    print(f"\n{'=' * 70}\n  {title}\n{'=' * 70}")


# ==============================================================================
# 1. Custom Sorting Keys with sorted() & .sort()
# ==============================================================================
def section_1_custom_sorting() -> None:
    print_section("1. Custom Sorting Keys using sorted(key=lambda)")

    # 1. Sorting strings by length vs alphabetical
    words = ["banana", "fig", "watermelon", "apple", "date"]
    by_length = sorted(words, key=lambda word: len(word))
    by_last_char = sorted(words, key=lambda word: word[-1])

    print(f"Original words      : {words}")
    print(f"Sorted by length    : {by_length}")
    print(f"Sorted by last char : {by_last_char}")

    # 2. Case-insensitive sorting
    mixed_strings = ["zebra", "Apple", "banana", "Cherry", "date"]
    default_sorted = sorted(mixed_strings)
    case_insensitive = sorted(mixed_strings, key=lambda s: s.lower())

    print(f"\nMixed Strings        : {mixed_strings}")
    print(f"Default ASCII sort  : {default_sorted}")
    print(f"Case-insensitive    : {case_insensitive}")

    # 3. Absolute value sorting for numbers
    nums = [-25, 10, -5, 30, -50, 15]
    by_abs = sorted(nums, key=lambda x: abs(x))
    print(f"\nNumbers by absolute value: {by_abs}")


# ==============================================================================
# 2. Multi-Attribute Compound Sorting
# ==============================================================================
def section_2_multi_attribute_sorting() -> None:
    print_section("2. Multi-Attribute Compound Sorting with Tuple Keys")

    # List of tuples: (Name, Age, Score)
    students = [
        ("Alice", 22, 88),
        ("Bob", 20, 95),
        ("Charlie", 22, 95),
        ("Diana", 20, 88),
        ("Eve", 21, 92),
    ]

    # Sort Priority: Primary = Score (Descending), Secondary = Age (Ascending), Tertiary = Name (Ascending)
    # Note trick for numeric descending: negate the number (-score) inside the tuple!
    sorted_students = sorted(
        students,
        key=lambda s: (-s[2], s[1], s[0])
    )

    print("Student dataset (Name, Age, Score):")
    for s in students:
        print(f"  {s}")

    print("\nSorted by Score (Desc), Age (Asc), Name (Asc):")
    for s in sorted_students:
        print(f"  Score: {s[2]} | Age: {s[1]} | Name: {s[0]}")


# ==============================================================================
# 3. Sorting Dictionaries & Dataclass Objects
# ==============================================================================
@dataclass
class Product:
    id: str
    name: str
    price: float
    rating: float


def section_3_dict_and_dataclass_sorting() -> None:
    print_section("3. Sorting Dictionaries and Dataclasses")

    # 1. Sorting Dictionary by Values
    scores: Dict[str, int] = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 95, "Eve": 88}
    sorted_by_val = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

    print("Dictionary sorted by value (highest to lowest score):")
    for name, score in sorted_by_val.items():
        print(f"  {name:8s}: {score}")

    # 2. Sorting Dataclass Instances
    inventory: List[Product] = [
        Product("P101", "Laptop", 1200.0, 4.7),
        Product("P102", "Mouse", 25.0, 4.2),
        Product("P103", "Monitor", 350.0, 4.8),
        Product("P104", "Keyboard", 75.0, 4.5),
        Product("P105", "Headphones", 150.0, 4.7),
    ]

    # Sort by Rating (Desc), then Price (Asc)
    sorted_inventory = sorted(inventory, key=lambda p: (-p.rating, p.price))

    print("\nInventory sorted by Rating (Desc) then Price (Asc):")
    for p in sorted_inventory:
        print(f"  [{p.id}] {p.name:<12s} | Rating: {p.rating} | Price: ${p.price:.2f}")


# ==============================================================================
# 4. Lambdas with min(), max(), and itertools.groupby()
# ==============================================================================
def section_4_min_max_groupby() -> None:
    print_section("4. Lambdas with min(), max(), and itertools.groupby()")

    cities = [
        {"name": "New York", "pop": 8_400_000, "region": "East"},
        {"name": "Los Angeles", "pop": 3_900_000, "region": "West"},
        {"name": "Chicago", "pop": 2_700_000, "region": "Midwest"},
        {"name": "Houston", "pop": 2_300_000, "region": "South"},
        {"name": "Phoenix", "pop": 1_600_000, "region": "West"},
        {"name": "Philadelphia", "pop": 1_500_000, "region": "East"},
    ]

    # Finding min and max by population key
    most_populous = max(cities, key=lambda c: c["pop"])
    least_populous = min(cities, key=lambda c: c["pop"])

    print(f"Most populous city : {most_populous['name']} ({most_populous['pop']:,})")
    print(f"Least populous city: {least_populous['name']} ({least_populous['pop']:,})")

    # Grouping cities by region using itertools.groupby
    # Note: groupby requires the input list to be sorted by the grouping key first!
    sorted_by_region = sorted(cities, key=lambda c: c["region"])

    print("\nCities grouped by Region using groupby + key=lambda:")
    for region, group in groupby(sorted_by_region, key=lambda c: c["region"]):
        city_names = [c["name"] for c in group]
        print(f"  Region [{region:<7s}]: {', '.join(city_names)}")


# ==============================================================================
# 5. Higher-Order Functions (HOF) & Dynamic Lambda Factories
# ==============================================================================
def section_5_lambda_factories() -> None:
    print_section("5. Higher-Order Functions & Lambda Function Factories")

    # Higher-Order Function returning a specialized lambda function dynamically
    def make_multiplier(factor: float) -> Callable[[float], float]:
        """Returns a lambda function that multiplies its input by `factor`."""
        return lambda x: x * factor

    double = make_multiplier(2)
    triple = make_multiplier(3)
    tenfold = make_multiplier(10)

    val = 7
    print(f"Base Value : {val}")
    print(f"double({val})  : {double(val)}")
    print(f"triple({val})  : {triple(val)}")
    print(f"tenfold({val}) : {tenfold(val)}")

    # Dynamic Rule Generator Factory for String Validation
    def make_length_validator(min_len: int, max_len: int) -> Callable[[str], bool]:
        """Returns a validator lambda checking if string length is within bounds."""
        return lambda text: min_len <= len(text.strip()) <= max_len

    username_validator = make_length_validator(3, 15)
    tweet_validator = make_length_validator(1, 280)

    test_user = "sam_dev"
    print(f"\nUsername {test_user!r} valid (3-15 chars)? {username_validator(test_user)}")
    print(f"Empty string valid (3-15 chars)? {username_validator('')}")


if __name__ == "__main__":
    section_1_custom_sorting()
    section_2_multi_attribute_sorting()
    section_3_dict_and_dataclass_sorting()
    section_4_min_max_groupby()
    section_5_lambda_factories()
