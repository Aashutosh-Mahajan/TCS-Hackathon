# Product Requirements Document
## P6 — AI Hallucination Confidence Labeler

**Team:** AlgoSmiths
**Theme:** Responsible Enterprise AI
**Prototype Type:** Multi-agent RAG system with multilingual, multi-model retrieval
**Timeline:** 90-minute mini-hackathon build

---

## 1. Problem Statement

AI systems frequently generate answers that sound confident regardless of whether they are actually supported by evidence. In enterprise settings — HR policy queries, compliance questions, financial reporting — this creates real risk: users cannot distinguish a well-grounded answer from a plausible-sounding hallucination.

**Core problem:** There is no lightweight, explainable mechanism that tells an enterprise user *how much to trust* an AI-generated answer, in the language they asked in.

## 2. Goal

Build a prototype that takes a question, retrieves relevant evidence (across languages), generates an answer, and labels that answer **Certain**, **Uncertain**, or **Needs Verification** — with a short reason, a warning if evidence is weak or missing, and a confidence/perplexity metric.

**Explicit non-goal:** Perfect factual accuracy. The focus is reliability *awareness*, not answer correctness.

## 3. Target User

Enterprise knowledge workers and compliance teams who query internal AI assistants (HR bots, policy bots, internal search) and need a trust signal before acting on the answer.

## 4. Success Criteria (for the demo)

| Criterion | Target |
|---|---|
| Correctly tags fully-supported answers as Certain | ≥ 90% on test set |
| Correctly flags contradicted/hallucinated answers as Needs Verification | ≥ 90% on test set |
| Correctly flags partially-supported answers as Uncertain | Demonstrated on ≥ 2 examples |
| Cross-lingual retrieval works (Hindi/Marathi query retrieves correct snippet) | Demonstrated live in demo |
| End-to-end latency per query | < 5 seconds |
| Explanation output is human-readable, not a raw score dump | Judged qualitatively |

## 5. System Architecture

```
User Question (any language)
        │
[Language Agent] — detect language
        │
[Retriever Agent] — multi-model retrieval
    • Dense: multilingual-e5-small embeddings (cosine similarity)
    • Sparse: BM25 keyword matching
    • Fusion: Reciprocal Rank Fusion (RRF) of both rankings
        │
[Answer Agent] — generates/selects answer using retrieved context (Claude API)
        │
[Grounding Agent] — checks answer against retrieved snippet
    • Entailment check: supported / partial / contradicted / no evidence
        │
[Confidence Scorer Agent] — rule-based fusion of:
    • retrieval similarity score
    • grounding label
    • answer perplexity / confidence proxy
    → maps to Certain / Uncertain / Needs Verification
        │
[Explainer Agent] — generates short human-readable reason + warning
        │
Output: Answer | Reliability Tag | Reason | Confidence Score | Source Snippet
```

Each stage is implemented as a discrete node (LangGraph-style), making the pipeline inspectable and each decision auditable — a requirement for enterprise responsible-AI use cases.

## 6. Functional Requirements

| ID | Requirement |
|---|---|
| FR1 | Accept a question in English, Hindi, or Marathi |
| FR2 | Retrieve top-k relevant source snippets using dense + sparse fusion |
| FR3 | Generate or surface an answer grounded in retrieved context |
| FR4 | Classify answer as Certain / Uncertain / Needs Verification |
| FR5 | Output a short (1–2 sentence) human-readable reason for the tag |
| FR6 | Display a warning when no source evidence is found |
| FR7 | Display a confidence/perplexity-style numeric score alongside the tag |
| FR8 | Support cross-lingual retrieval (query in one language, snippet in another, correctly matched by meaning) |

## 7. Data Requirements

- 20-entry hand-curated dataset (`rag_dataset.json`) covering:
  - Fully supported answers (Certain)
  - Contradicted answers (Needs Verification)
  - Partially supported answers (Uncertain)
  - No-source-available cases (Needs Verification)
  - English, Hindi, and Marathi entries, including cross-lingual "twin" pairs (same fact, different language) to validate multilingual embedding quality

## 8. Confidence Scoring Logic (Rule-Based, Explainable)

| Retrieval Score | Grounding Label | Output Tag |
|---|---|---|
| High | Supported | Certain |
| Medium / High | Partial | Uncertain |
| Low / None | Contradicted or No Evidence | Needs Verification |

Chosen deliberately over a black-box ML classifier: transparent, auditable, and defensible in a live Q&A with judges — directly aligned with "Responsible Enterprise AI" theme.

## 9. Technical Stack

| Layer | Tool |
|---|---|
| Embeddings | `intfloat/multilingual-e5-small` (sentence-transformers) |
| Sparse retrieval | `rank_bm25` |
| Fusion | Reciprocal Rank Fusion (custom, ~10 lines) |
| Generation / grounding check | Claude API |
| Orchestration | LangGraph (or function-chain fallback if time-constrained) |
| Backend | FastAPI |
| Frontend | Single-page HTML/React — input box, output card with color-coded tag |

## 10. Out of Scope (for this prototype)

- Live document ingestion / crawling
- Fine-tuned or trained confidence classifier
- Full translation pipeline (relying instead on multilingual embedding space)
- Authentication, multi-user support, persistence layer

## 11. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| 90-min time limit too tight for full pipeline | Pre-built dataset ready in advance; fallback to function-chain instead of full LangGraph if behind schedule |
| Perplexity metric unavailable via API | Use answer–context similarity as a labeled "confidence proxy" instead; state this transparently in demo |
| Judges test edge cases not in dataset | Rule-based scorer generalizes past the 20 examples since it operates on retrieval/grounding scores, not memorized answers |

## 12. Demo Script (for judges)

1. Ask a clearly supported question (English) → show **Certain** tag with source snippet.
2. Ask a subtly wrong / contradicted question → show **Needs Verification** with warning.
3. Ask the same underlying fact in Hindi and Marathi → show both retrieve the correct cross-lingual snippet with matching confidence, proving multilingual retrieval works — not hardcoded per-language rules.
4. Close with the one-line pitch: *"We don't just answer — we tell enterprises when to trust the answer and when to check it, across languages."*

## frontend prompt make changes according to project 
RECREATION PROMPT

Build a single-page landing site using React + TypeScript + Vite + Tailwind CSS + framer-motion + lucide-react. The entire page has a bg-black background. The font loaded via Google Fonts is Instrument Serif (italic and regular). Import it in index.css:


@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap');
LIQUID GLASS CSS (in index.css, inside @layer components)
Create a reusable .liquid-glass class used on every glass element:


.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.45) 0%,
    rgba(255, 255, 255, 0.15) 20%,
    rgba(255, 255, 255, 0) 40%,
    rgba(255, 255, 255, 0) 60%,
    rgba(255, 255, 255, 0.15) 80%,
    rgba(255, 255, 255, 0.45) 100%
  );
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
SECTION 1 -- HERO (full-viewport, in Index.tsx)
Full-screen (min-h-screen) container with overflow-hidden relative flex flex-col.

Background video: absolute, covers the entire viewport (absolute inset-0 w-full h-full object-cover object-bottom). URL:


https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260405_074625_a81f018a-956b-43fb-9aee-4d1508e30e6a.mp4
Attributes: muted, autoPlay, playsInline, preload="auto". Starts at opacity: 0.

Video fade logic (vanilla JS via refs, no CSS transitions):

On canplay: play the video, then animate opacity from 0 to 1 over 500ms using requestAnimationFrame.
On timeupdate: when remaining time <= 0.55s, animate opacity from current to 0 over 500ms.
On ended: set opacity to 0, wait 100ms, reset currentTime to 0, play again, fade back to 1 over 500ms.
This creates a seamless loop with smooth crossfade to black between plays.
Navbar (relative z-20, px-6 py-6):

A liquid-glass rounded-full pill, max-w-5xl mx-auto, px-6 py-3, flex between left/right.
Left: Globe icon (24px, white) + "Asme" text (white, font-semibold, text-lg). Hidden on mobile: nav links "Features", "Pricing", "About" (text-white/80 hover:text-white text-sm font-medium, gap-8 ml-8).
Right: "Sign Up" text button (white, text-sm, font-medium) + "Login" button (liquid-glass rounded-full px-6 py-2, white text-sm font-medium).
Hero content (relative z-10, flex-1 flex flex-col items-center justify-center, px-6 py-12 text-center, -translate-y-[20%]):

Heading: text-7xl md:text-8xl lg:text-9xl, white, tracking-tight whitespace-nowrap, font-family 'Instrument Serif', serif. Text: Know it then <em className="italic">all</em>.
Email input: max-w-xl w-full. A liquid-glass rounded-full pill with pl-6 pr-2 py-2 flex items-center gap-3. Inside: transparent <input> with placeholder "Enter your email" (text-white placeholder:text-white/40). A white circular submit button (bg-white rounded-full p-3 text-black) containing ArrowRight icon (20px).
Subtitle: text-white text-sm leading-relaxed px-4. Text: "Stay updated with the latest news and insights. Subscribe to our newsletter today and never miss out on exciting updates."
Manifesto button: liquid-glass rounded-full px-8 py-3 text-white text-sm font-medium hover:bg-white/5 transition-colors.
Social icons footer (relative z-10, flex justify-center gap-4 pb-12):

Three liquid-glass rounded-full p-4 buttons for Instagram, Twitter, Globe icons (20px). text-white/80 hover:text-white hover:bg-white/5 transition-all.
SECTION 2 -- ABOUT SECTION (separate component AboutSection.tsx)
Uses framer-motion useInView (ref, { once: true, margin: "-100px" }).
bg-black pt-32 md:pt-44 pb-10 md:pb-14 px-6 overflow-hidden.
Subtle radial gradient overlay: bg-[radial-gradient(ellipse_at_top,_rgba(255,255,255,0.03)_0%,_transparent_70%)].
Label: "About Us" -- text-white/40 text-sm tracking-widest uppercase. Animates: opacity: 0, y: 20 -> opacity: 1, y: 0, duration 0.6.
Heading: text-4xl md:text-6xl lg:text-7xl text-white leading-[1.1] tracking-tight. Animates: opacity: 0, y: 40 -> opacity: 1, y: 0, duration 0.8, delay 0.1. Text structure:
Pioneering then ideas (Instrument Serif italic, text-white/60) for
Line break (hidden on mobile)
minds that then create, build, and inspire. (all Instrument Serif italic, text-white/60)
SECTION 3 -- FEATURED VIDEO (separate component FeaturedVideoSection.tsx)
bg-black pt-6 md:pt-10 pb-20 md:pb-32 px-6 overflow-hidden. Max-w-6xl.
A rounded-3xl overflow-hidden aspect-video container that animates opacity: 0, y: 60 -> opacity: 1, y: 0, duration 0.9.
Video: w-full h-full object-cover, muted, autoPlay, loop, playsInline, preload="auto". URL:

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260402_054547_9875cfc5-155a-4229-8ec8-b7ba7125cbf8.mp4
Gradient overlay on video: bg-gradient-to-t from-black/60 via-transparent to-transparent.
Bottom overlay content (absolute bottom-0 left-0 right-0 p-6 md:p-10):
Flex row on desktop, column on mobile.
Left: a liquid-glass rounded-2xl p-6 md:p-8 max-w-md card. Label "Our Approach" (text-white/50 text-xs tracking-widest uppercase mb-3). Body text (text-white text-sm md:text-base leading-relaxed): "We believe in the power of curiosity-driven exploration. Every project starts with a question, and every answer opens a new door to innovation."
Right: "Explore more" button (liquid-glass rounded-full px-8 py-3, white text-sm font-medium) with whileHover={{ scale: 1.05 }} and whileTap={{ scale: 0.95 }}.
SECTION 4 -- PHILOSOPHY / INNOVATION x VISION (separate component PhilosophySection.tsx)
bg-black py-28 md:py-40 px-6 overflow-hidden. Max-w-6xl.
Heading: text-5xl md:text-7xl lg:text-8xl text-white tracking-tight mb-16 md:mb-24. Animates opacity: 0, y: 40 -> opacity: 1, y: 0, duration 0.8. Text: Innovation then x in Instrument Serif italic text-white/40, then Vision.
Two-column grid (grid-cols-1 md:grid-cols-2 gap-8 md:gap-12):
Left: Video in rounded-3xl overflow-hidden aspect-[4/3]. Animates from opacity: 0, x: -40. URL:

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260307_083826_e938b29f-a43a-41ec-a153-3d4730578ab8.mp4
muted, autoPlay, loop, playsInline, preload="auto".
Right: Animates from opacity: 0, x: 40. Two text blocks separated by a w-full h-px bg-white/10 divider.
Block 1: Label "Choose your space" (text-white/40 text-xs tracking-widest uppercase mb-4). Body (text-white/70 text-base md:text-lg leading-relaxed): "Every meaningful breakthrough begins at the intersection of disciplined strategy and remarkable creative vision. We operate at that crossroads, turning bold thinking into tangible outcomes that move people and reshape industries."
Block 2: Label "Shape the future". Body: "We believe that the best work emerges when curiosity meets conviction. Our process is designed to uncover hidden opportunities and translate them into experiences that resonate long after the first impression."
SECTION 5 -- SERVICES / WHAT WE DO (separate component ServicesSection.tsx)
bg-black py-28 md:py-40 px-6 overflow-hidden. Max-w-6xl.
Subtle radial gradient: bg-[radial-gradient(ellipse_at_center,_rgba(255,255,255,0.02)_0%,_transparent_60%)].
Header row: flex between "What we do" (text-3xl md:text-5xl text-white tracking-tight) and "Our services" label (text-white/40 text-sm, hidden on mobile). Animates opacity: 0, y: 30 -> visible, duration 0.7.
Two-card grid (grid-cols-1 md:grid-cols-2 gap-6 md:gap-8):
Each card: liquid-glass rounded-3xl overflow-hidden with group class. Animates opacity: 0, y: 50 -> visible, duration 0.8, staggered by 0.15s.
Card video area: aspect-video, object-cover, transition-transform duration-700 group-hover:scale-105. Gradient overlay: bg-gradient-to-t from-black/40 to-transparent.
Card body (p-6 md:p-8): tag label (uppercase, tracking-widest, text-white/40 text-xs), ArrowUpRight icon in a liquid-glass rounded-full p-2 circle, title (text-white text-xl md:text-2xl mb-3 tracking-tight), description (text-white/50 text-sm leading-relaxed).
Card 1: Video URL:

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260314_131748_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4
Tag: "Strategy". Title: "Research & Insight". Description: "We dig deep into data, culture, and human behavior to surface the insights that drive meaningful, lasting change."
Card 2: Video URL:

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260324_151826_c7218672-6e92-402c-9e45-f1e0f454bdc4.mp4
Tag: "Craft". Title: "Design & Execution". Description: "From concept to launch, we obsess over every detail to deliver experiences that feel effortless and look extraordinary."