"""Sprint 2 Expanded Data Models: GST, Multi-Item Cart, Khata Repayment, Suppliers."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class Item(BaseModel):
    sku: str
    name: str
    category: str = "General Fancy"
    barcode: Optional[str] = None
    cost_price: float
    selling_price: float
    stock_quantity: int
    reorder_level: int = 5
    gst_rate: float = 0.0  # e.g. 0%, 5%, 12%, 18%
    supplier_name: Optional[str] = "Local Wholesale"


class CartItem(BaseModel):
    sku: str
    quantity: int
    discount_percent: float = 0.0


class CheckoutRequest(BaseModel):
    customer_name: Optional[str] = "Walk-in Customer"
    customer_phone: Optional[str] = None
    payment_mode: str = "Cash"  # Cash, UPI, Credit (Khata)
    items: List[CartItem]
    apply_gst: bool = False
    overall_discount: float = 0.0


class SaleReceipt(BaseModel):
    sale_id: str
    timestamp: str
    customer_name: str
    customer_phone: Optional[str] = None
    payment_mode: str
    items_sold: List[Dict[str, Any]]
    subtotal: float
    discount_applied: float
    gst_amount: float
    total_amount: float
    total_profit: float
    whatsapp_share_text: str


class KhataPayment(BaseModel):
    customer_name: str
    amount_paid: float
    payment_mode: str = "Cash"  # Cash / UPI
    notes: Optional[str] = None


class SupplierPurchase(BaseModel):
    purchase_id: str
    supplier_name: str
    items: List[CartItem]
    total_cost: float
    timestamp: str
