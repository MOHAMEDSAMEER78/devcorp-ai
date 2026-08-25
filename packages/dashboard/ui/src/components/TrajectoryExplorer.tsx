import React, { useState } from "react";

export const TrajectoryExplorer: React.FC = () => {
  const [selectedRole, setSelectedRole] = useState("backend_engineer");

  const sampleEvents = [
    { step: 1, action: "ingest_ticket", details: "Ingested TSK-001 (PDF/CSV Parser)", time: "18:00:00" },
    { step: 2, action: "mcp_tool_call", tool: "filesystem.read_file", details: "Read OpenAPI & DB contracts", time: "18:00:05" },
    { step: 3, action: "code_generation", files: ["api/parser.py", "tests/test_parser.py"], time: "18:00:20" },
    { step: 4, action: "sandbox_execution", tool: "test_runner.run_tests", details: "38/38 tests passed", time: "18:00:35" }
  ];

  return (
    <div style={{ padding: "20px", background: "#1e293b", borderRadius: "8px", margin: "16px 0" }}>
      <h2 style={{ fontSize: "1.25rem", marginBottom: "12px", color: "#22c55e" }}>🔍 DSH Agent Trajectory Explorer</h2>
      <div style={{ marginBottom: "12px" }}>
        <label style={{ fontSize: "0.9rem", marginRight: "8px", color: "#94a3b8" }}>Select Agent Instance:</label>
        <select 
          value={selectedRole} 
          onChange={(e) => setSelectedRole(e.target.value)}
          style={{ background: "#0f172a", color: "#fff", padding: "6px 12px", borderRadius: "4px", border: "1px solid #334155" }}
        >
          <option value="product_manager">Product Manager</option>
          <option value="system_architect">System Architect</option>
          <option value="backend_engineer">Backend Engineer</option>
          <option value="frontend_engineer">Frontend Engineer</option>
          <option value="qa_reviewer">QA Reviewer</option>
          <option value="demo_release">Demo & Release Agent</option>
        </select>
      </div>
      <div style={{ background: "#0f172a", padding: "12px", borderRadius: "6px", fontFamily: "monospace", fontSize: "0.85rem" }}>
        {sampleEvents.map((e) => (
          <div key={e.step} style={{ padding: "6px 0", borderBottom: "1px solid #1e293b" }}>
            <span style={{ color: "#38bdf8" }}>[{e.time}]</span> <strong style={{ color: "#e2e8f0" }}>Step {e.step} ({e.action}):</strong> {e.details || JSON.stringify(e.files || e.tool)}
          </div>
        ))}
      </div>
    </div>
  );
};
