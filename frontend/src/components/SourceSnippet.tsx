"use client";

import { motion } from "framer-motion";
import { SnippetResponse, LANGUAGE_LABELS } from "@/types";
import { FileText, Globe } from "lucide-react";

interface SourceSnippetProps {
  snippet: SnippetResponse;
  rank: number;
}

export default function SourceSnippet({ snippet, rank }: SourceSnippetProps) {
  const scorePercent = (snippet.score * 100).toFixed(1);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: rank * 0.1 }}
      className="rounded-2xl border border-white/5 bg-white/[0.02] p-4 hover:bg-white/[0.04] transition-colors"
    >
      <div className="flex items-start gap-3">
        {/* Rank badge */}
        <div className="flex-shrink-0 w-7 h-7 rounded-full bg-white/5 flex items-center justify-center">
          <span className="text-white/40 text-xs font-bold">#{rank}</span>
        </div>

        <div className="flex-1 min-w-0">
          {/* Header */}
          <div className="mb-2 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex min-w-0 items-center gap-2">
              <FileText className="w-3.5 h-3.5 text-white/30" />
              {snippet.url ? (
                <a href={snippet.url} target="_blank" rel="noreferrer" className="truncate text-xs font-medium text-indigo-300 hover:text-indigo-200 underline">
                  {snippet.source}
                </a>
              ) : <span className="truncate text-xs font-medium text-white/60">{snippet.source}</span>}
            </div>
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
              <div className="flex items-center gap-1 text-white/30 text-[10px]">
                <Globe className="w-3 h-3" />
                <span>{LANGUAGE_LABELS[snippet.language] || snippet.language}</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-12 h-1.5 bg-white/5 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full bg-indigo-400/60"
                    style={{ width: `${snippet.score * 100}%` }}
                  />
                </div>
                <span className="text-white/30 text-[10px] font-mono">{scorePercent}%</span>
              </div>
            </div>
          </div>

          {/* Snippet text */}
          <p className="text-white/50 text-sm leading-relaxed">{snippet.text}</p>

          {/* Category tag */}
          {snippet.category && (
            <div className="mt-2">
              <span className="text-white/20 text-[10px] px-2 py-0.5 rounded-full border border-white/5">
                {snippet.category}
              </span>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
