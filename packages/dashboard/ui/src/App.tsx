import React, { useState } from "react";
import { KanbanBoard } from "./components/KanbanBoard";
import { DemoTheater } from "./components/DemoTheater";
import { TrajectoryExplorer } from "./components/TrajectoryExplorer";
import { BudgetMonitor } from "./components/BudgetMonitor";
import { FeedbackConsole } from "./components/FeedbackConsole";

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"overview" | "trajectories" | "budgets">("overview");

  return (
    <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "24px" }}>
      {/* Header */}
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid #334155", paddingBottom: "16px" }}>
        <div>
          <h1 style={{ fontSize: "1.75rem", margin: 0, fontWeight: "bold", color: "#38bdf8" }}>
            🏢 DevCorp AI
          </h1>
          <span style={{ fontSize: "0.85rem", color: "#94a3b8" }}>
            Autonomous Multi-Agent Software Organization — Executive Standup Dashboard
          </span>
        </div>
        <div style={{ display: "flex", gap: "8px" }}>
          <button 
            onClick={() => setActiveTab("overview")}
            style={{ background: activeTab === "overview" ? "#38bdf8" : "#1e293b", color: activeTab === "overview" ? "#0f172a" : "#fff", border: "none", padding: "6px 14px", borderRadius: "4px", cursor: "pointer", fontWeight: 500 }}
          >
            Sprint Overview & Demo
          </button>
          <button 
            onClick={() => setActiveTab("trajectories")}
            style={{ background: activeTab === "trajectories" ? "#38bdf8" : "#1e293b", color: activeTab === "trajectories" ? "#0f172a" : "#fff", border: "none", padding: "6px 14px", borderRadius: "4px", cursor: "pointer", fontWeight: 500 }}
          >
            Trajectory Explorer
          </button>
          <button 
            onClick={() => setActiveTab("budgets")}
            style={{ background: activeTab === "budgets" ? "#38bdf8" : "#1e293b", color: activeTab === "budgets" ? "#0f172a" : "#fff", border: "none", padding: "6px 14px", borderRadius: "4px", cursor: "pointer", fontWeight: 500 }}
          >
            Token Budgets
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ marginTop: "16px" }}>
        {activeTab === "overview" && (
          <>
            <BudgetMonitor />
            <DemoTheater />
            <KanbanBoard />
            <FeedbackConsole />
          </>
        )}

        {activeTab === "trajectories" && (
          <>
            <TrajectoryExplorer />
            <KanbanBoard />
          </>
        )}

        {activeTab === "budgets" && (
          <>
            <BudgetMonitor />
            <FeedbackConsole />
          </>
        )}
      </main>
    </div>
  );
};

export default App;
