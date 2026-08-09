import React, { useState, useCallback } from "react";
import {
  ReactFlow,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  type Connection,
  type Edge,
  type Node,
  BackgroundVariant
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import { CustomDecisionNode } from "./components/CustomDecisionNode";
import {
  Play,
  Plus,
  Download,
  Upload,
  Sparkles,
  CheckCircle,
  Sliders,
  Terminal,
  Activity,
  Layers
} from "lucide-react";

const nodeTypes = {
  decisionNode: CustomDecisionNode,
};

// Initial Pre-Configured Workflow Graph
const initialNodes: Node[] = [
  {
    id: "node-1",
    type: "decisionNode",
    position: { x: 300, y: 50 },
    data: {
      label: "Support Request Check",
      prompt: "Is this a support request or bug report?"
    }
  },
  {
    id: "node-2",
    type: "decisionNode",
    position: { x: 100, y: 250 },
    data: {
      label: "Urgent Outage Check",
      prompt: "Is this a critical system outage or urgent issue?"
    }
  },
  {
    id: "node-3",
    type: "decisionNode",
    position: { x: 500, y: 250 },
    data: {
      label: "Enterprise Sales Check",
      prompt: "Is this an enterprise pricing or sales inquiry?"
    }
  },
  {
    id: "node-4",
    type: "decisionNode",
    position: { x: 50, y: 450 },
    data: {
      label: "L3 PagerDuty Escalation",
      prompt: "Trigger L3 On-Call PagerDuty Alert?"
    }
  },
  {
    id: "node-5",
    type: "decisionNode",
    position: { x: 250, y: 450 },
    data: {
      label: "Standard Helpdesk Ticket",
      prompt: "Create standard support ticket in Zendesk?"
    }
  },
  {
    id: "node-6",
    type: "decisionNode",
    position: { x: 500, y: 450 },
    data: {
      label: "VIP Sales Rep Assignment",
      prompt: "Assign dedicated Account Executive?"
    }
  }
];

const initialEdges: Edge[] = [
  {
    id: "e1-2",
    source: "node-1",
    target: "node-2",
    sourceHandle: "YES",
    label: "YES",
    style: { stroke: "#10B981", strokeWidth: 3 },
    animated: true,
    data: { decision: "YES" }
  },
  {
    id: "e1-3",
    source: "node-1",
    target: "node-3",
    sourceHandle: "NO",
    label: "NO",
    style: { stroke: "#EF4444", strokeWidth: 3 },
    animated: true,
    data: { decision: "NO" }
  },
  {
    id: "e2-4",
    source: "node-2",
    target: "node-4",
    sourceHandle: "YES",
    label: "YES",
    style: { stroke: "#10B981", strokeWidth: 3 },
    animated: true,
    data: { decision: "YES" }
  },
  {
    id: "e2-5",
    source: "node-2",
    target: "node-5",
    sourceHandle: "NO",
    label: "NO",
    style: { stroke: "#EF4444", strokeWidth: 3 },
    animated: true,
    data: { decision: "NO" }
  },
  {
    id: "e3-6",
    source: "node-3",
    target: "node-6",
    sourceHandle: "YES",
    label: "YES",
    style: { stroke: "#10B981", strokeWidth: 3 },
    animated: true,
    data: { decision: "YES" }
  }
];

export function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const [userInput, setUserInput] = useState("Our database is down and returning HTTP 500 error! Urgent help needed!");
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [editingPrompt, setEditingPrompt] = useState("");
  const [editingLabel, setEditingLabel] = useState("");
  const [isExecuting, setIsExecuting] = useState(false);
  const [logs, setLogs] = useState<any[]>([]);
  const [activeEdgeIds, setActiveEdgeIds] = useState<string[]>([]);

  // Connect Nodes with YES/NO edge styling
  const onConnect = useCallback(
    (params: Connection) => {
      const isYes = params.sourceHandle === "YES";
      const newEdge: Edge = {
        ...params,
        id: `e-${params.source}-${params.target}-${params.sourceHandle}`,
        label: isYes ? "YES" : "NO",
        style: { stroke: isYes ? "#10B981" : "#EF4444", strokeWidth: 3 },
        animated: true,
        data: { decision: isYes ? "YES" : "NO" }
      };
      setEdges((eds) => addEdge(newEdge, eds));
    },
    [setEdges]
  );

  // Add New Decision Node
  const handleAddNode = () => {
    const newId = `node-${nodes.length + 1}`;
    const newNode: Node = {
      id: newId,
      type: "decisionNode",
      position: { x: 300 + nodes.length * 20, y: 150 + nodes.length * 30 },
      data: {
        label: `Custom Node ${nodes.length + 1}`,
        prompt: "Does this meet custom AI criteria?"
      }
    };
    setNodes((nds) => [...nds, newNode]);
  };

  // Node Click -> Open Edit Sidebar
  const onNodeClick = (_: React.MouseEvent, node: Node) => {
    setSelectedNodeId(node.id);
    setEditingLabel((node.data.label as string) || "");
    setEditingPrompt((node.data.prompt as string) || "");
  };

  // Save Edited Node Prompt
  const handleSaveNodeEdit = () => {
    if (!selectedNodeId) return;
    setNodes((nds) =>
      nds.map((n) => {
        if (n.id === selectedNodeId) {
          return {
            ...n,
            data: {
              ...n.data,
              label: editingLabel,
              prompt: editingPrompt
            }
          };
        }
        return n;
      })
    );
    setSelectedNodeId(null);
  };

  // Execute Workflow via Inngest Engine API
  const handleExecuteWorkflow = async () => {
    setIsExecuting(true);
    setLogs([]);
    setActiveEdgeIds([]);

    // Reset node visual highlights
    setNodes((nds) => nds.map((n) => ({ ...n, data: { ...n.data, isActive: false, lastDecision: undefined } })));

    try {
      const response = await fetch("http://localhost:3001/api/execute-flow", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          startNodeId: nodes[0]?.id,
          nodes,
          edges,
          userInput
        })
      });

      const data = await response.json();
      setLogs(data.history || []);
      setActiveEdgeIds(data.activeEdgeIds || []);

      // Highlight executed path step-by-step
      if (data.history) {
        for (const item of data.history) {
          setNodes((nds) =>
            nds.map((n) => {
              if (n.id === item.nodeId) {
                return {
                  ...n,
                  data: {
                    ...n.data,
                    isActive: false,
                    lastDecision: item.decision
                  }
                };
              }
              return n;
            })
          );
        }
      }

    } catch (err) {
      console.error("Execution Failed:", err);
    } finally {
      setIsExecuting(false);
    }
  };

  // Export Workflow to JSON
  const handleExportJSON = () => {
    const flowData = JSON.stringify({ nodes, edges }, null, 2);
    const blob = new Blob([flowData], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "ai-decision-workflow.json";
    link.click();
  };

  // Import Workflow from JSON
  const handleImportJSON = (event: React.ChangeEvent<HTMLInputElement>) => {
    const fileReader = new FileReader();
    if (event.target.files && event.target.files[0]) {
      fileReader.readAsText(event.target.files[0], "UTF-8");
      fileReader.onload = (e) => {
        try {
          const parsed = JSON.parse(e.target?.result as string);
          if (parsed.nodes && parsed.edges) {
            setNodes(parsed.nodes);
            setEdges(parsed.edges);
          }
        } catch (err) {
          alert("Invalid workflow JSON file!");
        }
      };
    }
  };

  return (
    <div className="flex h-screen w-screen bg-slate-950 text-slate-100 font-sans overflow-hidden">
      
      {/* Sidebar Controls & Panels */}
      <div className="w-96 border-r border-slate-800 bg-slate-900/90 flex flex-col z-10 shadow-2xl backdrop-blur-md">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-amber-400 animate-pulse" />
            <h1 className="text-lg font-bold tracking-tight bg-gradient-to-r from-amber-400 via-indigo-300 to-emerald-400 bg-clip-text text-transparent">
              AI Decision Flow
            </h1>
          </div>
          <span className="px-2 py-0.5 text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded-full">
            Inngest + React Flow
          </span>
        </div>

        {/* User Input Context */}
        <div className="p-4 border-b border-slate-800">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1 mb-2">
            <Activity className="w-3.5 h-3.5 text-indigo-400" />
            Test User Input Context
          </label>
          <textarea
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            className="w-full h-24 p-3 text-xs bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:border-indigo-500 resize-none font-mono"
            placeholder="Type a customer query or incident message..."
          />

          <button
            onClick={handleExecuteWorkflow}
            disabled={isExecuting}
            className="w-full mt-3 py-2.5 px-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold rounded-lg shadow-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50 cursor-pointer"
          >
            <Play className={`w-4 h-4 ${isExecuting ? "animate-spin" : ""}`} />
            {isExecuting ? "Executing via Inngest..." : "Run AI Workflow Execution"}
          </button>
        </div>

        {/* Toolbar & Canvas Controls */}
        <div className="p-4 border-b border-slate-800 flex items-center gap-2 flex-wrap">
          <button
            onClick={handleAddNode}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-md border border-slate-700 flex items-center gap-1 cursor-pointer"
          >
            <Plus className="w-3.5 h-3.5 text-emerald-400" /> Add Node
          </button>

          <button
            onClick={handleExportJSON}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-md border border-slate-700 flex items-center gap-1 cursor-pointer"
          >
            <Download className="w-3.5 h-3.5 text-sky-400" /> Export JSON
          </button>

          <label className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-md border border-slate-700 flex items-center gap-1 cursor-pointer">
            <Upload className="w-3.5 h-3.5 text-purple-400" /> Import JSON
            <input type="file" accept=".json" onChange={handleImportJSON} className="hidden" />
          </label>
        </div>

        {/* Node Prompt Editor Modal */}
        {selectedNodeId && (
          <div className="p-4 border-b border-slate-800 bg-slate-950/80 animate-fadeIn">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-amber-400 flex items-center gap-1">
                <Sliders className="w-3.5 h-3.5" /> Edit Selected Node ({selectedNodeId})
              </span>
              <button
                onClick={() => setSelectedNodeId(null)}
                className="text-slate-400 hover:text-white text-xs font-bold"
              >
                ✕
              </button>
            </div>

            <div className="space-y-2">
              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase">Node Title</label>
                <input
                  type="text"
                  value={editingLabel}
                  onChange={(e) => setEditingLabel(e.target.value)}
                  className="w-full p-2 text-xs bg-slate-900 border border-slate-800 rounded text-slate-200"
                />
              </div>

              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase">AI Decision Prompt</label>
                <textarea
                  value={editingPrompt}
                  onChange={(e) => setEditingPrompt(e.target.value)}
                  className="w-full h-16 p-2 text-xs bg-slate-900 border border-slate-800 rounded text-slate-200 resize-none font-mono"
                />
              </div>

              <button
                onClick={handleSaveNodeEdit}
                className="w-full py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded flex items-center justify-center gap-1 cursor-pointer"
              >
                <CheckCircle className="w-3.5 h-3.5" /> Save Node Prompt
              </button>
            </div>
          </div>
        )}

        {/* Real-time Execution Logs Panel */}
        <div className="flex-1 p-4 overflow-y-auto font-mono text-xs">
          <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
            <span className="font-bold text-slate-300 flex items-center gap-1.5">
              <Terminal className="w-4 h-4 text-emerald-400" /> Execution History
            </span>
            <span className="text-[10px] text-slate-500 font-bold">{logs.length} Steps Executed</span>
          </div>

          {logs.length === 0 ? (
            <div className="text-slate-600 text-center py-8">
              No active execution. Click "Run AI Workflow Execution" to trigger Inngest step evaluation.
            </div>
          ) : (
            <div className="space-y-3">
              {logs.map((log, idx) => (
                <div key={idx} className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-indigo-400 font-bold">Step {log.step}: {log.nodeLabel}</span>
                    <span className="text-slate-500">{log.timestamp}</span>
                  </div>
                  <p className="text-slate-400 text-[10px]">"{log.prompt}"</p>
                  <div className="flex items-center gap-2 pt-1">
                    <span className="text-slate-500 text-[10px]">Result:</span>
                    <span
                      className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                        log.decision === "YES"
                          ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                          : "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                      }`}
                    >
                      {log.decision}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Main React Flow Canvas */}
      <div className="flex-1 h-full w-full relative">
        <ReactFlow
          nodes={nodes}
          edges={edges.map((e) => ({
            ...e,
            style: activeEdgeIds.includes(e.id)
              ? { stroke: "#F59E0B", strokeWidth: 4 }
              : e.style
          }))}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          nodeTypes={nodeTypes}
          fitView
          className="bg-slate-950"
        >
          <Background color="#334155" variant={BackgroundVariant.Dots} gap={20} size={1} />
          <Controls className="!bg-slate-900 !border-slate-800 !text-slate-300 fill-slate-300" />
        </ReactFlow>

        {/* Overlay Legend */}
        <div className="absolute top-4 right-4 bg-slate-900/80 backdrop-blur-md border border-slate-800 p-3 rounded-xl shadow-xl text-xs space-y-1.5">
          <div className="font-bold text-slate-300 flex items-center gap-1 mb-1">
            <Layers className="w-3.5 h-3.5 text-amber-400" /> Path Legend
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-1 bg-emerald-500 rounded"></div>
            <span className="text-slate-400">YES Path</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-1 bg-rose-500 rounded"></div>
            <span className="text-slate-400">NO Path</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-1 bg-amber-400 rounded animate-pulse"></div>
            <span className="text-amber-300 font-semibold">Active Execution Path</span>
          </div>
        </div>
      </div>

    </div>
  );
}

export default App;
