"""Sprint 2 Engine: POS Multi-Item Cart, GST Engine, Khata Settlement, CSV Exporter."""
import uuid
import io
import csv
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from .models import Item, CartItem, CheckoutRequest, SaleReceipt, KhataPayment, SupplierPurchase


class ShopInventoryEngine:
    def __init__(self):
        self.catalog: Dict[str, Item] = {}
        self.sales_history: List[SaleReceipt] = []
        self.khata_ledger: Dict[str, float] = {}  # Customer -> Outstanding Due
        self.khata_history: List[Dict[str, Any]] = []
        self.purchases_history: List[SupplierPurchase] = []

    def add_or_update_item(self, item: Item) -> Item:
        if not item.barcode:
            item.barcode = f"BAR-{item.sku.replace('SKU-', '')}"
        self.catalog[item.sku] = item
        return item

    def get_item(self, sku_or_barcode: str) -> Optional[Item]:
        if sku_or_barcode in self.catalog:
            return self.catalog[sku_or_barcode]
        # Search by barcode
        for it in self.catalog.values():
            if it.barcode == sku_or_barcode:
                return it
        return None

    def list_items(self, low_stock_only: bool = False, category: Optional[str] = None) -> List[Item]:
        items = list(self.catalog.values())
        if category:
            items = [it for it in items if it.category.lower() == category.lower()]
        if low_stock_only:
            items = [it for it in items if it.stock_quantity <= it.reorder_level]
        return items

    def process_checkout(self, req: CheckoutRequest) -> Tuple[bool, Optional[SaleReceipt], Optional[str]]:
        if not req.items:
            return False, None, "Checkout cart is empty"

        # 1. Validate stock availability for all items
        for cart_item in req.items:
            it = self.get_item(cart_item.sku)
            if not it:
                return False, None, f"Item '{cart_item.sku}' not found in catalog"
            if it.stock_quantity < cart_item.quantity:
                return False, None, f"Insufficient stock for '{it.name}' (Available: {it.stock_quantity}, In Cart: {cart_item.quantity})"

        # 2. Process line items
        items_sold = []
        subtotal = 0.0
        cost_total = 0.0
        total_gst = 0.0

        for cart_item in req.items:
            it = self.get_item(cart_item.sku)
            line_gross = it.selling_price * cart_item.quantity
            line_disc = line_gross * (cart_item.discount_percent / 100.0)
            line_net = line_gross - line_disc
            line_cost = it.cost_price * cart_item.quantity

            if req.apply_gst and it.gst_rate > 0:
                line_gst = line_net * (it.gst_rate / 100.0)
            else:
                line_gst = 0.0

            subtotal += line_net
            cost_total += line_cost
            total_gst += line_gst
            it.stock_quantity -= cart_item.quantity  # Atomic inventory deduction

            items_sold.append({
                "sku": it.sku,
                "name": it.name,
                "quantity": cart_item.quantity,
                "unit_price": it.selling_price,
                "line_total": round(line_net, 2)
            })

        overall_disc = subtotal * (req.overall_discount / 100.0)
        final_total = round(subtotal - overall_disc + total_gst, 2)
        total_profit = round(final_total - total_gst - cost_total, 2)

        sale_id = f"BILL-{uuid.uuid4().hex[:6].upper()}"
        ts = datetime.now(timezone.utc).isoformat()
        c_name = req.customer_name or "Walk-in Customer"

        # Build WhatsApp Message Text
        wa_text = (
            f"🛍️ *Fancy Shop - Bill #{sale_id}*\n"
            f"👤 Customer: {c_name}\n"
            f"📅 Date: {ts[:10]}\n"
            f"--------------------------\n"
        )
        for i in items_sold:
            wa_text += f"• {i['name']} x{i['quantity']} = ₹{i['line_total']}\n"
        wa_text += (
            f"--------------------------\n"
            f"Subtotal: ₹{round(subtotal, 2)}\n"
            f"GST Tax: ₹{round(total_gst, 2)}\n"
            f"*Total Paid: ₹{final_total} ({req.payment_mode})*\n"
            f"🙏 Thank you for visiting Fancy Shop!"
        )

        receipt = SaleReceipt(
            sale_id=sale_id,
            timestamp=ts,
            customer_name=c_name,
            customer_phone=req.customer_phone,
            payment_mode=req.payment_mode,
            items_sold=items_sold,
            subtotal=round(subtotal, 2),
            discount_applied=round(overall_disc, 2),
            gst_amount=round(total_gst, 2),
            total_amount=final_total,
            total_profit=total_profit,
            whatsapp_share_text=wa_text
        )

        self.sales_history.append(receipt)

        # Record to Khata if credit
        if req.payment_mode.lower() == "credit":
            self.khata_ledger[c_name] = round(self.khata_ledger.get(c_name, 0.0) + final_total, 2)
            self.khata_history.append({
                "type": "CREDIT_SALE",
                "customer": c_name,
                "amount": final_total,
                "bill_id": sale_id,
                "timestamp": ts
            })

        return True, receipt, None

    def settle_khata_due(self, payment: KhataPayment) -> Tuple[bool, float, Optional[str]]:
        c_name = payment.customer_name
        current_due = self.khata_ledger.get(c_name, 0.0)
        if current_due <= 0:
            return False, 0.0, f"No outstanding due found for customer '{c_name}'"

        new_due = max(0.0, round(current_due - payment.amount_paid, 2))
        self.khata_ledger[c_name] = new_due

        ts = datetime.now(timezone.utc).isoformat()
        self.khata_history.append({
            "type": "PAYMENT_RECEIVED",
            "customer": c_name,
            "amount_paid": payment.amount_paid,
            "payment_mode": payment.payment_mode,
            "remaining_due": new_due,
            "timestamp": ts,
            "notes": payment.notes
        })
        return True, new_due, None

    def record_supplier_purchase(self, supplier_name: str, items: List[CartItem]) -> SupplierPurchase:
        total_cost = 0.0
        for ci in items:
            it = self.get_item(ci.sku)
            if it:
                it.stock_quantity += ci.quantity  # Restock inventory
                total_cost += it.cost_price * ci.quantity

        p_id = f"PUR-{uuid.uuid4().hex[:6].upper()}"
        purchase = SupplierPurchase(
            purchase_id=p_id,
            supplier_name=supplier_name,
            items=items,
            total_cost=round(total_cost, 2),
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        self.purchases_history.append(purchase)
        return purchase

    def export_sales_csv(self) -> str:
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(["Sale ID", "Timestamp", "Customer", "Phone", "Payment Mode", "Subtotal", "GST", "Total", "Profit"])
        for s in self.sales_history:
            writer.writerow([s.sale_id, s.timestamp, s.customer_name, s.customer_phone or "", s.payment_mode, s.subtotal, s.gst_amount, s.total_amount, s.total_profit])
        return out.getvalue()

    def export_inventory_csv(self) -> str:
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(["SKU", "Barcode", "Item Name", "Category", "Cost Price", "Selling Price", "Stock Quantity", "Reorder Level", "GST Rate"])
        for it in self.catalog.values():
            writer.writerow([it.sku, it.barcode, it.name, it.category, it.cost_price, it.selling_price, it.stock_quantity, it.reorder_level, it.gst_rate])
        return out.getvalue()

    def export_khata_csv(self) -> str:
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(["Customer Name", "Total Outstanding Due (₹)"])
        for cust, due in self.khata_ledger.items():
            if due > 0:
                writer.writerow([cust, due])
        return out.getvalue()

    def get_daily_summary(self) -> Dict[str, Any]:
        total_rev = sum(s.total_amount for s in self.sales_history)
        total_profit = sum(s.total_profit for s in self.sales_history)
        cash_rev = sum(s.total_amount for s in self.sales_history if s.payment_mode.lower() == "cash")
        upi_rev = sum(s.total_amount for s in self.sales_history if s.payment_mode.lower() == "upi")
        credit_due = sum(s.total_amount for s in self.sales_history if s.payment_mode.lower() == "credit")

        return {
            "total_bills_processed": len(self.sales_history),
            "total_revenue": round(total_rev, 2),
            "total_net_profit": round(total_profit, 2),
            "payment_breakdown": {
                "cash": round(cash_rev, 2),
                "upi": round(upi_rev, 2),
                "credit_khata": round(credit_due, 2)
            },
            "total_outstanding_khata_dues": round(sum(self.khata_ledger.values()), 2),
            "total_purchases_cost": round(sum(p.total_cost for p in self.purchases_history), 2),
            "low_stock_items_count": len(self.list_items(low_stock_only=True))
        }
