"use client";

import { motion } from "framer-motion";
import { Shield, Activity } from "lucide-react";

export default function Navbar() {
  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="relative z-20 px-4 py-4 sm:px-6 sm:py-6"
    >
      <div className="liquid-glass mx-auto flex max-w-5xl items-center justify-between gap-3 rounded-full px-4 py-3 sm:px-6">
        {/* Left: Logo */}
        <div className="min-w-0 flex items-center gap-2.5 sm:gap-3">
          <div className="relative">
            <Shield className="w-6 h-6 text-white" />
            <Activity className="w-3 h-3 text-emerald-400 absolute -bottom-0.5 -right-0.5" />
          </div>
          <span className="truncate text-base font-semibold tracking-tight text-white sm:text-lg">
            AlgoSmiths
          </span>
          <span className="hidden sm:inline-block text-white/30 text-xs tracking-widest uppercase ml-2">
            P6 · Confidence Labeler
          </span>
        </div>

        {/* Right: Nav links */}
        <div className="flex shrink-0 items-center gap-4 sm:gap-6">
          <a
            href="#demo"
            className="hidden md:inline text-white/70 hover:text-white text-sm font-medium transition-colors"
          >
            Demo
          </a>
          <a
            href="#architecture"
            className="hidden md:inline text-white/70 hover:text-white text-sm font-medium transition-colors"
          >
            Architecture
          </a>
          <div className="liquid-glass rounded-full px-3 py-1.5 sm:px-5">
            <span className="text-xs font-medium tracking-wide text-white">
              <span className="sm:hidden">AI</span>
              <span className="hidden sm:inline">Responsible AI</span>
            </span>
          </div>
        </div>
      </div>
    </motion.nav>
  );
}
