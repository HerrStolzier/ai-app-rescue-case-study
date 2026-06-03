# Case Study C: Python Report Automation

This is a public demo case study. It is not client work and contains no private data.

## Failure

Manual reporting often breaks in small ways:

- missing customer names,
- invalid totals,
- inconsistent order status,
- no repeatable command,
- no handover for edge cases.

## Diagnosis

The workflow needs a small, repeatable script with validation rather than another manual spreadsheet pass.

Inputs:

- [orders.csv](inputs/orders.csv)
- [customers.json](inputs/customers.json)

## Fix

The script reads orders, joins customer data, validates totals, and writes a customer-level summary report.

Run:

```bash
python3 case-studies/python-report-automation/src/report_automation.py \
  --orders case-studies/python-report-automation/inputs/orders.csv \
  --customers case-studies/python-report-automation/inputs/customers.json \
  --output case-studies/python-report-automation/outputs/generated-summary.csv
```

## Verification

Run:

```bash
npm run verify:python
```

The tests verify:

- valid orders are aggregated correctly,
- invalid rows are counted,
- unknown customers do not crash the report,
- the output CSV is stable.

## Handover

See:

- [before.md](handover/before.md)
- [after.md](handover/after.md)
- [final-handover.md](handover/final-handover.md)
