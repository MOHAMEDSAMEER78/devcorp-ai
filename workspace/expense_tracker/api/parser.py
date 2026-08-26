"""Bank Statement Parser & Ingestion Engine."""
import csv
import io
import re
from typing import List, Dict, Any, Tuple


CATEGORIZATION_RULES = {
    "PAYROLL|SALARY|DIRECT DEP|EMPLOYER": ("Income", 0.99),
    "KROGER|WHOLE FOODS|SAFEWAY|TRADER JOE|ALDI|GROCERY|WALMART": ("Groceries", 0.95),
    "SHELL|CHEVRON|EXXON|BP|GAS|MOBIL|AUTO": ("Transport", 0.95),
    "NETFLIX|SPOTIFY|HULU|APPLE.COM|DISNEY|PRIME": ("Subscriptions", 0.98),
    "STARBUCKS|CHIPOTLE|MCDONALD|RESTAURANT|CAFE|DINER|PIZZA": ("Dining", 0.92),
    "ELECTRIC|WATER|UTILITY|COMCAST|VERIZON|AT&T|INTERNET": ("Utilities", 0.95),
    "TARGET|AMAZON|BEST BUY|EBAY|STORE": ("Shopping", 0.90),
}


def categorize_merchant(description: str) -> Tuple[str, float]:
    """Classify transaction merchant string into category with confidence score."""
    desc_upper = description.upper()
    for pattern, (cat, conf) in CATEGORIZATION_RULES.items():
        if re.search(pattern, desc_upper):
            return cat, conf
    return "Other", 0.50


def clean_amount(raw_amount: Any) -> float:
    """Normalize currency string into float decimal."""
    if isinstance(raw_amount, (int, float)):
        return float(raw_amount)
    s = str(raw_amount).replace("$", "").replace(",", "").strip()
    # Handle parenthesized negative numbers e.g. (45.00)
    if s.startswith("(") and s.endswith(")"):
        return -float(s[1:-1])
    return float(s)


def parse_csv_statement(csv_content: str) -> List[Dict[str, Any]]:
    """Parse CSV bank statement content into normalized transaction records."""
    f = io.StringIO(csv_content.strip())
    reader = csv.DictReader(f)

    transactions = []
    for idx, row in enumerate(reader):
        # Normalize column header lookups
        keys = {k.lower().strip(): k for k in row.keys() if k}
        
        date_key = next((keys[k] for k in keys if "date" in k), None)
        desc_key = next((keys[k] for k in keys if "desc" in k or "merchant" in k or "payee" in k), None)
        amt_key = next((keys[k] for k in keys if "amount" in k), None)
        bal_key = next((keys[k] for k in keys if "balance" in k), None)

        if not (date_key and desc_key and amt_key):
            continue

        raw_desc = str(row[desc_key]).strip()
        amount = clean_amount(row[amt_key])
        category, confidence = categorize_merchant(raw_desc)

        transactions.append({
            "id": f"txn-{idx+1:04d}",
            "date": str(row[date_key]).strip(),
            "description": raw_desc,
            "amount": amount,
            "type": "Credit" if amount > 0 else "Debit",
            "category": category,
            "confidence": confidence,
            "balance": clean_amount(row[bal_key]) if bal_key and row[bal_key] else None
        })

    return transactions
