"""Data Models & Catalog Storage for Shop Inventory."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class Item(BaseModel):
    sku: str
    name: str
    category: str = "General Fancy"
    cost_price: float
    selling_price: float
    stock_quantity: int
    reorder_level: int = 5


class CartItem(BaseModel):
    sku: str
    quantity: int


class CheckoutRequest(BaseModel):
    customer_name: Optional[str] = "Walk-in Customer"
    payment_mode: str = "Cash"  # Cash, UPI, Credit
    items: List[CartItem]
    discount_percent: float = 0.0


class SaleReceipt(BaseModel):
    sale_id: str
    timestamp: str
    customer_name: str
    payment_mode: str
    items_sold: List[Dict[str, Any]]
    subtotal: float
    discount_applied: float
    total_amount: float
    total_profit: float


class KhataCreditEntry(BaseModel):
    customer_name: str
    amount_due: float
    notes: Optional[str] = None
