"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { AgentTraceEntry } from "@/types";
import { ChevronDown, ChevronRight, CheckCircle2, Clock } from "lucide-react";

interface AgentPipelineProps {
  trace: AgentTraceEntry[];
}

const AGENT_COLORS: Record<string, string> = {
  "Language Agent": "#8b5cf6",
  "Retriever Agent": "#3b82f6",
  "Answer Agent": "#06b6d4",
  "Grounding Agent": "#f59e0b",
  "Confidence Scorer": "#22c55e",
  "Explainer Agent": "#ec4899",
};

export default function AgentPipeline({ trace }: AgentPipelineProps) {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
  const totalDuration = trace.reduce((sum, t) => sum + t.duration_ms, 0);

  return (
    <div className="space-y-1">
      {/* Timeline header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2 text-white/30 text-xs">
          <Clock className="w-3.5 h-3.5" />
          <span>Total: {totalDuration.toFixed(0)}ms</span>
        </div>
        <span className="text-white/20 text-[10px]">{trace.length} agents</span>
      </div>

      {/* Agent nodes */}
      {trace.map((entry, i) => {
        const color = AGENT_COLORS[entry.agent] || "#6b7280";
        const isExpanded = expandedIndex === i;
        const isLast = i === trace.length - 1;

        return (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: i * 0.08 }}
          >
            {/* Node */}
            <button
              onClick={() => setExpandedIndex(isExpanded ? null : i)}
              className="w-full flex items-center gap-3 py-2.5 px-3 rounded-xl hover:bg-white/[0.03] transition-colors text-left"
            >
              {/* Timeline dot + line */}
              <div className="flex flex-col items-center flex-shrink-0">
                <div
                  className="w-3 h-3 rounded-full border-2"
                  style={{
                    borderColor: color,
                    backgroundColor: `${color}30`,
                    boxShadow: `0 0 8px ${color}30`,
                  }}
                />
                {!isLast && (
                  <div className="w-px h-4 mt-0.5" style={{ backgroundColor: `${color}30` }} />
                )}
              </div>

              {/* Agent info */}
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="truncate text-sm font-medium text-white">{entry.agent}</span>
                  <CheckCircle2 className="w-3.5 h-3.5" style={{ color }} />
                </div>
              </div>

              {/* Duration */}
              <span className="shrink-0 font-mono text-xs text-white/30">
                {entry.duration_ms.toFixed(0)}ms
              </span>

              {/* Expand icon */}
              {isExpanded ? (
                <ChevronDown className="w-4 h-4 text-white/20 flex-shrink-0" />
              ) : (
                <ChevronRight className="w-4 h-4 text-white/20 flex-shrink-0" />
              )}
            </button>

            {/* Expanded details */}
            {isExpanded && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.2 }}
                className="ml-9 mb-2 pl-3 border-l border-white/5"
              >
                <div className="space-y-1.5 py-2">
                  <div>
                    <span className="text-white/30 text-[10px] tracking-widest uppercase">Input</span>
                    <p className="text-white/50 text-xs mt-0.5">{entry.input_summary}</p>
                  </div>
                  <div>
                    <span className="text-white/30 text-[10px] tracking-widest uppercase">Output</span>
                    <p className="text-white/50 text-xs mt-0.5">{entry.output_summary}</p>
                  </div>
                </div>
              </motion.div>
            )}
          </motion.div>
        );
      })}
    </div>
  );
}
