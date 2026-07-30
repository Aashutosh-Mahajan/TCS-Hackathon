"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { ConfidenceTag, TAG_COLORS } from "@/types";

interface ConfidenceGaugeProps {
  score: number; // 0-1
  tag: ConfidenceTag;
}

export default function ConfidenceGauge({ score, tag }: ConfidenceGaugeProps) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const colors = TAG_COLORS[tag];
  const percentage = Math.round(score * 100);

  // Animate the score value
  useEffect(() => {
    const duration = 1200;
    const start = performance.now();

    const animate = (now: number) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setAnimatedScore(Math.round(eased * percentage));

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  }, [percentage]);

  // SVG gauge parameters
  const size = 180;
  const strokeWidth = 10;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score * circumference);

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg
          width={size}
          height={size}
          className="transform -rotate-90"
        >
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="rgba(255,255,255,0.05)"
            strokeWidth={strokeWidth}
          />
          {/* Animated progress circle */}
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={colors.text}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            style={{
              filter: `drop-shadow(0 0 8px ${colors.text}40)`,
            }}
          />
        </svg>

        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className="text-4xl font-bold tabular-nums"
            style={{ color: colors.text }}
          >
            {animatedScore}
          </span>
          <span className="text-white/30 text-xs mt-0.5">/ 100</span>
        </div>
      </div>

      {/* Tag below gauge */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="mt-4 rounded-full px-4 py-1"
        style={{
          backgroundColor: colors.bg,
          border: `1px solid ${colors.border}`,
        }}
      >
        <span className="text-xs font-medium" style={{ color: colors.text }}>
          {tag}
        </span>
      </motion.div>
    </div>
  );
}
