import { inngest } from "./client";
import OpenAI from "openai";

const getApiKey = () => {
  if (typeof process !== "undefined" && process.env) {
    return process.env.OPENAI_API_KEY || "mock-key";
  }
  return "mock-key";
};

const openai = new OpenAI({
  apiKey: getApiKey(),
});

export const executeDecisionWorkflow = (inngest.createFunction as any)(
  { id: "execute-ai-decision-workflow", name: "Execute AI Decision Workflow" },
  { event: "workflow/execute" },
  async ({ event, step }: { event: any; step: any }) => {
    const { startNodeId, nodes, edges, userInput } = event.data as any;

    let currentNodeId = startNodeId;
    const executionHistory: any[] = [];
    let stepCount = 0;
    const maxSteps = 10;

    while (currentNodeId && stepCount < maxSteps) {
      stepCount++;
      const node = nodes.find((n: any) => n.id === currentNodeId);
      if (!node) break;

      const nodePrompt = node.data.prompt || node.data.label;

      const decisionResult = await step.run(
        `evaluate-node-${currentNodeId}`,
        async () => {
          const apiKey = getApiKey();
          if (apiKey && !apiKey.includes("mock")) {
            try {
              const response = await openai.chat.completions.create({
                model: "gpt-4o-mini",
                messages: [
                  {
                    role: "system",
                    content: "You are an AI decision node in a workflow. Analyze the prompt and user input carefully. Answer ONLY 'YES' or 'NO'. No other words."
                  },
                  {
                    role: "user",
                    content: `Decision Question: "${nodePrompt}"\nUser Input Context: "${userInput}"`
                  }
                ],
                temperature: 0.1,
              });

              const answer = response.choices[0]?.message?.content?.trim().toUpperCase();
              return answer === "YES" ? "YES" : "NO";
            } catch (err) {
              console.warn("OpenAI API call failed, falling back to rule evaluator:", err);
            }
          }

          const promptLower = nodePrompt.toLowerCase();
          const inputLower = (userInput || "").toLowerCase();

          if (promptLower.includes("support") && (inputLower.includes("bug") || inputLower.includes("help") || inputLower.includes("issue") || inputLower.includes("error"))) {
            return "YES";
          }
          if (promptLower.includes("sales") || promptLower.includes("pricing") || promptLower.includes("enterprise") || promptLower.includes("demo")) {
            return inputLower.includes("price") || inputLower.includes("buy") || inputLower.includes("demo") ? "YES" : "NO";
          }
          if (promptLower.includes("urgent") || promptLower.includes("critical")) {
            return inputLower.includes("urgent") || inputLower.includes("asap") || inputLower.includes("down") ? "YES" : "NO";
          }

          return (inputLower.length % 2 === 0) ? "YES" : "NO";
        }
      );

      const decision = decisionResult;

      const matchingEdge = edges.find(
        (e: any) => e.source === currentNodeId && (e.data?.decision === decision || e.label === decision)
      );

      const nextNodeId = matchingEdge ? matchingEdge.target : null;

      executionHistory.push({
        step: stepCount,
        nodeId: currentNodeId,
        nodeLabel: node.data.label,
        prompt: nodePrompt,
        decision: decision,
        nextExecutionNodeId: nextNodeId,
        timestamp: new Date().toISOString()
      });

      currentNodeId = nextNodeId;
    }

    return {
      status: "COMPLETED",
      stepsExecuted: stepCount,
      history: executionHistory,
      finalNodeId: executionHistory[executionHistory.length - 1]?.nodeId
    };
  }
);
