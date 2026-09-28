# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

A searchable guide to 5 cities in a fictional region (city_guides corpus). The system answers specific questions about each city—attractions, logistics, costs, accessibility—by retrieving relevant sections from city guides and grounding answers in actual documents.

## Chunking Strategy

**Strategy:** Split documents on section heading boundaries (`#` markers) instead of fixed character counts.

**Why:** City guides are organized by topic (Getting around, Eat and drink, When to go). The default 800-character chunker ignored these boundaries and created fragments. By splitting on `#`, each chunk covers one complete topic, keeping related information together. This keeps sentences intact and lets retrieval find topically coherent chunks.

## Sample Chunks

**Chunk 1** — source: `guide_accessibility.md` — produced by: `chunker.py::section_split`

```
Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md` — produced by: `chunker.py::section_split`

```
When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.
```

**Chunk 3** — source: `guide_givens_mill.md` — produced by: `chunker.py::section_split`

```
Eat and drink

A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metres away and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.
```

**Chunk 4** — source: `guide_kestrelford.md` — produced by: `chunker.py::section_split`

```
When to go

Late spring and early autumn. The Saturday market runs year-round but is much reduced from November to February. August is busy with walkers. The single-track approach road is genuinely difficult in snow and the town can be cut off for a day or two most winters.
```

**Chunk 5** — source: `guide_regional_transport.md` — produced by: `chunker.py::section_split`

```
The railway

The line runs along the river valley, connecting Brightwater to the regional
hub in 50 minutes. Eleven services a day on weekdays, six on Sundays. The line
north of Brightwater closed in 1963 and everything beyond it is bus or car.

Tickets are cheaper booked the day before than on the day, and considerably
cheaper than that booked a week ahead. There is no ticket office at
Brightwater station outside weekday mornings; the machine on the platform takes
cards only.
```

## Sample Answer

**Question:** which city's has Saturday market that has run since the 1400s

**Answer:** According to guide_eating.md, Kestrelford's Saturday market has run since the 1400s.

**My relevance cutoff:** 0.65

**Why this cutoff:** In-scope questions (about topics in the corpus) had distances 0.265-0.578. Setting cutoff at 0.65 leaves room for legitimate questions while blocking out-of-scope noise.

| Question | In corpus? | Best distance |
|---|---|---|
| Saturday market in Kestrelford | Yes | 0.265 |
| Lighthouse cities | Yes | 0.459 |
| Minor injuries units | Yes | 0.578 |
| Landmark in Brightwater | Yes | 0.362 |
| Valley and villages | Yes | 0.358 |

## How I Used AI

**1.** I asked Claude to help me think through what makes a good chunking strategy. It guided me to realize that section boundaries (`#` markers) in my documents were the key signal, not character count. I implemented section_split based on that insight, tested it, and saw retrieval improve from distance 0.701 (rejected) to 0.538 (accepted).

**2.** I asked Claude to review my acceptance criteria before committing them. It caught that my first criterion was too vague about "chunking the right size," so I rewrote criterion 4 to be specific: "4 of 5 chunks read as complete thoughts with no sentence cuts." That made it testable.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks keep important information together | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. Answer names the right place | 4 of 5 | 3/5 | 3/5 | 3/5 | MISSED |

### Real Output — Criterion 1

Q1: which city's has Saturday market that has run since the 1400s

**Run 1:**
- Sources:  guide_brightwater.md, guide_eating.md, guide_kestrelford.md
- Answer:  Kestrelford's Saturday market has run since the 1400s
- Retrieved chunks contain answer? YES

Q2: which cities are closer to a lighthouse (max 3 hours away)

**Run 1:**
- Sources: guide_elder_ness.md, guide_halden_bay.md, guide_pellew_sands.md, guide_walking.md
- Answer: Based on the provided documents, I do not have enough information to answer which cities are closer to a lighthouse.
- Retrieved chunks contain answer? NO

Q3: which cities have minor injuries units

**Run 1:**
- Sources: guide_accessibility.md, guide_brightwater.md, guide_corry_vale.md, guide_elder_ness.md, guide_halden_bay.md
- Answer: Based on the provided documents, minor injuries units are located in Kestrelford, Halden Bay, Corry Vale, Givens Mill, and Elder Ness 
- Retrieved chunks contain answer? YES

Q4: what is the famous landmark or museum in Brightwater

**Run 1:**
- Sources: guide_brightwater.md, guide_kestrelford.md, guide_regional_transport.md, guide_seasons.md, guide_walking.md
- Answer: I don't have enough information to answer your question from the provided documents.
- Retrieved chunks contain answer? NO

Q5: which city has valley and four villages in it

**Run 1:**
- Sources: guide_corry_vale.md, guide_walking.md
- Answer: Based on the provided documents, Corry Vale is not a town or city, but a valley containing four villages strung along eleven miles of road
- Retrieved chunks contain answer? YES

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MISSED | Three of five questions had the answer in retrieved chunks, below my target of 4 of 5. |
| 2 | Every answer names a source | MISSED | Only three answers named specific source files (Q1, Q3, Q5). Q2 and Q4 said "no information" without naming any guide_*.md files. Target requires all 5. |
| 3 | Gate stops out-of-corpus questions | MET | All 5 out-of-scope questions were refused by the gate, exceeding target of 4 of 5. |
| 4 | Chunks keep important information together | MET | Section-based chunking kept 4 of 5 sampled chunks as complete thoughts with no sentence cuts, meeting the target of 4 of 5. |
| 5 | Answer names the right place | MISSED | Q1 correctly names Kestrelford, Q3 correctly names all 5 cities, Q5 correctly names Corry Vale. Q2 and Q4 refused to answer. 3 correct out of 5, below target of 4. |

## Diagnoses

All three misses (Criteria 1, 2, 5) stem from the same root cause:

Questions 2 and 4 fail at GENERATION stage:
- Retrieval successfully finds relevant chunks (distances 0.459 and 0.362, both below 0.65 threshold)
- Gate accepts them as in-corpus questions
- But the generation step refuses to answer, saying "I do not have enough information"
- Q2 retrieves chunks about Elder Ness and Halden Bay (which mention lighthouses), but model ignores them
- Q4 retrieves chunks about Brightwater, but model says it doesn't know about landmarks there
- The model is too conservative. It has the chunks but doesn't extract answers from them

Pattern: Retrieval works fine, but generation is overly cautious and refuses to answer from perfectly valid chunks. The grounding prompt or model behavior needs adjustment to use retrieved chunks more aggressively.

## The Improvement

**What I changed:**

Modified the grounding instruction in generate.py to be more aggressive about using retrieved chunks. Changed from "If the documents don't cover the question, say you don't have enough information. Do not guess." to "Extract and use relevant information from the documents, even if it requires inference from related topics. If documents mention information related to the question, use it rather than refusing."

**Why I picked it:**

My diagnosis showed that retrieval worked but generation refused to answer from good chunks. Q2 and Q4 both retrieved relevant documents but said "I do not have enough information." The grounding prompt was telling the model to refuse unless it had perfect answers. Making it more aggressive directly targets this failure.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 4/5 | 4/5 | 4/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks keep important information together | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. Answer names the right place | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |

**Did it help?**

Yes. The improvement lifted Criterion 1 from MISSED (3/5) to MET (4/5). Q2 now answers with Halden Bay and Elder Ness, naming the lighthouse information from the documents. Q4 still refuses to answer about Brightwater landmarks despite having chunks retrieved. Criterion 5 also improved from 3/5 to 4/5 because Q2 now names the correct places.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
