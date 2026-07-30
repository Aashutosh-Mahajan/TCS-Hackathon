import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Hallucination Confidence Labeler | AlgoSmiths",
  description:
    "Multi-agent RAG system that labels AI-generated answers with confidence and reliability tags — Certain, Uncertain, or Needs Verification — across languages.",
  keywords: [
    "AI hallucination",
    "confidence labeling",
    "responsible AI",
    "RAG",
    "multilingual",
    "enterprise AI",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-black text-white antialiased">{children}</body>
    </html>
  );
}
