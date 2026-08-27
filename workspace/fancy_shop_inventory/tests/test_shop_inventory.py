"""Automated Pytest Suite for Shop Inventory & POS Platform (Sprint 2)."""
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
    engine.khata_history.clear()
    engine.purchases_history.clear()

    engine.add_or_update_item(Item(sku="SKU-WATCH-01", name="Analog Wristwatch", category="Accessories", cost_price=250.0, selling_price=499.0, stock_quantity=15, reorder_level=5, gst_rate=18.0))
    engine.add_or_update_item(Item(sku="SKU-PERFUME-01", name="Rose Attar Perfume", category="Cosmetics", cost_price=80.0, selling_price=180.0, stock_quantity=20, reorder_level=5, gst_rate=12.0))
    engine.add_or_update_item(Item(sku="SKU-BANGLES-01", name="Glass Bangles Set", category="Jewelry", cost_price=30.0, selling_price=70.0, stock_quantity=4, reorder_level=5, gst_rate=5.0))


def test_catalog_and_low_stock():
    resp = client.get("/api/items")
    assert resp.status_code == 200
    assert len(resp.json()) == 3

    resp_low = client.get("/api/items?low_stock_only=true")
    assert resp_low.status_code == 200
    assert len(resp_low.json()) == 1
    assert resp_low.json()[0]["sku"] == "SKU-BANGLES-01"


def test_multi_item_checkout_with_gst_and_discount():
    # Buy 1 Watch + 2 Perfumes with 10% discount and GST enabled
    req = {
        "customer_name": "Vikram Singh",
        "customer_phone": "9876543210",
        "payment_mode": "UPI",
        "items": [
            {"sku": "SKU-WATCH-01", "quantity": 1},
            {"sku": "SKU-PERFUME-01", "quantity": 2}
        ],
        "apply_gst": True,
        "overall_discount": 10.0
    }
    resp = client.post("/api/sales/checkout", json=req)
    assert resp.status_code == 200
    data = resp.json()

    assert data["customer_name"] == "Vikram Singh"
    assert len(data["items_sold"]) == 2
    assert "WhatsApp" not in data["whatsapp_share_text"] or len(data["whatsapp_share_text"]) > 20
    assert data["gst_amount"] > 0
    assert data["total_amount"] > 0

    # Verify inventory was decremented
    watch = engine.get_item("SKU-WATCH-01")
    perfume = engine.get_item("SKU-PERFUME-01")
    assert watch.stock_quantity == 14
    assert perfume.stock_quantity == 18


def test_out_of_stock_validation():
    req = {
        "customer_name": "Rani",
        "items": [{"sku": "SKU-BANGLES-01", "quantity": 10}]
    }
    resp = client.post("/api/sales/checkout", json=req)
    assert resp.status_code == 422
    assert "Insufficient stock" in resp.json()["detail"]


def test_khata_credit_and_repayment_settlement():
    # 1. Buy on Credit
    req = {
        "customer_name": "Gupta Ji",
        "payment_mode": "Credit",
        "items": [{"sku": "SKU-WATCH-01", "quantity": 1}],
        "apply_gst": False
    }
    resp = client.post("/api/sales/checkout", json=req)
    assert resp.status_code == 200

    # Verify Khata Ledger
    k_resp = client.get("/api/khata/ledger")
    assert k_resp.status_code == 200
    assert k_resp.json()["Gupta Ji"] == 499.0

    # 2. Customer repays ₹300 partial due
    repay_req = {
        "customer_name": "Gupta Ji",
        "amount_paid": 300.0,
        "payment_mode": "Cash"
    }
    repay_resp = client.post("/api/khata/repay", json=repay_req)
    assert repay_resp.status_code == 200
    assert repay_resp.json()["remaining_due"] == 199.0

    # 3. Check updated ledger
    k_resp2 = client.get("/api/khata/ledger")
    assert k_resp2.json()["Gupta Ji"] == 199.0


def test_csv_exports_and_supplier_purchase():
    # 1. Supplier purchase (restock)
    p_resp = client.post(
        "/api/suppliers/purchase?supplier_name=Surat_Textiles",
        json=[{"sku": "SKU-BANGLES-01", "quantity": 20}]
    )
    assert p_resp.status_code == 200
    assert engine.get_item("SKU-BANGLES-01").stock_quantity == 24

    # 2. Export Inventory CSV
    inv_csv = client.get("/api/export/inventory.csv")
    assert inv_csv.status_code == 200
    assert "SKU-BANGLES-01" in inv_csv.text

    # 3. Export Sales CSV
    sales_csv = client.get("/api/export/sales.csv")
    assert sales_csv.status_code == 200
    assert "Sale ID" in sales_csv.text
