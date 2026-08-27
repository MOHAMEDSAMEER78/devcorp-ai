"""FastAPI Backend Server & Interactive Web UI for Fancy Shop Inventory & POS Platform (Sprint 2)."""
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import Item, CartItem, CheckoutRequest, SaleReceipt, KhataPayment, SupplierPurchase
from .engine import ShopInventoryEngine

app = FastAPI(
    title="Fancy Shop POS, Inventory & Khata Ledger Platform (Sprint 2)",
    version="2.0.0",
    description="Multi-item cart, GST tax engine, customer Khata repayment, and CSV exports"
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
engine.add_or_update_item(Item(sku="SKU-WATCH-01", name="Analog Wristwatch (Gold Trim)", category="Accessories", cost_price=250.0, selling_price=499.0, stock_quantity=15, reorder_level=5, gst_rate=18.0))
engine.add_or_update_item(Item(sku="SKU-PERFUME-01", name="Rose Attar Perfume (100ml)", category="Cosmetics", cost_price=80.0, selling_price=180.0, stock_quantity=20, reorder_level=5, gst_rate=12.0))
engine.add_or_update_item(Item(sku="SKU-BANGLES-01", name="Bridal Glass Bangles Set", category="Jewelry", cost_price=30.0, selling_price=70.0, stock_quantity=4, reorder_level=5, gst_rate=5.0))
engine.add_or_update_item(Item(sku="SKU-GIFTBAG-01", name="Velvet Gift Bag with Ribbon", category="Packaging", cost_price=15.0, selling_price=40.0, stock_quantity=50, reorder_level=10, gst_rate=0.0))


@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "shop-inventory-pos-sprint2"}


@app.post("/api/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_or_update_item(item: Item):
    return engine.add_or_update_item(item)


@app.get("/api/items", response_model=List[Item])
def list_items(low_stock_only: bool = False, category: Optional[str] = None):
    return engine.list_items(low_stock_only=low_stock_only, category=category)


@app.post("/api/sales/checkout", response_model=SaleReceipt)
def checkout(req: CheckoutRequest):
    success, receipt, err = engine.process_checkout(req)
    if not success:
        raise HTTPException(status_code=422, detail=err)
    return receipt


@app.post("/api/khata/repay")
def repay_khata(payment: KhataPayment):
    """Record customer repayment against pending credit dues."""
    success, new_due, err = engine.settle_khata_due(payment)
    if not success:
        raise HTTPException(status_code=422, detail=err)
    return {
        "status": "SUCCESS",
        "customer_name": payment.customer_name,
        "amount_paid": payment.amount_paid,
        "remaining_due": new_due
    }


@app.get("/api/khata/ledger")
def get_khata_ledger() -> Dict[str, float]:
    return engine.khata_ledger


@app.get("/api/khata/history")
def get_khata_history() -> List[Dict[str, Any]]:
    return engine.khata_history


@app.post("/api/suppliers/purchase", response_model=SupplierPurchase)
def record_purchase(supplier_name: str, items: List[CartItem]):
    return engine.record_supplier_purchase(supplier_name, items)


@app.get("/api/analytics/daily-summary")
def get_daily_summary() -> Dict[str, Any]:
    return engine.get_daily_summary()


@app.get("/api/export/sales.csv")
def export_sales():
    csv_data = engine.export_sales_csv()
    return Response(content=csv_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=sales_register.csv"})


@app.get("/api/export/inventory.csv")
def export_inventory():
    csv_data = engine.export_inventory_csv()
    return Response(content=csv_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=inventory_audit.csv"})


@app.get("/api/export/khata.csv")
def export_khata():
    csv_data = engine.export_khata_csv()
    return Response(content=csv_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=khata_receivables.csv"})


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
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 8px;
        }
        h1 { font-size: 1.4rem; color: var(--primary); }
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 16px;
            margin-bottom: 16px;
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
        }
        .card h2 { font-size: 1.1rem; margin-bottom: 12px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
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
            text-decoration: none;
            display: inline-block;
        }
        .btn-green { background: var(--green); color: #0f172a; }
        .btn-orange { background: var(--orange); color: #0f172a; }
        .btn-purple { background: var(--purple); color: #fff; }
        .btn-sm { padding: 4px 8px; font-size: 0.75rem; }
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
        .cart-item-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--sub);
            padding: 8px 12px;
            border-radius: 4px;
            margin-bottom: 6px;
            font-size: 0.85rem;
            border: 1px solid var(--border);
        }
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
                <h1>🛍️ Fancy Shop POS & Inventory Manager (Sprint 2)</h1>
                <div style="font-size: 0.8rem; color: var(--dim);">Multi-Item Cart • GST Engine • Customer Khata Repayment • CSV Exports</div>
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <a href="/shop/api/export/sales.csv" class="btn btn-sm">📥 Export Sales</a>
                <a href="/shop/api/export/inventory.csv" class="btn btn-sm">📥 Export Stock</a>
                <a href="/shop/api/export/khata.csv" class="btn btn-sm btn-orange">📥 Export Khata</a>
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
            <!-- 1. Multi-Item POS Billing Counter -->
            <div class="card">
                <h2 style="color: var(--primary);">🧾 Multi-Item POS Billing Register</h2>
                
                <!-- Add Item to Cart Bar -->
                <div style="background: var(--sub); padding: 10px; border-radius: 6px; border: 1px solid var(--border); margin-bottom: 12px;">
                    <div style="display: grid; grid-template-columns: 2fr 1fr auto; gap: 8px; align-items: center;">
                        <select id="pos-item-select" style="margin-bottom: 0;"></select>
                        <input type="number" id="pos-qty" min="1" value="1" placeholder="Qty" style="margin-bottom: 0;" />
                        <button type="button" onclick="addToCart()" class="btn">+ Add</button>
                    </div>
                </div>

                <!-- Live Cart List -->
                <div style="margin-bottom: 12px;">
                    <div style="font-size: 0.8rem; color: var(--dim); margin-bottom: 6px;">🛒 Current Cart Items:</div>
                    <div id="cart-list">
                        <p style="font-size: 0.85rem; color: var(--dim);">Cart is empty. Select items above to ring up bill.</p>
                    </div>
                </div>

                <form onsubmit="handleCheckout(event)">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                        <div>
                            <label style="font-size: 0.75rem; color: var(--dim);">Customer Name</label>
                            <input type="text" id="pos-customer" value="Walk-in Customer" required />
                        </div>
                        <div>
                            <label style="font-size: 0.75rem; color: var(--dim);">WhatsApp / Mobile</label>
                            <input type="text" id="pos-phone" placeholder="9876543210" />
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                        <div>
                            <label style="font-size: 0.75rem; color: var(--dim);">Payment Method</label>
                            <select id="pos-payment">
                                <option value="Cash">💵 Cash</option>
                                <option value="UPI">📱 UPI (GPay/PhonePe)</option>
                                <option value="Credit">📒 Credit (Khata/Udhar)</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size: 0.75rem; color: var(--dim);">Discount (%)</label>
                            <input type="number" id="pos-discount" min="0" max="100" value="0" />
                        </div>
                    </div>

                    <div style="margin-bottom: 10px;">
                        <label style="font-size: 0.8rem; cursor: pointer; color: var(--text);">
                            <input type="checkbox" id="pos-gst" style="width: auto; margin-right: 6px;" /> Apply GST Tax (Item Rates)
                        </label>
                    </div>

                    <button type="submit" class="btn btn-green" style="width: 100%; padding: 10px; font-size: 0.95rem;">⚡ Complete Sale & Print Bill</button>
                </form>

                <div id="receipt-container" style="display: none;">
                    <div class="receipt-box" id="receipt-output"></div>
                    <button type="button" onclick="shareWhatsApp()" class="btn btn-green btn-sm" style="margin-top: 8px; width: 100%;">📲 Share Bill on WhatsApp</button>
                </div>
            </div>

            <!-- 2. Customer Khata Settlement & Add Item -->
            <div>
                <!-- Khata Ledger & Settlement -->
                <div class="card">
                    <h2 style="color: var(--orange);">📒 Customer Khata (Udhar) Ledger & Repayment</h2>
                    <div id="khata-list" style="margin-bottom: 12px; max-height: 140px; overflow-y: auto;">
                        <p style="font-size: 0.85rem; color: var(--dim);">No pending customer dues recorded yet.</p>
                    </div>

                    <!-- Record Payment Form -->
                    <div style="background: var(--sub); padding: 10px; border-radius: 6px; border: 1px solid var(--border);">
                        <div style="font-size: 0.75rem; color: var(--dim); margin-bottom: 6px; text-transform: uppercase;">💳 Record Customer Repayment</div>
                        <form onsubmit="handleKhataRepay(event)">
                            <div style="display: grid; grid-template-columns: 2fr 1fr auto; gap: 8px;">
                                <input type="text" id="repay-customer" placeholder="Customer Name" required style="margin-bottom: 0;" />
                                <input type="number" id="repay-amount" placeholder="Amount (₹)" required style="margin-bottom: 0;" />
                                <button type="submit" class="btn btn-orange">Settle</button>
                            </div>
                        </form>
                    </div>
                </div>

                <!-- Add / Restock Item -->
                <div class="card">
                    <h2 style="color: var(--purple);">➕ Add / Restock Catalog Item</h2>
                    <form onsubmit="handleAddItem(event)">
                        <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 8px;">
                            <input type="text" id="add-sku" placeholder="SKU (e.g. SKU-RING-01)" required />
                            <input type="text" id="add-name" placeholder="Item Name (e.g. Silver Ring)" required />
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;">
                            <input type="number" id="add-cost" placeholder="Cost (₹)" required />
                            <input type="number" id="add-sell" placeholder="Sell Price (₹)" required />
                            <select id="add-gst">
                                <option value="0">0% GST</option>
                                <option value="5">5% GST</option>
                                <option value="12">12% GST</option>
                                <option value="18">18% GST</option>
                            </select>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                            <input type="number" id="add-stock" placeholder="Initial Stock" required />
                            <input type="number" id="add-reorder" placeholder="Reorder Level" value="5" />
                        </div>
                        <button type="submit" class="btn btn-purple" style="width: 100%;">Save to Catalog</button>
                    </form>
                </div>
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
                            <th>Barcode</th>
                            <th>Item Name</th>
                            <th>Category</th>
                            <th>Cost</th>
                            <th>Sell Price</th>
                            <th>GST</th>
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
        let currentCart = [];
        let lastReceipt = null;

        async function loadData() {
            try {
                const res = await fetch('/shop/api/items');
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
                            <td><small style="color: var(--dim);">${it.barcode || '-'}</small></td>
                            <td><strong>${it.name}</strong></td>
                            <td>${it.category}</td>
                            <td>₹${it.cost_price.toFixed(2)}</td>
                            <td><strong>₹${it.selling_price.toFixed(2)}</strong></td>
                            <td>${it.gst_rate}%</td>
                            <td>${it.stock_quantity}</td>
                            <td>${badge}</td>
                        </tr>
                    `;

                    select.innerHTML += `<option value="${it.sku}" data-name="${it.name}" data-price="${it.selling_price}">${it.name} - ₹${it.selling_price} (Stock: ${it.stock_quantity})</option>`;
                });

                const sumRes = await fetch('/shop/api/analytics/daily-summary');
                const sum = await sumRes.json();
                document.getElementById('stat-rev').innerText = `₹${sum.total_revenue.toFixed(2)}`;
                document.getElementById('stat-profit').innerText = `₹${sum.total_net_profit.toFixed(2)}`;
                document.getElementById('stat-bills').innerText = sum.total_bills_processed;
                document.getElementById('stat-khata').innerText = `₹${sum.total_outstanding_khata_dues.toFixed(2)}`;

                const khataRes = await fetch('/shop/api/khata/ledger');
                const khata = await khataRes.json();
                const khataBox = document.getElementById('khata-list');
                const entries = Object.entries(khata);
                if (entries.length === 0 || entries.every(([_, d]) => d === 0)) {
                    khataBox.innerHTML = '<p style="font-size: 0.85rem; color: var(--dim);">No pending customer dues recorded yet.</p>';
                } else {
                    let kHtml = "<table><thead><tr><th>Customer</th><th>Pending Due</th><th>Action</th></tr></thead><tbody>";
                    entries.forEach(([name, due]) => {
                        if (due > 0) {
                            kHtml += `<tr><td><strong>${name}</strong></td><td style="color: var(--orange); font-weight: bold;">₹${due.toFixed(2)}</td><td><button class="btn btn-sm btn-orange" onclick="prefillRepay('${name}', ${due})">Settle</button></td></tr>`;
                        }
                    });
                    kHtml += "</tbody></table>";
                    khataBox.innerHTML = kHtml;
                }
            } catch (err) {}
        }

        function addToCart() {
            const select = document.getElementById('pos-item-select');
            const sku = select.value;
            const opt = select.options[select.selectedIndex];
            const name = opt.getAttribute('data-name');
            const price = parseFloat(opt.getAttribute('data-price'));
            const qty = parseInt(document.getElementById('pos-qty').value) || 1;

            const existing = currentCart.find(c => c.sku === sku);
            if (existing) {
                existing.quantity += qty;
            } else {
                currentCart.push({ sku, name, price, quantity: qty, discount_percent: 0 });
            }
            renderCart();
        }

        function removeFromCart(idx) {
            currentCart.splice(idx, 1);
            renderCart();
        }

        function renderCart() {
            const box = document.getElementById('cart-list');
            if (currentCart.length === 0) {
                box.innerHTML = '<p style="font-size: 0.85rem; color: var(--dim);">Cart is empty. Select items above to ring up bill.</p>';
                return;
            }

            let html = "";
            let subtotal = 0;
            currentCart.forEach((item, idx) => {
                const total = item.price * item.quantity;
                subtotal += total;
                html += `
                    <div class="cart-item-row">
                        <div><strong>${item.name}</strong> <span style="color: var(--dim);">x${item.quantity}</span></div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <strong>₹${total.toFixed(2)}</strong>
                            <button type="button" class="btn btn-sm" style="background: var(--red); color: #fff;" onclick="removeFromCart(${idx})">✕</button>
                        </div>
                    </div>
                `;
            });
            html += `<div style="text-align: right; font-size: 0.9rem; margin-top: 4px;"><strong>Subtotal: ₹${subtotal.toFixed(2)}</strong></div>`;
            box.innerHTML = html;
        }

        function prefillRepay(name, due) {
            document.getElementById('repay-customer').value = name;
            document.getElementById('repay-amount').value = due;
        }

        async function handleCheckout(e) {
            e.preventDefault();
            if (currentCart.length === 0) {
                alert("Please add at least one item to the cart.");
                return;
            }

            const customer = document.getElementById('pos-customer').value;
            const phone = document.getElementById('pos-phone').value;
            const payment = document.getElementById('pos-payment').value;
            const discount = parseFloat(document.getElementById('pos-discount').value) || 0;
            const applyGst = document.getElementById('pos-gst').checked;

            try {
                const res = await fetch('/shop/api/sales/checkout', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        customer_name: customer,
                        customer_phone: phone,
                        payment_mode: payment,
                        items: currentCart.map(c => ({ sku: c.sku, quantity: c.quantity })),
                        apply_gst: applyGst,
                        overall_discount: discount
                    })
                });

                if (!res.ok) {
                    const err = await res.json();
                    alert("Checkout Failed: " + err.detail);
                    return;
                }

                lastReceipt = await res.json();
                document.getElementById('receipt-container').style.display = 'block';
                document.getElementById('receipt-output').innerText = lastReceipt.whatsapp_share_text;

                currentCart = [];
                renderCart();
                loadData();
            } catch (err) {
                alert("Error during sale");
            }
        }

        async function handleKhataRepay(e) {
            e.preventDefault();
            const customer = document.getElementById('repay-customer').value;
            const amount = parseFloat(document.getElementById('repay-amount').value);

            const res = await fetch('/shop/api/khata/repay', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    customer_name: customer,
                    amount_paid: amount,
                    payment_mode: "Cash"
                })
            });

            if (!res.ok) {
                const err = await res.json();
                alert("Repayment Error: " + err.detail);
                return;
            }

            const data = await res.json();
            alert(`✅ Payment Recorded! Remaining due for ${customer}: ₹${data.remaining_due.toFixed(2)}`);
            e.target.reset();
            loadData();
        }

        async function handleAddItem(e) {
            e.preventDefault();
            const sku = document.getElementById('add-sku').value;
            const name = document.getElementById('add-name').value;
            const cost = parseFloat(document.getElementById('add-cost').value);
            const sell = parseFloat(document.getElementById('add-sell').value);
            const gst = parseFloat(document.getElementById('add-gst').value);
            const stock = parseInt(document.getElementById('add-stock').value);
            const reorder = parseInt(document.getElementById('add-reorder').value);

            await fetch('/shop/api/items', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sku: sku,
                    name: name,
                    cost_price: cost,
                    selling_price: sell,
                    gst_rate: gst,
                    stock_quantity: stock,
                    reorder_level: reorder
                })
            });

            e.target.reset();
            loadData();
        }

        function shareWhatsApp() {
            if (!lastReceipt) return;
            const text = encodeURIComponent(lastReceipt.whatsapp_share_text);
            window.open(`https://api.whatsapp.com/send?text=${text}`, '_blank');
        }

        loadData();
    </script>
</body>
</html>
"""
