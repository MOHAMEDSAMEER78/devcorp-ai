# Reference Product Vision: Bank Statement Expense Tracker

## Executive Concept:
Build a modern, personal expense tracking web application that allows users to upload bank statements in multi-page PDF or CSV formats, automatically parses and extracts all transaction line items, categorizes transactions (Groceries, Utilities, Dining, Transport, Subscriptions, Income) using rule-based and LLM heuristics, and renders an interactive spending dashboard with category breakdown charts and budget threshold alerts.

## Target Application Features:
1. **Authentication**: User sign-in with email/password and OAuth2 simulation.
2. **Statement Upload Pipeline**:
   - Drag-and-drop file upload zone.
   - Support for multi-page bank PDF statements and CSV exports.
   - File validation (size limit: 50MB, MIME type verification).
3. **Transaction Extraction Engine**:
   - Extraction of Date, Description/Merchant, Amount (Debit/Credit), and Running Balance.
   - Normalization of bank-specific transaction formats.
4. **Smart Categorization Service**:
   - Heuristic and pattern-matching rules for common merchants (e.g., "KROGER" -> Groceries, "SHELL" -> Transport).
   - Fallback to "Uncategorized" with manual override and category-learning capability.
5. **Analytics & Spending Dashboard**:
   - Total monthly outflow vs inflow summary cards.
   - Interactive category spending breakdown pie chart.
   - 6-month spending trend bar chart.
   - Budget progress bars with warning alerts at >80% utilization.
6. **Data Export**:
   - Export structured parsed transactions to JSON and CSV.
