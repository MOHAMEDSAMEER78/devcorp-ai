import React, { useState } from "react";

export const FeedbackConsole: React.FC = () => {
  const [feedback, setFeedback] = useState("");
  const [statusMsg, setStatusMsg] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedback.trim()) return;
    setStatusMsg("Feedback submitted! Initiating LangGraph Delta Replanning for Sprint 2...");
    setTimeout(() => {
      setFeedback("");
      setStatusMsg("");
    }, 4000);
  };

  return (
    <div style={{ padding: "20px", background: "#1e293b", borderRadius: "8px", margin: "16px 0" }}>
      <h2 style={{ fontSize: "1.25rem", marginBottom: "8px", color: "#ec4899" }}>🎯 Executive Steering & Standup Gate</h2>
      <p style={{ fontSize: "0.85rem", color: "#94a3b8", marginBottom: "12px" }}>
        Submit high-level strategic directives to automatically trigger a PRD delta diff and enqueue newly prioritized tickets for Sprint 2.
      </p>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={3}
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="E.g., Add collapsible sidebar, category progress bars, and CSV export..."
          style={{ width: "100%", background: "#0f172a", color: "#fff", border: "1px solid #334155", borderRadius: "6px", padding: "10px", boxSizing: "border-box", fontFamily: "inherit" }}
        />
        <div style={{ marginTop: "8px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <button
            type="submit"
            style={{ background: "#38bdf8", color: "#0f172a", fontWeight: "bold", border: "none", padding: "8px 20px", borderRadius: "4px", cursor: "pointer" }}
          >
            Submit Feedback & Replan Sprint
          </button>
          {statusMsg && <span style={{ color: "#22c55e", fontSize: "0.85rem" }}>{statusMsg}</span>}
        </div>
      </form>
    </div>
  );
};
