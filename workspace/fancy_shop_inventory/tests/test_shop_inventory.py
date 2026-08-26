"""Automated Pytest Suite for Shop Inventory & POS Management System."""
import pytest
from fastapi.testclient import TestClient
from api.main import app, engine
from api.models import Item, CheckoutRequest, CartItem

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_inventory():
    engine.catalog.clear()
    engine.sales_history.clear()
    engine.khata_ledger.clear()

    engine.add_or_update_item(Item(sku="SKU-WATCH-01", name="Analog Wristwatch", category="Accessories", cost_price=250.0, selling_price=499.0, stock_quantity=15, reorder_level=5))
    engine.add_or_update_item(Item(sku="SKU-PERFUME-01", name="Rose Attar Perfume", category="Cosmetics", cost_price=80.0, selling_price=180.0, stock_quantity=20, reorder_level=5))
    engine.add_or_update_item(Item(sku="SKU-BANGLES-01", name="Glass Bangles Set", category="Jewelry", cost_price=30.0, selling_price=70.0, stock_quantity=3, reorder_level=5))


def test_catalog_and_low_stock_detection():
    resp = client.get("/api/items")
    assert resp.status_code == 200
    assert len(resp.json()) == 3

    resp = client.get("/api/items?low_stock_only=true")
    assert resp.status_code == 200
    low_stock = resp.json()
    assert len(low_stock) == 1
    assert low_stock[0]["sku"] == "SKU-BANGLES-01"


def test_pos_checkout_and_stock_reduction():
    req = {
        "customer_name": "Ramesh Kumar",
        "payment_mode": "UPI",
        "items": [{"sku": "SKU-PERFUME-01", "quantity": 2}],
        "discount_percent": 10.0
    }
    resp = client.post("/api/sales/checkout", json=req)
    assert resp.status_code == 200
    data = resp.json()

    assert data["subtotal"] == 360.0
    assert data["discount_applied"] == 36.0
    assert data["total_amount"] == 324.0

    perfume = engine.get_item("SKU-PERFUME-01")
    assert perfume.stock_quantity == 18


def test_out_of_stock_rejection():
    req = {
        "customer_name": "Sneha",
        "payment_mode": "Cash",
        "items": [{"sku": "SKU-BANGLES-01", "quantity": 10}]
    }
    resp = client.post("/api/sales/checkout", json=req)
    assert resp.status_code == 422
    assert "Insufficient stock" in resp.json()["detail"]


def test_khata_credit_and_daily_summary():
    req = {
        "customer_name": "Sharma Ji",
        "payment_mode": "Credit",
        "items": [{"sku": "SKU-WATCH-01", "quantity": 1}]
    }
    resp = client.post("/api/sales/checkout", json=req)
    assert resp.status_code == 200

    k_resp = client.get("/api/khata/ledger")
    assert k_resp.status_code == 200
    assert k_resp.json()["Sharma Ji"] == 499.0

    summary_resp = client.get("/api/analytics/daily-summary")
    assert summary_resp.status_code == 200
    s_data = summary_resp.json()
    assert s_data["total_bills_processed"] == 1
    assert s_data["total_revenue"] == 499.0
