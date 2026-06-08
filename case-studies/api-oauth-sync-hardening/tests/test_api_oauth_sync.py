import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_sync_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "case-studies" / "api-oauth-sync-hardening" / "src" / "api_oauth_sync.py"
    spec = importlib.util.spec_from_file_location("api_oauth_sync", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


api_oauth_sync = load_sync_module()


def fake_token(label):
    return "-".join(["fake", "oauth", label])


class FakeOAuthProvider:
    def __init__(self):
        self.refresh_calls = []

    def refresh(self, refresh_token):
        self.refresh_calls.append(refresh_token)
        return {
            api_oauth_sync.ACCESS_TOKEN_KEY: fake_token("fresh"),
            "expires_at": 999,
        }


class FakeApiClient:
    def __init__(self):
        self.tokens_seen = []

    def list_jobs(self, access_token):
        self.tokens_seen.append(access_token)
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


class ApiOAuthSyncTest(unittest.TestCase):
    def test_refreshes_expired_token_before_api_call_and_writes_stable_csv(self):
        token_store = api_oauth_sync.MemoryTokenStore(
            {
                api_oauth_sync.ACCESS_TOKEN_KEY: fake_token("expired"),
                api_oauth_sync.REFRESH_TOKEN_KEY: fake_token("refresh"),
                "expires_at": 10,
            },
        )
        oauth_provider = FakeOAuthProvider()
        api_client = FakeApiClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "jobs.csv"
            result = api_oauth_sync.sync_jobs(
                token_store=token_store,
                oauth_provider=oauth_provider,
                api_client=api_client,
                output_path=output,
                now=100,
            )

            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(oauth_provider.refresh_calls, [fake_token("refresh")])
        self.assertEqual(api_client.tokens_seen, [fake_token("fresh")])
        self.assertEqual(result, {"refreshed": True, "written_rows": 2})
        self.assertEqual(rows[0]["job_id"], "job_001")
        self.assertEqual(rows[0]["gp_percent"], "60.00")
        self.assertEqual(rows[1]["job_id"], "job_002")
        self.assertEqual(rows[1]["gp_percent"], "50.00")

    def test_second_sync_updates_rows_without_duplicates(self):
        token_store = api_oauth_sync.MemoryTokenStore(
            {
                api_oauth_sync.ACCESS_TOKEN_KEY: fake_token("fresh"),
                api_oauth_sync.REFRESH_TOKEN_KEY: fake_token("refresh"),
                "expires_at": 999,
            },
        )
        oauth_provider = FakeOAuthProvider()
        api_client = FakeApiClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "jobs.csv"
            api_oauth_sync.sync_jobs(token_store, oauth_provider, api_client, output, now=100)
            api_oauth_sync.sync_jobs(token_store, oauth_provider, api_client, output, now=100)

            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(oauth_provider.refresh_calls, [])
        self.assertEqual([row["job_id"] for row in rows], ["job_001", "job_002"])

    def test_expired_token_without_refresh_token_fails_before_api_call(self):
        token_store = api_oauth_sync.MemoryTokenStore(
            {
                api_oauth_sync.ACCESS_TOKEN_KEY: fake_token("expired"),
                "expires_at": 10,
            },
        )
        oauth_provider = FakeOAuthProvider()
        api_client = FakeApiClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(ValueError, "refresh_token"):
                api_oauth_sync.sync_jobs(
                    token_store=token_store,
                    oauth_provider=oauth_provider,
                    api_client=api_client,
                    output_path=Path(tmpdir) / "jobs.csv",
                    now=100,
                )

        self.assertEqual(api_client.tokens_seen, [])


if __name__ == "__main__":
    unittest.main()
