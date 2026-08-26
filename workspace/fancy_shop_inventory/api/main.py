"""FastAPI Backend Server & Interactive Web UI for Fancy Shop Inventory & POS Platform."""
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import Item, CartItem, CheckoutRequest, SaleReceipt, KhataCreditEntry
from .engine import ShopInventoryEngine

app = FastAPI(
    title="Fancy Shop Inventory, POS & Khata Management Platform",
    version="1.0.0",
    description="Production-grade inventory, quick POS billing, and Khata ledger platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ShopInventoryEngine()

# Seed default fancy shop items
engine.add_or_update_item(Item(sku="SKU-WATCH-01", name="Analog Wristwatch (Gold Trim)", category="Accessories", cost_price=250.0, selling_price=499.0, stock_quantity=15, reorder_level=5))
engine.add_or_update_item(Item(sku="SKU-PERFUME-01", name="Rose Attar Perfume (100ml)", category="Cosmetics", cost_price=80.0, selling_price=180.0, stock_quantity=20, reorder_level=5))
engine.add_or_update_item(Item(sku="SKU-BANGLES-01", name="Bridal Glass Bangles Set", category="Jewelry", cost_price=30.0, selling_price=70.0, stock_quantity=4, reorder_level=5))
engine.add_or_update_item(Item(sku="SKU-GIFTBAG-01", name="Velvet Gift Bag with Ribbon", category="Packaging", cost_price=15.0, selling_price=40.0, stock_quantity=50, reorder_level=10))


@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "shop-inventory-pos"}


@app.post("/api/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_or_update_item(item: Item):
    return engine.add_or_update_item(item)


@app.get("/api/items", response_model=List[Item])
def list_items(low_stock_only: bool = False):
    return engine.list_items(low_stock_only=low_stock_only)


@app.post("/api/sales/checkout", response_model=SaleReceipt)
def checkout(req: CheckoutRequest):
    success, receipt, err = engine.process_checkout(req)
    if not success:
        raise HTTPException(status_code=422, detail=err)
    return receipt


@app.get("/api/analytics/daily-summary")
def get_daily_summary() -> Dict[str, Any]:
    return engine.get_daily_summary()


@app.get("/api/khata/ledger")
def get_khata_ledger() -> Dict[str, float]:
    return engine.khata_ledger


@app.get("/", response_class=HTMLResponse)
@app.get("/shop", response_class=HTMLResponse)
def serve_shop_ui():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fancy Shop POS, Inventory & Khata Ledger</title>
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --sub: #0f172a;
            --border: #334155;
            --text: #f8fafc;
            --dim: #94a3b8;
            --primary: #38bdf8;
            --green: #22c55e;
            --orange: #f59e0b;
            --red: #ef4444;
            --purple: #a855f7;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            padding: 16px;
            line-height: 1.5;
        }
        .container { max-width: 1100px; margin: 0 auto; }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 12px;
            margin-bottom: 16px;
        }
        h1 { font-size: 1.4rem; color: var(--primary); }
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 16px;
            margin-bottom: 16px;
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
        }
        .card h2 { font-size: 1.1rem; margin-bottom: 12px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 10px;
            margin-bottom: 16px;
        }
        .stat-box {
            background: var(--sub);
            padding: 10px;
            border-radius: 6px;
            border: 1px solid var(--border);
        }
        .stat-label { font-size: 0.75rem; color: var(--dim); text-transform: uppercase; }
        .stat-val { font-size: 1.25rem; font-weight: bold; margin-top: 4px; }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        th { color: var(--dim); font-size: 0.75rem; text-transform: uppercase; }
        .btn {
            background: var(--primary);
            color: #0f172a;
            border: none;
            padding: 8px 14px;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
            font-size: 0.85rem;
        }
        .btn-green { background: var(--green); color: #0f172a; }
        input, select {
            width: 100%;
            background: var(--sub);
            border: 1px solid var(--border);
            color: #fff;
            padding: 8px;
            border-radius: 4px;
            margin-bottom: 10px;
            font-size: 0.85rem;
        }
        .badge {
            padding: 2px 6px;
            border-radius: 10px;
            font-size: 0.75rem;
            font-weight: bold;
        }
        .badge-low { background: rgba(239, 68, 68, 0.2); color: var(--red); border: 1px solid var(--red); }
        .badge-ok { background: rgba(34, 197, 94, 0.2); color: var(--green); }
        .receipt-box {
            background: #000;
            padding: 12px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 0.85rem;
            border: 1px dashed var(--border);
            margin-top: 10px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>🛍️ Fancy Shop POS & Inventory Manager</h1>
                <div style="font-size: 0.8rem; color: var(--dim);">Digital POS Billing, Stock Reduction & Customer Khata (Udhar) Ledger</div>
            </div>
            <div>
                <span class="badge badge-ok">SYSTEM LIVE</span>
            </div>
        </header>

        <!-- Summary Metrics -->
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-label">Today's Revenue</div>
                <div class="stat-val" style="color: var(--green);" id="stat-rev">₹0.00</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Net Profit</div>
                <div class="stat-val" style="color: var(--primary);" id="stat-profit">₹0.00</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Total Bills</div>
                <div class="stat-val" style="color: #fff;" id="stat-bills">0</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Pending Khata (Udhar)</div>
                <div class="stat-val" style="color: var(--orange);" id="stat-khata">₹0.00</div>
            </div>
        </div>

        <div class="grid-2">
            <!-- 1. Quick POS Billing Counter -->
            <div class="card">
                <h2 style="color: var(--primary);">🧾 Quick POS Billing Checkout</h2>
                <form onsubmit="handleCheckout(event)">
                    <label style="font-size: 0.75rem; color: var(--dim);">Customer Name</label>
                    <input type="text" id="pos-customer" placeholder="E.g. Rajesh Kumar / Walk-in" value="Walk-in Customer" required />

                    <label style="font-size: 0.75rem; color: var(--dim);">Select Item</label>
                    <select id="pos-item-select"></select>

                    <label style="font-size: 0.75rem; color: var(--dim);">Quantity</label>
                    <input type="number" id="pos-qty" min="1" value="1" required />

                    <label style="font-size: 0.75rem; color: var(--dim);">Payment Method</label>
                    <select id="pos-payment">
                        <option value="Cash">💵 Cash</option>
                        <option value="UPI">📱 UPI (Google Pay / PhonePe / Paytm)</option>
                        <option value="Credit">📒 Credit (Khata / Udhar Ledger)</option>
                    </select>

                    <label style="font-size: 0.75rem; color: var(--dim);">Discount (%)</label>
                    <input type="number" id="pos-discount" min="0" max="100" value="0" />

                    <button type="submit" class="btn btn-green" style="width: 100%; margin-top: 4px;">⚡ Complete Sale & Print Bill</button>
                </form>

                <div id="receipt-container" style="display: none;">
                    <div class="receipt-box" id="receipt-output"></div>
                </div>
            </div>

            <!-- 2. Customer Khata Ledger & New Item -->
            <div class="card">
                <h2 style="color: var(--orange);">📒 Customer Credit (Khata / Udhar) Ledger</h2>
                <div id="khata-list" style="margin-bottom: 16px; max-height: 120px; overflow-y: auto;">
                    <p style="font-size: 0.85rem; color: var(--dim);">No pending customer dues recorded yet.</p>
                </div>

                <h2 style="color: var(--purple); border-top: 1px solid var(--border); padding-top: 12px;">➕ Add / Restock Item</h2>
                <form onsubmit="handleAddItem(event)">
                    <input type="text" id="add-sku" placeholder="SKU (e.g. SKU-RING-01)" required />
                    <input type="text" id="add-name" placeholder="Item Name (e.g. Silver Ring)" required />
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                        <input type="number" id="add-cost" placeholder="Cost (₹)" required />
                        <input type="number" id="add-sell" placeholder="Sell Price (₹)" required />
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                        <input type="number" id="add-stock" placeholder="Initial Stock" required />
                        <input type="number" id="add-reorder" placeholder="Reorder Level" value="5" />
                    </div>
                    <button type="submit" class="btn" style="width: 100%;">Save to Catalog</button>
                </form>
            </div>
        </div>

        <!-- Stock Catalog Table -->
        <div class="card">
            <h2 style="color: var(--primary);">📦 Current Inventory & Stock Levels</h2>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>SKU</th>
                            <th>Item Name</th>
                            <th>Category</th>
                            <th>Cost</th>
                            <th>Sell Price</th>
                            <th>Stock</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="catalog-table-body"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        async function loadData() {
            try {
                const res = await fetch('/api/items');
                const items = await res.json();
                
                const tableBody = document.getElementById('catalog-table-body');
                const select = document.getElementById('pos-item-select');
                
                tableBody.innerHTML = "";
                select.innerHTML = "";

                items.forEach(it => {
                    const isLow = it.stock_quantity <= it.reorder_level;
                    const badge = isLow ? `<span class="badge badge-low">LOW STOCK (${it.stock_quantity})</span>` : `<span class="badge badge-ok">IN STOCK (${it.stock_quantity})</span>`;

                    tableBody.innerHTML += `
                        <tr>
                            <td><code>${it.sku}</code></td>
                            <td><strong>${it.name}</strong></td>
                            <td>${it.category}</td>
                            <td>₹${it.cost_price.toFixed(2)}</td>
                            <td><strong>₹${it.selling_price.toFixed(2)}</strong></td>
                            <td>${it.stock_quantity}</td>
                            <td>${badge}</td>
                        </tr>
                    `;

                    select.innerHTML += `<option value="${it.sku}">${it.name} - ₹${it.selling_price} (Stock: ${it.stock_quantity})</option>`;
                });

                const sumRes = await fetch('/api/analytics/daily-summary');
                const sum = await sumRes.json();
                document.getElementById('stat-rev').innerText = `₹${sum.total_revenue.toFixed(2)}`;
                document.getElementById('stat-profit').innerText = `₹${sum.total_net_profit.toFixed(2)}`;
                document.getElementById('stat-bills').innerText = sum.total_bills_processed;
                document.getElementById('stat-khata').innerText = `₹${sum.total_outstanding_khata_dues.toFixed(2)}`;

                const khataRes = await fetch('/api/khata/ledger');
                const khata = await khataRes.json();
                const khataBox = document.getElementById('khata-list');
                const entries = Object.entries(khata);
                if (entries.length === 0) {
                    khataBox.innerHTML = '<p style="font-size: 0.85rem; color: var(--dim);">No pending customer dues recorded yet.</p>';
                } else {
                    let kHtml = "<table><thead><tr><th>Customer</th><th>Pending Due</th></tr></thead><tbody>";
                    entries.forEach(([name, due]) => {
                        kHtml += `<tr><td><strong>${name}</strong></td><td style="color: var(--orange); font-weight: bold;">₹${due.toFixed(2)}</td></tr>`;
                    });
                    kHtml += "</tbody></table>";
                    khataBox.innerHTML = kHtml;
                }
            } catch (err) {}
        }

        async function handleCheckout(e) {
            e.preventDefault();
            const customer = document.getElementById('pos-customer').value;
            const sku = document.getElementById('pos-item-select').value;
            const qty = parseInt(document.getElementById('pos-qty').value);
            const payment = document.getElementById('pos-payment').value;
            const discount = parseFloat(document.getElementById('pos-discount').value) || 0;

            try {
                const res = await fetch('/api/sales/checkout', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        customer_name: customer,
                        payment_mode: payment,
                        items: [{ sku: sku, quantity: qty }],
                        discount_percent: discount
                    })
                });

                if (!res.ok) {
                    const err = await res.json();
                    alert("Checkout Failed: " + err.detail);
                    return;
                }

                const receipt = await res.json();
                document.getElementById('receipt-container').style.display = 'block';
                document.getElementById('receipt-output').innerHTML = `
🧾 <strong>FANCY SHOP RETAIL BILL: ${receipt.sale_id}</strong>
📅 ${receipt.timestamp.slice(0, 19).replace('T', ' ')}
👤 Customer: ${receipt.customer_name}
💳 Payment: ${receipt.payment_mode}
----------------------------------------
Item: ${receipt.items_sold[0].name} x ${receipt.items_sold[0].quantity} = ₹${receipt.items_sold[0].line_total}
Subtotal: ₹${receipt.subtotal}
Discount: -₹${receipt.discount_applied}
<strong>TOTAL AMOUNT: ₹${receipt.total_amount}</strong>
----------------------------------------
✅ Stock Updated Automatically!
                `;

                loadData();
            } catch (err) {
                alert("Error during sale");
            }
        }

        async function handleAddItem(e) {
            e.preventDefault();
            const sku = document.getElementById('add-sku').value;
            const name = document.getElementById('add-name').value;
            const cost = parseFloat(document.getElementById('add-cost').value);
            const sell = parseFloat(document.getElementById('add-sell').value);
            const stock = parseInt(document.getElementById('add-stock').value);
            const reorder = parseInt(document.getElementById('add-reorder').value);

            await fetch('/api/items', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sku: sku,
                    name: name,
                    cost_price: cost,
                    selling_price: sell,
                    stock_quantity: stock,
                    reorder_level: reorder
                })
            });

            e.target.reset();
            loadData();
        }

        loadData();
    </script>
</body>
</html>
"""
