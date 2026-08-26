"""FastAPI Backend Server for Bank Statement Expense Tracker."""
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .parser import parse_csv_statement, categorize_merchant

app = FastAPI(title="Bank Statement Expense Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory transaction storage
IN_MEMORY_TRANSACTIONS: List[Dict[str, Any]] = []


class StatementUploadResponse(BaseModel):
    status: str
    filename: str
    transactions_extracted: int
    total_inflow: float
    total_outflow: float


@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "expense-tracker-api"}


@app.post("/api/statements/upload", response_model=StatementUploadResponse)
async def upload_statement(file: UploadFile = File(...)):
    """Upload and parse CSV bank statement."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=422, detail="Only CSV statement files are currently supported")

    content = (await file.read()).decode("utf-8")
    txns = parse_csv_statement(content)
    if not txns:
        raise HTTPException(status_code=422, detail="No valid transactions could be parsed from file")

    global IN_MEMORY_TRANSACTIONS
    IN_MEMORY_TRANSACTIONS = txns

    inflow = sum(t["amount"] for t in txns if t["amount"] > 0)
    outflow = abs(sum(t["amount"] for t in txns if t["amount"] < 0))

    return StatementUploadResponse(
        status="SUCCESS",
        filename=file.filename,
        transactions_extracted=len(txns),
        total_inflow=round(inflow, 2),
        total_outflow=round(outflow, 2)
    )


@app.get("/api/transactions")
def list_transactions(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List extracted transactions with optional category filter."""
    if category:
        return [t for t in IN_MEMORY_TRANSACTIONS if t["category"].lower() == category.lower()]
    return IN_MEMORY_TRANSACTIONS


@app.get("/api/analytics/summary")
def get_analytics_summary() -> Dict[str, Any]:
    """Compute aggregate totals and spending breakdown by category."""
    txns = IN_MEMORY_TRANSACTIONS
    inflow = sum(t["amount"] for t in txns if t["amount"] > 0)
    outflow = abs(sum(t["amount"] for t in txns if t["amount"] < 0))

    category_breakdown: Dict[str, float] = {}
    for t in txns:
        if t["amount"] < 0:
            cat = t["category"]
            category_breakdown[cat] = round(category_breakdown.get(cat, 0.0) + abs(t["amount"]), 2)

    return {
        "total_transactions": len(txns),
        "total_inflow": round(inflow, 2),
        "total_outflow": round(outflow, 2),
        "net_savings": round(inflow - outflow, 2),
        "category_breakdown": category_breakdown
    }
