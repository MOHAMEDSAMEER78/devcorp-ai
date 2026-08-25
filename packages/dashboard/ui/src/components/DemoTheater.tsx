import React from "react";

export const DemoTheater: React.FC = () => {
  return (
    <div style={{ padding: "20px", background: "#1e293b", borderRadius: "8px", margin: "16px 0" }}>
      <h2 style={{ fontSize: "1.25rem", marginBottom: "12px", color: "#a855f7" }}>🎬 Playwright Demo Theater (MP4 Video Replay)</h2>
      <div style={{ position: "relative", background: "#000", height: "360px", borderRadius: "6px", display: "flex", alignItems: "center", justifyContent: "center", border: "1px solid #334155" }}>
        <div style={{ textAlign: "center" }}>
          <p style={{ fontSize: "1.1rem", color: "#e2e8f0" }}>🎥 Automated Journey Walkthrough: Expense Tracker MVP</p>
          <span style={{ fontSize: "0.8rem", color: "#94a3b8" }}>Rendered with visible cursor overlays & click animations</span>
        </div>
      </div>
    </div>
  );
};
