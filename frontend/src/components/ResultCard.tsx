"use client";

import { motion } from "framer-motion";
import { QueryResponse, TAG_COLORS, LANGUAGE_LABELS, ConfidenceTag } from "@/types";
import ConfidenceGauge from "./ConfidenceGauge";
import ScoringFactors from "./ScoringFactors";
import AgentPipeline from "./AgentPipeline";
import SourceSnippet from "./SourceSnippet";
import { AlertTriangle, CheckCircle2, HelpCircle, Globe } from "lucide-react";

interface ResultCardProps {
  result: QueryResponse;
}

const TAG_ICONS: Record<ConfidenceTag, React.ReactNode> = {
  Certain: <CheckCircle2 className="w-5 h-5" />,
  Uncertain: <HelpCircle className="w-5 h-5" />,
  "Needs Verification": <AlertTriangle className="w-5 h-5" />,
};

export default function ResultCard({ result }: ResultCardProps) {
  const tagColors = TAG_COLORS[result.confidence_tag as ConfidenceTag];

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="mx-auto mt-10 w-full max-w-5xl space-y-6"
    >
      {/* Main Answer Card */}
      <div
        className="liquid-glass rounded-3xl p-6 md:p-8"
        style={{ boxShadow: tagColors.glow }}
      >
        {/* Header: Tag + Language */}
        <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200, delay: 0.3 }}
            className="flex items-center gap-2 rounded-full px-4 py-1.5"
            style={{
              backgroundColor: tagColors.bg,
              border: `1px solid ${tagColors.border}`,
            }}
          >
            <span style={{ color: tagColors.text }}>{TAG_ICONS[result.confidence_tag as ConfidenceTag]}</span>
            <span
              className="text-xs font-semibold tracking-wide sm:text-sm"
              style={{ color: tagColors.text }}
            >
              {result.confidence_tag}
            </span>
          </motion.div>

          <div className="flex items-center gap-2 text-xs text-white/40">
            <Globe className="w-3.5 h-3.5" />
            <span>{LANGUAGE_LABELS[result.detected_language] || result.detected_language}</span>
          </div>
        </div>

        <div className={`mb-5 rounded-xl px-4 py-3 text-sm ${result.dataset_status === "in_dataset" ? "border border-emerald-400/20 bg-emerald-400/5 text-emerald-200/80" : "border border-amber-400/30 bg-amber-400/10 text-amber-100"}`}>
          {result.dataset_status === "in_dataset"
            ? "Internal dataset evidence found."
            : result.web_searched
              ? "Not in the internal dataset. This output was web-searched and requires verification against the original source."
              : "Not in the internal dataset. Verification is required before relying on this response."}
        </div>

        {/* Warning Banner */}
        {result.warning && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="rounded-xl px-4 py-3 mb-5 text-sm"
            style={{
              backgroundColor: "rgba(239, 68, 68, 0.08)",
              border: "1px solid rgba(239, 68, 68, 0.2)",
              color: "rgba(239, 68, 68, 0.9)",
            }}
          >
            {result.warning}
          </motion.div>
        )}

        {/* Answer */}
        <div className="mb-5">
          <h3 className="text-white/40 text-xs tracking-widest uppercase mb-3">
            Answer
          </h3>
          <p className="text-white text-base md:text-lg leading-relaxed">
            {result.answer}
          </p>
        </div>

        {/* Explanation */}
        <div className="border-t border-white/5 pt-4">
          <h3 className="text-white/40 text-xs tracking-widest uppercase mb-2">
            Explanation
          </h3>
          <p className="text-white/60 text-sm leading-relaxed">
            {result.explanation}
          </p>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Confidence Gauge */}
        <div className="liquid-glass rounded-3xl p-6 md:p-8">
          <h3 className="text-white/40 text-xs tracking-widest uppercase mb-6">
            Confidence Score
          </h3>
          <ConfidenceGauge
            score={result.confidence_score}
            tag={result.confidence_tag as ConfidenceTag}
          />
        </div>

        {/* Scoring Factors */}
        <div className="liquid-glass rounded-3xl p-6 md:p-8">
          <h3 className="text-white/40 text-xs tracking-widest uppercase mb-6">
            Scoring Factors
          </h3>
          <ScoringFactors factors={result.scoring_factors} />
        </div>
      </div>

      {/* Agent Pipeline */}
      <div className="liquid-glass rounded-3xl p-6 md:p-8" id="architecture">
        <h3 className="mb-6 text-xs uppercase tracking-widest text-white/40">
          Agent Pipeline Trace
        </h3>
        <AgentPipeline trace={result.agent_trace} />
      </div>

      {/* Source Snippets */}
      <div className="liquid-glass rounded-3xl p-6 md:p-8">
        <h3 className="text-white/40 text-xs tracking-widest uppercase mb-6">
          Retrieved Source Evidence ({result.retrieved_snippets.length})
        </h3>
        <div className="space-y-4">
          {result.retrieved_snippets.map((snippet, i) => (
            <SourceSnippet key={i} snippet={snippet} rank={i + 1} />
          ))}
        </div>
      </div>
    </motion.div>
  );
}
