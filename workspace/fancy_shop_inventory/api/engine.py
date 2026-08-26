"""Core Inventory, POS Checkout & Khata Ledger Engine."""
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from .models import Item, CartItem, CheckoutRequest, SaleReceipt, KhataCreditEntry


class ShopInventoryEngine:
    def __init__(self):
        self.catalog: Dict[str, Item] = {}
        self.sales_history: List[SaleReceipt] = []
        self.khata_ledger: Dict[str, float] = {}

    def add_or_update_item(self, item: Item) -> Item:
        self.catalog[item.sku] = item
        return item

    def get_item(self, sku: str) -> Optional[Item]:
        return self.catalog.get(sku)

    def list_items(self, low_stock_only: bool = False) -> List[Item]:
        items = list(self.catalog.values())
        if low_stock_only:
            return [it for it in items if it.stock_quantity <= it.reorder_level]
        return items

    def process_checkout(self, req: CheckoutRequest) -> Tuple[bool, Optional[SaleReceipt], Optional[str]]:
        for cart_item in req.items:
            it = self.get_item(cart_item.sku)
            if not it:
                return False, None, f"Item SKU '{cart_item.sku}' not found in catalog"
            if it.stock_quantity < cart_item.quantity:
                return False, None, f"Insufficient stock for '{it.name}' (Available: {it.stock_quantity}, Requested: {cart_item.quantity})"

        items_sold = []
        subtotal = 0.0
        cost_total = 0.0

        for cart_item in req.items:
            it = self.catalog[cart_item.sku]
            line_subtotal = it.selling_price * cart_item.quantity
            line_cost = it.cost_price * cart_item.quantity

            subtotal += line_subtotal
            cost_total += line_cost
            it.stock_quantity -= cart_item.quantity

            items_sold.append({
                "sku": it.sku,
                "name": it.name,
                "quantity": cart_item.quantity,
                "unit_price": it.selling_price,
                "line_total": round(line_subtotal, 2)
            })

        discount = round(subtotal * (req.discount_percent / 100.0), 2)
        total_amount = round(subtotal - discount, 2)
        total_profit = round(total_amount - cost_total, 2)

        receipt = SaleReceipt(
            sale_id=f"BILL-{uuid.uuid4().hex[:6].upper()}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            customer_name=req.customer_name or "Walk-in Customer",
            payment_mode=req.payment_mode,
            items_sold=items_sold,
            subtotal=round(subtotal, 2),
            discount_applied=discount,
            total_amount=total_amount,
            total_profit=total_profit
        )

        self.sales_history.append(receipt)

        if req.payment_mode.lower() == "credit":
            c_name = req.customer_name or "Unknown"
            self.khata_ledger[c_name] = round(self.khata_ledger.get(c_name, 0.0) + total_amount, 2)

        return True, receipt, None

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
            "low_stock_items_count": len(self.list_items(low_stock_only=True))
        }
