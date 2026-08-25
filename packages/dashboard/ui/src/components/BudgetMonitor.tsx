import React from "react";

export const BudgetMonitor: React.FC = () => {
  return (
    <div style={{ padding: "20px", background: "#1e293b", borderRadius: "8px", margin: "16px 0" }}>
      <h2 style={{ fontSize: "1.25rem", marginBottom: "12px", color: "#f59e0b" }}>💰 Token Quotas & Spend Monitor (13 Roles)</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px" }}>
        <div style={{ background: "#0f172a", padding: "12px", borderRadius: "6px" }}>
          <div style={{ fontSize: "0.8rem", color: "#94a3b8" }}>Sprint 1 Compute Spend</div>
          <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#22c55e" }}>$1.42</div>
          <div style={{ fontSize: "0.75rem", color: "#64748b" }}>Monthly Cap Ceiling: $815.00</div>
        </div>
        <div style={{ background: "#0f172a", padding: "12px", borderRadius: "6px" }}>
          <div style={{ fontSize: "0.8rem", color: "#94a3b8" }}>Active Fallback Tier</div>
          <div style={{ fontSize: "1.2rem", fontWeight: "bold", color: "#38bdf8" }}>Primary Cloud (Gemini 2.5)</div>
          <div style={{ fontSize: "0.75rem", color: "#64748b" }}>Circuit Breakers: CLOSED (Healthy)</div>
        </div>
        <div style={{ background: "#0f172a", padding: "12px", borderRadius: "6px" }}>
          <div style={{ fontSize: "0.8rem", color: "#94a3b8" }}>Total Swarm Tokens</div>
          <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#e2e8f0" }}>248,500</div>
          <div style={{ fontSize: "0.75rem", color: "#64748b" }}>Across 13 DSH instances</div>
        </div>
      </div>
    </div>
  );
};
