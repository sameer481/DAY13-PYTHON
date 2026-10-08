"""
Day 13 - Python Lambda Functions Masterclass
File 5: Practical Real-World Mini-Projects Powered by Lambdas

This script includes 4 fully-functional production projects:
1. ETL Streaming Data Pipeline Engine (Log processing via map/filter/reduce)
2. Dynamic Rule & Payload Validation Engine (Configurable lambda rules)
3. Multi-Column E-Commerce Inventory Sorter (Compound sorting engine)
4. Event Listener & Functional Middleware Dispatcher (Event-driven system)
"""

from datetime import datetime
from functools import reduce
import re
from typing import Any, Callable, Dict, List, Tuple


def print_project_header(title: str) -> None:
    print(f"\n{'#' * 75}\n# PROJECT: {title}\n{'#' * 75}")


# ==============================================================================
# PROJECT 1: ETL Streaming Log Data Pipeline Engine
# ==============================================================================
def project_1_etl_pipeline() -> None:
    print_project_header("1. ETL Streaming Log Data Pipeline Engine")

    # Raw server log entries stream
    raw_logs = [
        "2026-10-08 10:15:30 | INFO  | 192.168.1.105 | GET /api/v1/products | 200 OK | 45ms",
        "2026-10-08 10:15:32 | WARN  | 192.168.1.112 | POST /api/v1/login | 401 Unauthorized | 120ms",
        "2026-10-08 10:15:35 | ERROR | 10.0.0.52     | GET /api/v1/checkout | 500 Internal Error | 850ms",
        "2026-10-08 10:15:38 | INFO  | 192.168.1.105 | GET /api/v1/cart | 200 OK | 30ms",
        "2026-10-08 10:15:42 | ERROR | 10.0.0.88     | POST /api/v1/payment | 502 Bad Gateway | 1450ms",
        "2026-10-08 10:15:45 | ERROR | 192.168.1.112 | GET /api/v1/products | 504 Gateway Timeout | 2100ms",
    ]

    # Pipeline Step 1: Parser Lambda (Raw text -> Structured Dictionary)
    parse_log: Callable[[str], Dict[str, Any]] = lambda log: (
        lambda parts: {
            "timestamp": parts[0].strip(),
            "level": parts[1].strip(),
            "ip": parts[2].strip(),
            "endpoint": parts[3].strip(),
            "status": parts[4].strip(),
            "latency_ms": int(parts[5].strip().replace("ms", "")),
        }
    )([p for p in log.split("|")])

    # Step 1 Execution (Map)
    parsed_logs = list(map(parse_log, raw_logs))

    # Pipeline Step 2: Filter Errors & Warnings (Filter)
    error_logs = list(filter(lambda entry: entry["level"] in ("WARN", "ERROR"), parsed_logs))

    # Pipeline Step 3: Anonymize IP Addresses (Map)
    anonymize_ip: Callable[[Dict[str, Any]], Dict[str, Any]] = lambda entry: {
        **entry,
        "ip": re.sub(r"\.\d+$", ".***", entry["ip"])
    }
    anonymized_errors = list(map(anonymize_ip, error_logs))

    # Pipeline Step 4: Aggregate Metrics (Reduce) - Total Latency & Count per level
    metrics = reduce(
        lambda acc, entry: {
            **acc,
            "total_latency": acc["total_latency"] + entry["latency_ms"],
            "count": acc["count"] + 1,
            "level_counts": {
                **acc["level_counts"],
                entry["level"]: acc["level_counts"].get(entry["level"], 0) + 1,
            },
        },
        error_logs,
        {"total_latency": 0, "count": 0, "level_counts": {}}
    )

    avg_latency = metrics["total_latency"] / metrics["count"] if metrics["count"] > 0 else 0

    print("Pipeline Results:")
    print(f"  Total Raw Logs Processed : {len(raw_logs)}")
    print(f"  Critical Issues Filtered : {len(error_logs)}")
    print(f"  Average Error Latency    : {avg_latency:.2f} ms")
    print(f"  Level Breakdown          : {metrics['level_counts']}")
    print("\nAnonymized Error Stream:")
    for log in anonymized_errors:
        print(f"  [{log['timestamp']}] {log['level']:<5s} IP: {log['ip']:<15s} | {log['endpoint']} ({log['latency_ms']}ms)")


# ==============================================================================
# PROJECT 2: Dynamic Payload Validation Rule Engine
# ==============================================================================
def project_2_payload_validator() -> None:
    print_project_header("2. Dynamic Payload Validation Rule Engine")

    # Validator predicate table mapping payload field names to validation lambdas
    rules: Dict[str, Tuple[Callable[[Any], bool], str]] = {
        "username": (
            lambda val: isinstance(val, str) and 3 <= len(val) <= 20 and val.isalnum(),
            "Username must be alphanumeric and between 3-20 characters."
        ),
        "email": (
            lambda val: isinstance(val, str) and "@" in val and "." in val.split("@")[-1],
            "Email must be a valid address format."
        ),
        "age": (
            lambda val: isinstance(val, int) and 18 <= val <= 120,
            "Age must be an integer between 18 and 120."
        ),
        "roles": (
            lambda val: isinstance(val, list) and len(val) > 0 and all(r in ["admin", "user", "editor"] for r in val),
            "Roles must be a non-empty list containing valid role strings."
        ),
    }

    def validate_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        for field, (validator_lambda, err_msg) in rules.items():
            if field not in payload:
                errors.append(f"Missing required field: {field!r}")
            elif not validator_lambda(payload[field]):
                errors.append(f"Field {field!r} invalid: {err_msg}")
        return len(errors) == 0, errors

    # Test Payload 1 (Valid)
    payload_valid = {
        "username": "alex99",
        "email": "alex@company.com",
        "age": 28,
        "roles": ["user", "editor"],
    }

    # Test Payload 2 (Invalid)
    payload_invalid = {
        "username": "a!",  # Too short & non-alphanumeric
        "email": "invalid_email.com",
        "age": 16,  # Under 18
        "roles": ["super_god_mode"],  # Unknown role
    }

    print("Validating Payload 1 (Valid Case):")
    is_valid_1, errs_1 = validate_payload(payload_valid)
    print(f"  Passed: {is_valid_1} | Errors: {errs_1}")

    print("\nValidating Payload 2 (Invalid Case):")
    is_valid_2, errs_2 = validate_payload(payload_invalid)
    print(f"  Passed: {is_valid_2}")
    for err in errs_2:
        print(f"    [X] {err}")


# ==============================================================================
# PROJECT 3: Multi-Column E-Commerce Inventory Sorter
# ==============================================================================
def project_3_inventory_sorter() -> None:
    print_project_header("3. Multi-Column E-Commerce Inventory Sorter")

    products = [
        {"sku": "SKU-001", "name": "Gaming Laptop", "category": "Electronics", "price": 1499.99, "stock": 12, "rating": 4.8},
        {"sku": "SKU-002", "name": "Wireless Mouse", "category": "Electronics", "price": 29.99,   "stock": 150, "rating": 4.3},
        {"sku": "SKU-003", "name": "Standing Desk",  "category": "Furniture",   "price": 450.00,  "stock": 8,  "rating": 4.8},
        {"sku": "SKU-004", "name": "Ergonomic Chair","category": "Furniture",   "price": 299.99,  "stock": 25, "rating": 4.5},
        {"sku": "SKU-005", "name": "Mechanical KB",  "category": "Electronics", "price": 89.99,   "stock": 45, "rating": 4.8},
        {"sku": "SKU-006", "name": "Monitor Arm",    "category": "Furniture",   "price": 65.00,   "stock": 0,  "rating": 4.1},
    ]

    # Flexible sorter factory accepting dynamic sort criteria list of (field, descending_bool)
    def create_table_sorter(criteria: List[Tuple[str, bool]]) -> Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]:
        """Creates a sorter lambda handling strings, floats, and inverted directions."""
        def key_builder(item: Dict[str, Any]) -> tuple:
            key_tuple = []
            for field, reverse in criteria:
                val = item[field]
                if isinstance(val, (int, float)):
                    key_tuple.append(-val if reverse else val)
                elif isinstance(val, str):
                    # For strings descending, invert character ordinals
                    key_tuple.append(tuple(-ord(c) for c in val) if reverse else val)
                else:
                    key_tuple.append(val)
            return tuple(key_tuple)

        return lambda data: sorted(data, key=key_builder)

    # Sort Preset 1: Category (Ascending) -> Rating (Descending) -> Price (Ascending)
    sorter_preset_1 = create_table_sorter([("category", False), ("rating", True), ("price", False)])
    sorted_1 = sorter_preset_1(products)

    print("Sorted by Category (Asc) -> Rating (Desc) -> Price (Asc):")
    print(f"  {'SKU':<8s} | {'Name':<18s} | {'Category':<12s} | {'Price':<9s} | {'Rating':<6s} | {'Stock'}")
    print(f"  {'-'*65}")
    for p in sorted_1:
        print(f"  {p['sku']:<8s} | {p['name']:<18s} | {p['category']:<12s} | ${p['price']:<8.2f} | {p['rating']:<6.1f} | {p['stock']}")


# ==============================================================================
# PROJECT 4: Event Listener & Functional Middleware Dispatcher
# ==============================================================================
def project_4_event_dispatcher() -> None:
    print_project_header("4. Event Listener & Functional Middleware Dispatcher")

    EventListener = Callable[[str, Dict[str, Any]], None]
    Middleware = Callable[[str, Dict[str, Any]], Dict[str, Any]]

    class EventBus:
        def __init__(self) -> None:
            self._listeners: Dict[str, List[EventListener]] = {}
            self._middlewares: List[Middleware] = []

        def use_middleware(self, mw: Middleware) -> None:
            self._middlewares.append(mw)

        def on(self, event_name: str, listener: EventListener) -> None:
            self._listeners.setdefault(event_name, []).append(listener)

        def emit(self, event_name: str, data: Dict[str, Any]) -> None:
            # Process data through middleware chain using reduce
            processed_data = reduce(
                lambda curr_data, mw: mw(event_name, curr_data),
                self._middlewares,
                data
            )

            # Invoke matching event listeners
            listeners = self._listeners.get(event_name, [])
            for handler in listeners:
                handler(event_name, processed_data)

    # Initialize Event Bus instance
    bus = EventBus()

    # Middleware 1: Timestamp Injector Middleware (Lambda)
    bus.use_middleware(lambda event, data: {**data, "_timestamp": datetime.now().isoformat()})

    # Middleware 2: Data Sanitizer Middleware (Lambda)
    bus.use_middleware(
        lambda event, data: {**data, "payload": {k: v.strip().upper() if isinstance(v, str) else v for k, v in data.get("payload", {}).items()}}
    )

    # Registering Event Handlers using Lambdas
    bus.on("USER_REGISTERED", lambda evt, data: print(f"  [AUDIT SERVICE] Event: {evt} | User: {data['payload'].get('username')} at {data['_timestamp']}"))
    bus.on("USER_REGISTERED", lambda evt, data: print(f"  [EMAIL SERVICE] Sending welcome email to {data['payload'].get('email')}"))

    print("Emitting 'USER_REGISTERED' Event through Middleware Pipeline:")
    bus.emit("USER_REGISTERED", {
        "payload": {
            "username": "   johndoe  ",
            "email": " john@example.com  ",
        }
    })


if __name__ == "__main__":
    project_1_etl_pipeline()
    project_2_payload_validator()
    project_3_inventory_sorter()
    project_4_event_dispatcher()
