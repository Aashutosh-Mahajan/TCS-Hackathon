"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Sparkles, Loader2 } from "lucide-react";

interface QueryInputProps {
  onSubmit: (query: string) => void;
  isLoading: boolean;
}

const DEMO_QUESTIONS = [
  { text: "What is the annual leave policy?", lang: "en", emoji: "🇬🇧" },
  { text: "Is it true that employees get 60 days of annual leave?", lang: "en", emoji: "🔍" },
  { text: "वार्षिक छुट्टी नीति क्या है?", lang: "hi", emoji: "🇮🇳" },
  { text: "वार्षिक रजा धोरण काय आहे?", lang: "mr", emoji: "🇮🇳" },
  { text: "What is the health insurance coverage?", lang: "en", emoji: "🏥" },
  { text: "What is the company's policy on cryptocurrency investments?", lang: "en", emoji: "❓" },
];

export default function QueryInput({ onSubmit, isLoading }: QueryInputProps) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query.trim());
    }
  };

  const handleDemoClick = (text: string) => {
    setQuery(text);
    onSubmit(text);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, delay: 0.2 }}
      className="mx-auto w-full max-w-3xl"
      id="demo"
    >
      {/* Input */}
      <form onSubmit={handleSubmit}>
        <div className="liquid-glass flex items-center gap-2 rounded-2xl py-2 pl-4 pr-2 sm:gap-3 sm:rounded-full sm:pl-6">
          <Sparkles className="w-5 h-5 text-white/40 flex-shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question in English, Hindi, or Marathi..."
            className="min-w-0 flex-1 border-none bg-transparent text-sm text-white outline-none placeholder:text-white/35 sm:text-base"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="bg-white rounded-full p-3 text-black hover:bg-white/90 transition-colors disabled:opacity-40 disabled:cursor-not-allowed flex-shrink-0"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <ArrowRight className="w-5 h-5" />
            )}
          </button>
        </div>
      </form>

      {/* Demo questions */}
      <div className="mt-5">
        <p className="mb-2 text-center text-xs text-white/35">Try a demo question</p>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
        {DEMO_QUESTIONS.map((q, i) => (
          <motion.button
            key={i}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={() => handleDemoClick(q.text)}
            disabled={isLoading}
            className="liquid-glass min-w-0 rounded-xl px-3.5 py-2 text-left text-xs text-white/65 transition-colors hover:text-white disabled:opacity-40"
          >
            <span className="mr-1">{q.emoji}</span>
            <span className="inline-block max-w-[calc(100%-1.5rem)] truncate align-bottom">{q.text}</span>
          </motion.button>
        ))}
        </div>
      </div>
    </motion.div>
  );
}
