# The Unofficial Guide

Tanisha Jain — corpus: `campus_life`

> Note: unit 1 was completed late, at the start of unit 2. The questions and
> criteria were committed (34c8d9d) before any eval run, so the order in the
> history is still criteria → results.

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

A question-answering system over `campus_life`: 88 short student-written posts
about a fictional university's dining halls, dorms, courses, transit and admin
rules. You ask a plain-English question ("How late is the library open during
reading week?"), it retrieves the most relevant posts with a local embedding
model, refuses if nothing is close enough, and otherwise has Gemini answer
using only those posts, naming the file it used.

## Chunking Strategy

**Chunk size:** one whole post per chunk (posts over 800 characters would be split on paragraph breaks — none are)
**Overlap:** none

Every post is one short thought: they average 317 characters and the longest
(`housing_old_brewhouse.txt`) is 554. Splitting them would only separate a
building's name from its facts — "Laundry in Morrow House" from "$1.50 wash,
$1.25 dry" — and since seven laundry posts are otherwise word-for-word
identical, a chunk without the building name is useless. So
`chunker.py::split_documents` keeps each post whole (88 documents → 88
chunks), with a paragraph-boundary split as a safety net for anything over
`CHUNK_SIZE`. Overlap only matters when you cut, so there is none.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** How much does it cost to use a dryer in Morrow House?

**Answer:** (`python app.py ask ...`, best distance 0.320, cutoff 0.6)

```
It costs $1.25 to use a dryer in Morrow House.

Source: housing_morrow_house.txt (also found in housing_morrow_house_laundry.txt)

Sources retrieved: housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_old_brewhouse_laundry.txt
```

**My relevance cutoff:** 0.6 (kept the default, because my own measurements put it in the middle of a clean gap)

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

The five in-corpus questions landed between 0.320 and 0.463; the five
out-of-corpus ones between 0.825 and 0.934. Nothing falls between 0.463 and
0.825, so any cutoff in that range separates them; 0.6 leaves ~0.14 of margin
above the worst in-corpus question and ~0.22 below the closest out-of-corpus one.

| Question | In corpus? | Best distance |
|---|---|---|
| How often does the campus shuttle run on weekends? | yes | 0.411 |
| How much does it cost to use a dryer in Morrow House? | yes | 0.320 |
| What is the last week you can withdraw from a course? | yes | 0.406 |
| How late is the library open during reading week? | yes | 0.427 |
| Is a cash meal cheaper at Halden Hall or Kestrel Commons? | yes | 0.463 |
| What is the capital of Mongolia? | no | 0.825 |
| How do I change the oil in a diesel engine? | no | 0.934 |
| Who won the 1994 World Cup? | no | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.844 |
| How do I write a for loop in Rust? | no | 0.896 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1. Writing the questions and criteria.** I asked Claude (Claude Code) to
draft my five test questions and criteria 4 and 5 from the `campus_life`
documents. It read the whole corpus and deliberately picked questions with
traps — seven near-identical laundry posts, the drop vs. withdrawal deadlines,
seven noise posts that all say "library open until 2am". It also added an
`answer_in` field to each question so criterion 1 could be checked
mechanically instead of by my judgment. I reviewed them and committed them
before running anything.

**2. Chunking and the cutoff.** Claude suggested keeping each post as one
chunk rather than tuning the 800/120 numbers, because no post reaches 800
characters, and measured the ten best distances that set the cutoff. I kept
0.6 because the measured gap (0.463 → 0.825) showed it was already safe.

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

Source file: [`results/run_2026-10-04_2112_before.md`](results/run_2026-10-04_2112_before.md),
produced by `run_eval.py::main` (3 runs, cache off, 15 real model calls).
Per-criterion counts aggregated from it by `criteria_report.py::main`; answers
scored by `scorer.py::judge`. Corpus `campus_life`, whole-post chunks
(`chunker.py::split_documents`), top-k 5, cutoff 0.6.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Rank-1 chunk is from the answer document | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. Answer states the correct fact | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Criteria 3 and 4 are identical across runs by construction: both depend only on
retrieval, which is deterministic. Criteria 2 and 5 depend on the generated
answer and *could* have moved; they didn't. The runs were real — the wording
differs between runs (e.g. Morrow House run 1 cites
"`housing_morrow_house_laundry.txt` (also mentioned in
`housing_morrow_house.txt`)", run 2 "Sources: housing_morrow_house_laundry.txt
and housing_morrow_house.txt") — the facts just didn't.

**Real output, run 1** (from `results/run_2026-10-04_2112_before.md`):

*Criterion 1* — `store.py::search`, sources retrieved for the comparison question (both `answer_in` documents present):
```
- Best distance: 0.4630 (passed the gate)
- Sources retrieved: admin_dining_dollars.txt, dining_halden_hall.txt, dining_kestrel_commons.txt, dining_north_kitchen.txt, dining_pellew_dining_hall.txt
```

*Criterion 2* — `generate.py::answer_from_chunks`:
```
You can withdraw from a course through week ten, according to admin_withdrawal_deadline.txt.
```

*Criterion 3* — `run_eval.py::check_out_of_scope`, cutoff 0.6:
```
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.896 | refused |
```

*Criterion 4* — `store.py::search` ranking, the one question where rank 1 was wrong:
```
How late is the library open during reading week?
  1. admin_library_holds.txt          0.427   <- not the answer document
  2. study_library_hours.txt          0.450   <- the answer
  3. housing_morrow_house_noise.txt   0.485
  4. housing_calder_annexe_noise.txt  0.497
  5. dining_north_kitchen_followup.txt 0.523
```

*Criterion 5* — `generate.py::answer_from_chunks`, scored by `scorer.py::judge`:
```
The library is open until 10pm during reading week (from study_library_hours.txt).
A cash meal is cheaper at Halden Hall, where it costs $10.00 cash compared to $12.50 cash at Kestrel Commons (dining_halden_hall.txt and dining_kestrel_commons.txt).
```

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer (4 of 5) | MET | 5/5 in all three runs; every `answer_in` document was in the top 5 every time, so there's no generous reading involved. |
| 2 | Every answer names a source (5 of 5) | MET | All 15 answers contain a corpus filename; the strictest target I set, and it held in every run. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | 5/5 refused; the closest out-of-scope question (Mongolia, 0.825) is still 0.225 over the cutoff. |
| 4 | Rank-1 chunk is from the answer document (4 of 5) | MET — barely | 4/5 in all three runs, exactly on the target. The opposite case: one more wrong rank-1 misses it, and the library question shows the mechanism that would cause it. But the target was 4 of 5, it held 4 of 5 in every run, and the miss is the question I predicted would be hard. |
| 5 | Answer states the correct fact (4 of 5) | MET | 15/15 answers contained the expected fact. I also read the Halden/Kestrel answers by hand since the scorer only checks "Halden" appears; all three state Halden $10.00 vs Kestrel $12.50 correctly. |

## Diagnoses

**Nothing was missed.** That mostly says my targets were safe, not that the
system is excellent: four of five criteria cleared their target with room to
spare, on questions I chose knowing the corpus. If I were setting them again
I'd tighten criterion 1 and criterion 5 to **5 of 5** (both came out 15/15) and
criterion 4 to **5 of 5**, since it's the only one with real signal.

The two near-misses are still worth diagnosing, because they share a cause and
they're the first things that would break with harder questions:

1. **Criterion 4, the library question — stage: embedding/retrieval.** The
   answer document `study_library_hours.txt` ranks 2nd (0.450) behind
   `admin_library_holds.txt` (0.427). The whole post is embedded as a single
   384-dim vector, and both posts are overwhelmingly "about the library", so
   they land close together. The words that actually separate them — "reading
   week", "10pm" — are a handful of tokens in a 300-character post and barely
   move its vector. Generation recovered (it read the 2nd chunk), so the
   answer was right, but retrieval was wrong.

2. **The comparison question — stage: retrieval.** `dining_kestrel_commons.txt`
   came in **5th of 5** (0.598), behind North Kitchen (0.493) and Pellew
   (0.571), which the question never mentions. Every dining post has the same
   template ("Wait times: ... Hours are ... Costs one meal swipe, or $X cash"),
   so to the embedding they are all "a dining hall post about cost". The
   question's exact name, "Kestrel Commons", is the strongest signal and
   semantic search treats it as just more dining vocabulary. At top-k 4 this
   question would have failed criterion 1 and criterion 5.

**Pattern:** both are the same problem. The corpus is full of near-template
posts (7 dining, 7 laundry, 7 noise, 7 course triples) that differ only in
proper names and specific terms, and meaning-only retrieval underweights
exactly those exact terms.

## The Improvement

**What I changed:** hybrid search. `store.py::search` now ranks every chunk by
semantic distance *and* by BM25 keyword score (`rank-bm25`, lowercase
alphanumeric tokens, no stemming), and fuses the two rankings with reciprocal
rank fusion (`store.py::_fuse_with_bm25`, `RRF_K = 60`). Each result keeps its
cosine distance, so the relevance gate still judges meaning; only the *order*
of the top 5 changes. It's switched by `config.HYBRID` — `AI201_HYBRID=0` gives
the exact "before" system. Nothing else changed: same chunks, same index, same
top-k, same cutoff, same prompt.

**Why I picked it:** my diagnosis said meaning-only retrieval underweights the
exact names and terms ("reading week", "Kestrel Commons") that are the only
thing distinguishing this corpus's near-template posts — and keyword matching
is the direct fix for exact terms.

### Run Log — After

Source file: [`results/run_2026-10-04_2114_after.md`](results/run_2026-10-04_2114_after.md),
`run_eval.py::main`, 3 runs, cache off, 15 real model calls; aggregated by
`criteria_report.py::main`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Rank-1 chunk is from the answer document | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. Answer states the correct fact | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |

**Before vs after, side by side:**

| Criterion | Target | Before (R1/R2/R3) | After (R1/R2/R3) | Change |
|---|---|---|---|---|
| 1. Chunks contain the answer | 4 of 5 | 5/5 · 5/5 · 5/5 | 4/5 · 4/5 · 4/5 | worse |
| 2. Names a source | 5 of 5 | 5/5 · 5/5 · 5/5 | 5/5 · 5/5 · 5/5 | same |
| 3. Gate refuses out-of-corpus | 4 of 5 | 5/5 · 5/5 · 5/5 | 5/5 · 5/5 · 5/5 | same |
| 4. Rank-1 is the answer doc | 4 of 5 | 4/5 · 4/5 · 4/5 | 4/5 · 4/5 · 4/5 | same count, different question |
| 5. Correct fact | 4 of 5 | 5/5 · 5/5 · 5/5 | 4/5 · 4/5 · 4/5 | worse |

What moved, per question (`store.py::search` rankings, deterministic):

| Question | Before | After |
|---|---|---|
| Library in reading week | answer doc ranked **2nd** | ranked **1st** ✅ |
| Halden vs Kestrel | Kestrel ranked **5th** of 5 | ranked **3rd** ✅ |
| Withdrawal deadline | answer doc ranked **1st** | **not in top 5** ❌ |

Real output after the change — the withdrawal question, run 2:
```
- Best distance: 0.4581 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_pass_fail_option.txt, course_biol_160.txt, course_biol_160_workload.txt, course_engl_205.txt

You can drop (withdraw) through the end of week six, though a drop after week two shows as a W on your transcript. This information comes from `admin_add_drop_deadline.txt`.
```
The correct answer is week ten. Before the change, all three runs said "through week ten".

**Did it help?** No — it made the system worse, even though every criterion
still technically meets its target. It fixed both near-misses I diagnosed, but
it broke a question that was working, and broke it in the worst way: a
confident, sourced, *wrong* answer that passes the gate and names a real file.
Before, the one weakness (library ranked 2nd) still produced the right answer;
after, a retrieval failure turns into a wrong answer every run.

How I know why: `admin_withdrawal_deadline.txt` is semantic rank 1, but BM25
ranks it **21st of 88** (score 5.89), because the question says "withdraw" and
the document only ever says "withdrawal" — with no stemming those are different
tokens, so BM25 sees no match on the most important word. Meanwhile
`admin_add_drop_deadline.txt` is BM25 rank 1 (11.63): it matches "week" (three
times), "course", "can", "you". RRF scores: withdrawal 1/61 + 1/81 = 0.0287,
add/drop 1/62 + 1/61 = 0.0325 — and three course posts that say "week" a lot
also outrank it. Keyword search helps when the question uses the document's
exact words, and hurts when it uses a different form of them.

## What's Still Broken

No criterion is formally MISSED after the fix, but that's because my targets
allowed one failure each, not because nothing is broken:

- **Criteria 1 and 5 — the withdrawal question (introduced by my fix).** Next
  step: stem tokens before BM25 (e.g. a Porter stemmer, so withdraw/withdrawal
  → `withdraw`), and then re-run all three questions this change touched. I
  didn't add it because the rule for this unit is one change, and stemming is a
  second change that needs its own before/after. A cheaper alternative is to
  weight semantic rank above keyword rank in the fusion, since the gate already
  trusts semantic distance. If neither works, `AI201_HYBRID=0` returns to the
  "before" system, which was better on my test set.
- **Criterion 4 — still 4/5, now for a different reason.** The library miss is
  fixed; the remaining miss is the withdrawal question above, same fix.
- **The comparison question is still fragile.** Kestrel improved from 5th to
  3rd, but North Kitchen and Pellew still sit near it. Any question that names
  two halls needs both in the top k, and nothing in the system guarantees that.

I stopped here because the improvement is measured and explained, and further
changes would have made it impossible to say which change did what.

## What I'd Do Differently

- **Tighten criteria 1 and 5 to 5 of 5.** Both came out 15/15 before the
  change, so 4 of 5 couldn't catch anything. Worse, my fix *broke* a question
  and every criterion still said MET. A target that can't tell a better system
  from a worse one isn't doing its job.
- **Make criterion 4 5 of 5 too, and add more questions.** With five questions,
  "4 of 5" means one failure is always free. Ten questions, including more that
  word things differently from the documents ("withdraw" vs "withdrawal",
  "laundry" vs "dryer"), would have caught this regression without me
  reading the per-question output.
- **Track a per-question regression rule** ("no question that passed before may
  fail after"), because averages hid the one change that mattered here.

## How I Used AI (unit 2)

**3. Scorer and aggregation.** Claude wrote `scorer.py` (fact matching with
number-word and time normalisation) and `criteria_report.py`, which turns
run_eval's per-question file into per-criterion counts. Its first scorer failed
"every 40-minute loop" against "40 minutes", which a quick test caught before
the real run; it fixed the normalisation then. I read the Halden/Kestrel
answers by hand because the scorer only checks that "Halden" appears.

**4. Spotting the pattern and the regression.** Claude noticed that both near-
misses before the change were near-template posts told apart only by exact
names, which is why hybrid search was the fix. After the change it found the
withdrawal regression in the per-question output before I'd read it, and
checked the BM25 rank (21st of 88) to confirm the stemming explanation rather
than guessing.
