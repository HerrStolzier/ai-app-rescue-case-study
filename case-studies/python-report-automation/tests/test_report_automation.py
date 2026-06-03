import csv
import tempfile
import unittest
from pathlib import Path

from case_studies_import import load_report_module


report_automation = load_report_module()


ROOT = Path(__file__).resolve().parents[3]
CASE_DIR = ROOT / "case-studies" / "python-report-automation"


class ReportAutomationTest(unittest.TestCase):
    def test_summarizes_paid_orders_and_invalid_rows(self):
        rows = report_automation.summarize_orders(
            CASE_DIR / "inputs" / "orders.csv",
            CASE_DIR / "inputs" / "customers.json",
        )

        self.assertEqual(
            rows,
            [
                {
                    "customer_id": "c_001",
                    "customer_name": "Northwind Studio",
                    "paid_orders": 1,
                    "paid_total": "120.50",
                    "invalid_rows": 0,
                },
                {
                    "customer_id": "c_002",
                    "customer_name": "Acme Ops",
                    "paid_orders": 2,
                    "paid_total": "95.25",
                    "invalid_rows": 0,
                },
                {
                    "customer_id": "c_003",
                    "customer_name": "Missing Total Ltd",
                    "paid_orders": 0,
                    "paid_total": "0.00",
                    "invalid_rows": 1,
                },
                {
                    "customer_id": "c_004",
                    "customer_name": "Unknown customer",
                    "paid_orders": 1,
                    "paid_total": "42.00",
                    "invalid_rows": 0,
                },
            ],
        )

    def test_writes_stable_csv(self):
        rows = report_automation.summarize_orders(
            CASE_DIR / "inputs" / "orders.csv",
            CASE_DIR / "inputs" / "customers.json",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "summary.csv"
            report_automation.write_summary(rows, output)

            with output.open(newline="", encoding="utf-8") as handle:
                written = list(csv.DictReader(handle))

        self.assertEqual(written[1]["customer_name"], "Acme Ops")
        self.assertEqual(written[1]["paid_total"], "95.25")


if __name__ == "__main__":
    unittest.main()
