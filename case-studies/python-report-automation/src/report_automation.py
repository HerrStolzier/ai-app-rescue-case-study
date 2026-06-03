import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


def load_customers(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def parse_money(value):
    try:
        if value is None or value.strip() == "":
            raise InvalidOperation("missing total")
        return Decimal(value)
    except (InvalidOperation, AttributeError) as error:
        raise ValueError(f"Invalid total: {value!r}") from error


def summarize_orders(orders_path, customers_path):
    customers = load_customers(customers_path)
    summary = defaultdict(lambda: {"paid_orders": 0, "paid_total": Decimal("0.00"), "invalid_rows": 0})

    with Path(orders_path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            customer_id = row["customer_id"]
            customer_name = customers.get(customer_id, "Unknown customer")
            bucket = summary[(customer_id, customer_name)]

            if row["status"] != "paid":
                continue

            try:
                total = parse_money(row["total"])
            except ValueError:
                bucket["invalid_rows"] += 1
                continue

            bucket["paid_orders"] += 1
            bucket["paid_total"] += total

    return [
        {
            "customer_id": customer_id,
            "customer_name": customer_name,
            "paid_orders": values["paid_orders"],
            "paid_total": f"{values['paid_total']:.2f}",
            "invalid_rows": values["invalid_rows"],
        }
        for (customer_id, customer_name), values in sorted(summary.items())
    ]


def write_summary(rows, output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["customer_id", "customer_name", "paid_orders", "paid_total", "invalid_rows"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate a customer payment summary report.")
    parser.add_argument("--orders", required=True)
    parser.add_argument("--customers", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = summarize_orders(args.orders, args.customers)
    write_summary(rows, args.output)
    print(f"Wrote {len(rows)} customer rows to {args.output}")


if __name__ == "__main__":
    main()
