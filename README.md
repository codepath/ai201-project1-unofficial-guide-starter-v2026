# The Unofficial Guide

Yaw Kessey-Ankomah — `campus_life`

---

# Unit 1

## What This Does

I selected the `campus_life` corpus of short campus posts. This command-line guide answers questions covered by those posts, including courses, campus work hours, and meal-plan details. It retrieves relevant chunks and uses them to generate an answer with a source document. If no chunk is close enough to the question, the relevance gate refuses to answer.

## Chunking Strategy

**Chunk size:** Up to three complete body sentences, with the document title repeated for context.

**Overlap:** Zero repeated body sentences; the title is retained in each chunk.

Campus posts are short but can cover several topics, so I chose smaller groups of complete sentences to keep the retrieved material focused. The original 800-character windows kept all 88 posts whole; the new strategy produces 141 chunks. I start with no body-sentence overlap to avoid repeating the same facts, while retaining the title to identify the topic. This limits retrieved text, not the length of the final answer. The simple sentence splitter preserves decimal prices but may split abbreviations incorrectly, and sentence groups can still depend on context in another chunk.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_340.txt#0` — produced by: `chunker.py::split_documents`

```
CS 340 Databases

I'm a junior and I've done this twice now. Format is lecture twice a week plus a project that runs the whole term. Assessment: one midterm and a final, both open-book.
```

**Chunk 3** — source: `dining_halden_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Halden Hall

I lived here my sophomore year. Wait times: rarely more than 8 minutes, even at noon. The thing worth going for is soup rotation, and the bread is baked on site.
```

**Chunk 4** — source: `health_center.txt#0` — produced by: `chunker.py::split_documents`

```
The health centre

Walk-in hours are 8am to 11am; everything after that is by appointment and appointments run about a week out. If something is urgent, go at 8am and wait rather than booking. Counselling is separate, in the same building, and has its own intake process with a shorter wait than people expect — usually three or four days for a first session.
```

**Chunk 5** — source: `housing_morrow_house_laundry.txt#0` — produced by: `chunker.py::split_documents`

```
Laundry in Morrow House

Machines take $1.50 wash, $1.25 dry, coin or card. There are eight washers and six dryers for the building, which is the wrong ratio and means the dryers back up on Sunday evenings. Best time to do laundry here is Tuesday or Wednesday morning.
```

## Sample Answer

**Question:** How many times can I change my meal plan tier?

**Answer:**

```
You can change your meal plan tier once.

Source: admin_meal_plan_changes.txt
```

**My relevance cutoff:** `0.6`

With the rebuilt sentence-based index, the five in-corpus best distances range from 0.2302 to 0.3938, while the five out-of-scope distances range from 0.8236 to 0.8859. The existing cutoff of 0.6 falls in the gap, so I kept it: all five in-corpus questions pass the gate and all five out-of-scope questions are refused. These measurements support the cutoff for these ten questions; they do not guarantee the same result for every possible question.

| Question | In corpus? | Best distance |
|---|---|---|
| How many times can I change my meal plan tier? | Yes | 0.2475 |
| When is the withdrawl dealine? | Yes | 0.3938 |
| How many hours do I have to commit to CS 340 Databases class? | Yes | 0.2835 |
| How much money do I get to print per semester. | Yes | 0.2876 |
| How many hours can I work a week with campus work | Yes | 0.2302 |
| What is the capital of Mongolia? | No | 0.8236 |
| How do I change the oil in a diesel engine? | No | 0.8493 |
| Who won the 1994 World Cup? | No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8442 |
| How do I write a for loop in Rust? | No | 0.8714 |

## How I Used AI

**1.**
I asked Codex to help me write `split_documents()` using my three-sentence chunk limit, without editing the file for me. It suggested grouping up to three body sentences, repeating the document title for context, and using zero body-sentence overlap. I pasted the code myself, but my saved version had missing lines and indentation errors. With Codex's debugging feedback, I corrected the indentation, added the missing import, document loop, and chunk-list initialization, and returned the new chunks instead of calling the fallback. Codex then ran the preview successfully, producing 141 chunks instead of the starter's 88.

**2.**
I ran retrieval for my meal-plan and withdrawal questions, then asked Codex to run the remaining three campus questions and the five out-of-scope questions and record the distances in my README. The combined results showed in-corpus best distances of 0.2302–0.3938 and out-of-scope distances of 0.8236–0.8859. Codex recommended keeping the existing 0.6 cutoff because it fell between those groups and filled the blank table with the measured results. I left that recommendation unchanged. I then asked Codex to run the meal-plan question and add the actual answer and source to the Sample Answer section.

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
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

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
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

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
