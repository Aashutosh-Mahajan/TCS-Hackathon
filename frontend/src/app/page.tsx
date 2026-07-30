"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Shield, Zap, Globe, Brain } from "lucide-react";
import Navbar from "@/components/Navbar";
import QueryInput from "@/components/QueryInput";
import ResultCard from "@/components/ResultCard";
import { submitQuery } from "@/lib/api";
import { QueryResponse } from "@/types";

export default function Home() {
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (query: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await submitQuery(query);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen overflow-x-clip bg-black text-white">
      {/* Subtle radial gradient background */}
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_rgba(99,102,241,0.08)_0%,_transparent_50%)] pointer-events-none" />
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_bottom_right,_rgba(34,197,94,0.04)_0%,_transparent_50%)] pointer-events-none" />

      {/* Navbar */}
      <Navbar />

      {/* Hero Section */}
      <section className="relative z-10 flex min-h-[calc(100svh-96px)] flex-col items-center justify-center px-4 py-12 text-center sm:px-6">
        {/* Floating badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="liquid-glass mb-7 flex max-w-full items-center gap-2 rounded-full px-4 py-2 sm:px-5"
        >
          <Brain className="w-4 h-4 text-indigo-400" />
          <span className="truncate text-xs tracking-wide text-white/60">
            Responsible Enterprise AI · Multi-Agent RAG
          </span>
        </motion.div>

        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="mb-6 max-w-4xl text-5xl leading-[0.95] tracking-tight text-white sm:text-6xl md:text-7xl lg:text-8xl"
        >
          <span className="font-serif-display">Know</span>{" "}
          <span className="font-serif-display italic text-white/50">when</span>{" "}
          <span className="font-serif-display">to</span>{" "}
          <span className="font-serif-display italic text-white/50">trust</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mb-8 max-w-2xl px-2 text-sm leading-relaxed text-white/55 md:text-base"
        >
          We don&apos;t just answer — we tell enterprises when to trust the answer 
          and when to check it, across languages. Powered by multi-agent 
          retrieval with confidence scoring.
        </motion.p>

        {/* Feature pills */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="mb-8 grid w-full max-w-xs grid-cols-1 gap-2 sm:mb-10 sm:max-w-2xl sm:grid-cols-3 sm:gap-3"
        >
          {[
            { icon: Shield, text: "Hallucination Detection", color: "text-emerald-400" },
            { icon: Globe, text: "Multilingual (EN/HI/MR)", color: "text-blue-400" },
            { icon: Zap, text: "< 5s Latency", color: "text-amber-400" },
          ].map((feature, i) => (
            <div
              key={i}
              className="flex items-center justify-center gap-1.5 text-xs text-white/45"
            >
              <feature.icon className={`w-3.5 h-3.5 ${feature.color}`} />
              <span>{feature.text}</span>
            </div>
          ))}
        </motion.div>

        {/* Query Input */}
        <QueryInput onSubmit={handleSubmit} isLoading={isLoading} />
      </section>

      {/* Error Display */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="max-w-3xl mx-auto px-6 mt-4"
          >
            <div className="rounded-2xl px-5 py-4 text-sm border border-red-500/20 bg-red-500/5 text-red-400">
              <strong>Error:</strong> {error}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Results */}
      <AnimatePresence>
        {result && (
          <motion.section
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="relative z-10 px-4 pb-20 sm:px-6"
          >
            <ResultCard result={result} />
          </motion.section>
        )}
      </AnimatePresence>

      {/* Footer */}
      <footer className="relative z-10 py-8 text-center border-t border-white/5">
        <p className="text-white/20 text-xs">
          P6 — AI Hallucination Confidence Labeler · Team AlgoSmiths · TCS Hackathon
        </p>
      </footer>
    </main>
  );
}
