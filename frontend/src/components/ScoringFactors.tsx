"use client";

import { motion } from "framer-motion";
import { ScoringFactors as ScoringFactorsType } from "@/types";

interface ScoringFactorsProps {
  factors: ScoringFactorsType;
}

const GROUNDING_COLORS: Record<string, string> = {
  supported: "#22c55e",
  partial: "#f59e0b",
  contradicted: "#ef4444",
  no_evidence: "#ef4444",
};

export default function ScoringFactors({ factors }: ScoringFactorsProps) {
  return (
    <div className="space-y-5">
      {/* Retrieval Score */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-white/50 text-xs">
            Retrieval Similarity
          </span>
          <span className="text-white text-xs font-mono">
            {(factors.retrieval_score * 100).toFixed(1)}%
          </span>
        </div>
        <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${factors.retrieval_score * 100}%` }}
            transition={{ duration: 0.8, ease: "easeOut", delay: 0.2 }}
            className="h-full rounded-full"
            style={{
              background: `linear-gradient(90deg, rgba(99,102,241,0.6), rgba(99,102,241,1))`,
            }}
          />
        </div>
        <span className="text-white/25 text-[10px] mt-0.5 inline-block">
          Weight: {factors.retrieval_weight}
        </span>
      </div>

      {/* Grounding Label */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-white/50 text-xs">
            Grounding
          </span>
          <span
            className="text-xs font-semibold px-2 py-0.5 rounded-full"
            style={{
              color: GROUNDING_COLORS[factors.grounding_label] || "#fff",
              backgroundColor: `${GROUNDING_COLORS[factors.grounding_label] || "#fff"}15`,
            }}
          >
            {factors.grounding_label}
          </span>
        </div>
        <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${factors.grounding_multiplier * 100}%` }}
            transition={{ duration: 0.8, ease: "easeOut", delay: 0.4 }}
            className="h-full rounded-full"
            style={{
              backgroundColor: GROUNDING_COLORS[factors.grounding_label] || "#fff",
            }}
          />
        </div>
        <span className="text-white/25 text-[10px] mt-0.5 inline-block">
          Weight: {factors.grounding_weight} · Multiplier: {factors.grounding_multiplier}
        </span>
      </div>

      {/* Grounding Details */}
      <div className="border-t border-white/5 pt-3">
        <p className="text-white/40 text-xs leading-relaxed">
          {factors.grounding_details}
        </p>
      </div>

      {/* Formula */}
      <div className="border-t border-white/5 pt-3">
        <span className="text-white/30 text-[10px] tracking-widest uppercase">
          Formula
        </span>
        <p className="text-white/60 text-xs font-mono mt-1 break-all">
          {factors.formula}
        </p>
      </div>
    </div>
  );
}
