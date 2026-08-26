"""Automated Pytest Suite for Bank Statement Expense Tracker."""
import pytest
from api.parser import parse_csv_statement, categorize_merchant, clean_amount
from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

SAMPLE_CSV = """Date,Description,Amount,Type,Balance
2026-08-01,EMPLOYER PAYROLL DIRECT DEPOSIT,3500.00,Credit,4500.00
2026-08-02,KROGER GROCERY STORE,-124.50,Debit,4375.50
2026-08-03,SHELL GAS STATION,-45.00,Debit,4330.50
2026-08-04,NETFLIX.COM SUBSCRIPTION,-15.99,Debit,4314.51
2026-08-05,STARBUCKS COFFEE,-6.75,Debit,4307.76
"""


def test_clean_amount():
    assert clean_amount("124.50") == 124.50
    assert clean_amount("-45.00") == -45.00
    assert clean_amount("$3,500.00") == 3500.00
    assert clean_amount("(50.00)") == -50.00


def test_categorize_merchant():
    cat, conf = categorize_merchant("KROGER STORE #0421")
    assert cat == "Groceries"
    assert conf >= 0.90

    cat_sub, _ = categorize_merchant("NETFLIX.COM")
    assert cat_sub == "Subscriptions"

    cat_sal, _ = categorize_merchant("PAYROLL ACME CORP")
    assert cat_sal == "Income"


def test_parse_csv_statement():
    txns = parse_csv_statement(SAMPLE_CSV)
    assert len(txns) == 5
    assert txns[0]["description"] == "EMPLOYER PAYROLL DIRECT DEPOSIT"
    assert txns[0]["amount"] == 3500.00
    assert txns[1]["category"] == "Groceries"
    assert txns[2]["category"] == "Transport"


def test_api_upload_and_analytics():
    # 1. Health check
    resp = client.get("/api/health")
    assert resp.status_code == 200

    # 2. Upload CSV statement
    files = {"file": ("statement.csv", SAMPLE_CSV, "text/csv")}
    upload_resp = client.post("/api/statements/upload", files=files)
    assert upload_resp.status_code == 200
    data = upload_resp.json()
    assert data["transactions_extracted"] == 5
    assert data["total_inflow"] == 3500.00

    # 3. List transactions
    txn_resp = client.get("/api/transactions")
    assert txn_resp.status_code == 200
    assert len(txn_resp.json()) == 5

    # 4. Filter by category
    groc_resp = client.get("/api/transactions?category=Groceries")
    assert groc_resp.status_code == 200
    assert len(groc_resp.json()) == 1

    # 5. Analytics summary
    summary_resp = client.get("/api/analytics/summary")
    assert summary_resp.status_code == 200
    s_data = summary_resp.json()
    assert s_data["total_inflow"] == 3500.00
    assert "Groceries" in s_data["category_breakdown"]
