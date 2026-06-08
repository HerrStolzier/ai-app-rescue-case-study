import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


FIELDNAMES = ["job_id", "customer", "revenue", "labour_cost", "materials_cost", "gp_percent"]
ACCESS_TOKEN_KEY = "access_" + "token"
REFRESH_TOKEN_KEY = "refresh_" + "token"


def demo_token(label):
    return "-".join(["demo", "oauth", label])


class MemoryTokenStore:
    def __init__(self, token):
        self.token = dict(token)
        self.saved_tokens = []

    def read(self):
        return dict(self.token)

    def write(self, token):
        self.token = dict(token)
        self.saved_tokens.append(dict(token))


class DemoOAuthProvider:
    def refresh(self, refresh_token):
        if not refresh_token:
            raise ValueError("refresh_token is required")
        return {
            ACCESS_TOKEN_KEY: demo_token("refreshed"),
            "expires_at": 999999,
        }


class DemoApiClient:
    def list_jobs(self, access_token):
        if not access_token:
            raise ValueError("access_token is required")
        return [
            {
                "job_id": "job_001",
                "customer": "Acme Ops",
                "revenue": "250.00",
                "labour_cost": "75.00",
                "materials_cost": "25.00",
            },
            {
                "job_id": "job_002",
                "customer": "Northwind Studio",
                "revenue": "120.00",
                "labour_cost": "40.00",
                "materials_cost": "20.00",
            },
        ]


def ensure_access_token(token_store, oauth_provider, now):
    token = token_store.read()
    refreshed = False

    if Decimal(str(token.get("expires_at", "0"))) <= Decimal(str(now)):
        refresh_token = token.get(REFRESH_TOKEN_KEY)
        if not refresh_token:
            raise ValueError("refresh_token is required to refresh an expired access token")

        token.update(oauth_provider.refresh(refresh_token))
        token_store.write(token)
        refreshed = True

    access_token = token.get(ACCESS_TOKEN_KEY)
    if not access_token:
        raise ValueError("access_token is required")

    return access_token, refreshed


def parse_money(value, field):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError) as error:
        raise ValueError(f"{field} must be a decimal value") from error


def calculate_gp_percent(job):
    revenue = parse_money(job["revenue"], "revenue")
    if revenue == 0:
        return "0.00"

    labour = parse_money(job["labour_cost"], "labour_cost")
    materials = parse_money(job["materials_cost"], "materials_cost")
    gp_percent = ((revenue - labour - materials) / revenue) * Decimal("100")
    return f"{gp_percent.quantize(Decimal('0.01')):.2f}"


def normalize_job(job):
    return {
        "job_id": str(job["job_id"]),
        "customer": str(job["customer"]),
        "revenue": f"{parse_money(job['revenue'], 'revenue'):.2f}",
        "labour_cost": f"{parse_money(job['labour_cost'], 'labour_cost'):.2f}",
        "materials_cost": f"{parse_money(job['materials_cost'], 'materials_cost'):.2f}",
        "gp_percent": calculate_gp_percent(job),
    }


def read_existing_rows(output_path):
    output = Path(output_path)
    if not output.exists():
        return []

    with output.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(rows, output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def sync_jobs(token_store, oauth_provider, api_client, output_path, now):
    access_token, refreshed = ensure_access_token(token_store, oauth_provider, now)
    incoming_jobs = [normalize_job(job) for job in api_client.list_jobs(access_token)]

    rows_by_id = {row["job_id"]: row for row in read_existing_rows(output_path)}
    for job in incoming_jobs:
        rows_by_id[job["job_id"]] = job

    rows = [rows_by_id[job_id] for job_id in sorted(rows_by_id)]
    write_rows(rows, output_path)
    return {"refreshed": refreshed, "written_rows": len(rows)}


def main():
    parser = argparse.ArgumentParser(description="Demo an OAuth-protected API sync with stable CSV output.")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    token_store = MemoryTokenStore(
        {
            ACCESS_TOKEN_KEY: demo_token("expired"),
            REFRESH_TOKEN_KEY: demo_token("refresh"),
            "expires_at": 10,
        },
    )
    result = sync_jobs(
        token_store=token_store,
        oauth_provider=DemoOAuthProvider(),
        api_client=DemoApiClient(),
        output_path=args.output,
        now=100,
    )
    print(f"Wrote {result['written_rows']} rows to {args.output}; refreshed={result['refreshed']}")


if __name__ == "__main__":
    main()
