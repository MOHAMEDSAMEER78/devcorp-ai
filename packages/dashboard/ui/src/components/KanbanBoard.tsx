import React, { useEffect, useState } from "react";

export const KanbanBoard: React.FC = () => {
  const [columns, setColumns] = useState<Record<string, string[]>>({
    backlog: ["TSK-002: Analytics Charts"],
    in_progress: ["TSK-001: PDF/CSV Parser", "TSK-003: Design System"],
    in_review: [],
    done: [],
    blocked: []
  });

  return (
    <div style={{ padding: "20px", background: "#1e293b", borderRadius: "8px", margin: "16px 0" }}>
      <h2 style={{ fontSize: "1.25rem", marginBottom: "16px", color: "#38bdf8" }}>📋 Active Virtual Kanban (Sprint 1)</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "12px" }}>
        {Object.entries(columns).map(([col, items]) => (
          <div key={col} style={{ background: "#0f172a", padding: "12px", borderRadius: "6px", border: "1px solid #334155" }}>
            <h3 style={{ fontSize: "0.9rem", textTransform: "uppercase", color: "#94a3b8", marginBottom: "8px" }}>
              {col.replace("_", " ")} ({items.length})
            </h3>
            {items.map((item, idx) => (
              <div key={idx} style={{ background: "#1e293b", padding: "8px", borderRadius: "4px", marginBottom: "6px", fontSize: "0.85rem", borderLeft: "3px solid #38bdf8" }}>
                {item}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};
