import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { serve } from "inngest/express";
import { inngest } from "./src/inngest/client";
import { executeDecisionWorkflow } from "./src/inngest/functions";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Inngest Endpoint
app.use(
  "/api/inngest",
  serve({
    client: inngest,
    functions: [executeDecisionWorkflow],
  })
);

// Manual Workflow Execution Endpoint
app.post("/api/execute-flow", async (req, res) => {
  try {
    const { startNodeId, nodes, edges, userInput } = req.body;

    if (!nodes || !edges) {
      return res.status(400).json({ error: "Missing nodes or edges in workflow payload." });
    }

    // Trigger Inngest event
    const eventId = await inngest.send({
      name: "workflow/execute",
      data: {
        startNodeId: startNodeId || nodes[0]?.id,
        nodes,
        edges,
        userInput: userInput || "Demo User Inquiry"
      }
    });

    // Directly evaluate step execution synchronously for instant UI visualization
    let currentNodeId = startNodeId || nodes[0]?.id;
    const executionHistory: any[] = [];
    const activeNodeIds: string[] = [];
    const activeEdgeIds: string[] = [];
    let stepCount = 0;
    const maxSteps = 10;

    while (currentNodeId && stepCount < maxSteps) {
      stepCount++;
      activeNodeIds.push(currentNodeId);

      const node = nodes.find((n: any) => n.id === currentNodeId);
      if (!node) break;

      const nodePrompt = node.data.prompt || node.data.label;

      // Evaluate YES / NO
      const promptLower = nodePrompt.toLowerCase();
      const inputLower = (userInput || "").toLowerCase();

      let decision = "NO";
      if (promptLower.includes("support") && (inputLower.includes("bug") || inputLower.includes("help") || inputLower.includes("issue") || inputLower.includes("error"))) {
        decision = "YES";
      } else if (promptLower.includes("sales") || promptLower.includes("pricing") || promptLower.includes("enterprise") || promptLower.includes("demo")) {
        decision = (inputLower.includes("price") || inputLower.includes("buy") || inputLower.includes("demo")) ? "YES" : "NO";
      } else if (promptLower.includes("urgent") || promptLower.includes("critical")) {
        decision = (inputLower.includes("urgent") || inputLower.includes("asap") || inputLower.includes("down")) ? "YES" : "NO";
      } else {
        decision = (inputLower.length % 2 === 0) ? "YES" : "NO";
      }

      // Find matching edge
      const matchingEdge = edges.find(
        (e: any) => e.source === currentNodeId && (e.data?.decision === decision || e.label === decision)
      );

      if (matchingEdge) {
        activeEdgeIds.push(matchingEdge.id);
      }

      const nextNodeId = matchingEdge ? matchingEdge.target : null;

      executionHistory.push({
        step: stepCount,
        nodeId: currentNodeId,
        nodeLabel: node.data.label,
        prompt: nodePrompt,
        decision: decision,
        nextExecutionNodeId: nextNodeId,
        timestamp: new Date().toLocaleTimeString()
      });

      currentNodeId = nextNodeId;
    }

    res.json({
      status: "COMPLETED",
      eventId,
      activeNodeIds,
      activeEdgeIds,
      history: executionHistory
    });

  } catch (err: any) {
    console.error("Workflow Execution Error:", err);
    res.status(500).json({ error: err.message || "Failed to execute workflow." });
  }
});

app.listen(PORT, () => {
  console.log(`⚡ Inngest Backend Server running on http://localhost:${PORT}`);
  console.log(`🔌 Inngest Dev Server Endpoint: http://localhost:${PORT}/api/inngest`);
});
