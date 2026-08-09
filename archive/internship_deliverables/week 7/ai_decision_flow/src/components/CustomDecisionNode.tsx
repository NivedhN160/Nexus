import React from "react";
import { Handle, Position } from "@xyflow/react";
import { Brain, CheckCircle2, XCircle, Sparkles } from "lucide-react";

interface DecisionNodeProps {
  id: string;
  data: {
    label: string;
    prompt: string;
    isActive?: boolean;
    lastDecision?: "YES" | "NO";
  };
}

export const CustomDecisionNode: React.FC<DecisionNodeProps> = ({ data }) => {
  const { label, prompt, isActive, lastDecision } = data;

  return (
    <div
      className={`min-w-[240px] rounded-xl border-2 bg-slate-900 text-white shadow-xl transition-all duration-300 ${
        isActive
          ? "border-amber-400 shadow-amber-500/30 ring-4 ring-amber-400/20 scale-105"
          : lastDecision === "YES"
          ? "border-emerald-500 shadow-emerald-500/20"
          : lastDecision === "NO"
          ? "border-rose-500 shadow-rose-500/20"
          : "border-slate-700 hover:border-slate-500"
      }`}
    >
      {/* Top Handle for Incoming Connections */}
      <Handle
        type="target"
        position={Position.Top}
        className="w-3 h-3 !bg-slate-400 border-2 border-slate-900"
      />

      <div className="p-4">
        <div className="flex items-center justify-between gap-2 border-b border-slate-800 pb-2 mb-2">
          <div className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-indigo-400 animate-pulse" />
            <span className="font-bold text-sm tracking-wide text-indigo-100">{label}</span>
          </div>
          {isActive ? (
            <span className="px-2 py-0.5 text-xs font-semibold bg-amber-400/20 text-amber-300 border border-amber-400/30 rounded-full flex items-center gap-1 animate-pulse">
              <Sparkles className="w-3 h-3" /> Evaluating...
            </span>
          ) : lastDecision ? (
            <span
              className={`px-2 py-0.5 text-xs font-bold rounded-full flex items-center gap-1 ${
                lastDecision === "YES"
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                  : "bg-rose-500/20 text-rose-300 border border-rose-500/30"
              }`}
            >
              {lastDecision === "YES" ? <CheckCircle2 className="w-3 h-3" /> : <XCircle className="w-3 h-3" />}
              {lastDecision}
            </span>
          ) : null}
        </div>

        <p className="text-xs text-slate-300 bg-slate-950/60 p-2.5 rounded-lg font-mono border border-slate-800/80">
          "{prompt}"
        </p>
      </div>

      {/* Dual Outgoing Handles: YES (Green Left) & NO (Red Right) */}
      <div className="flex justify-between items-center px-4 pb-3 pt-1 border-t border-slate-800 text-[11px] font-bold">
        <div className="flex items-center gap-1 text-emerald-400">
          <span>YES</span>
          <Handle
            type="source"
            position={Position.Bottom}
            id="YES"
            style={{ left: "25%" }}
            className="w-3 h-3 !bg-emerald-500 border-2 border-slate-900"
          />
        </div>

        <div className="flex items-center gap-1 text-rose-400">
          <span>NO</span>
          <Handle
            type="source"
            position={Position.Bottom}
            id="NO"
            style={{ left: "75%" }}
            className="w-3 h-3 !bg-rose-500 border-2 border-slate-900"
          />
        </div>
      </div>
    </div>
  );
};
