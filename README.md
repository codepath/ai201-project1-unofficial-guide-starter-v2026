# The Unofficial Guide

Fatima Rahimi, advice_threads corpus

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

This is a question answering system built on the advice_threads corpus, 23 forum threads where students answer each other's practical questions about campus life: laundry timing, laptop specs, meal plans, bike commuting, that kind of thing. You ask it a question, it finds the thread closest in meaning to your question, and a model writes a short answer from that thread only, naming the file it came from. If your question isn't something the threads cover, a relevance gate refuses to answer instead of letting the model make something up.

## Chunking Strategy

**Chunk size: one whole thread (317–793 characters)**
**Overlap: none**

Each file in my corpus is one thread: a `THREAD:` title that states the question, then the replies that answer it. The replies only make sense under the title. "Counterpoint, I sold mine" is useless without knowing the question was about bikes, so cutting anywhere inside a thread separates answers from their question. I measured the threads and the longest is 793 characters, under the embedding model's roughly 1000 character limit, so nothing needs splitting and one thread = one chunk.

I changed my mind to get here. I first experimented with small fixed-size chunks through the fallback splitter, and when I looked at what retrieval brought back, some chunks were cut mid reply and one literally started mid word ("t...."). That's what convinced me the thread boundary is the only place a cut makes sense in this corpus. If a longer thread ever shows up, my plan is one chunk per reply with the `THREAD:` title line prepended to each.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.

--- reply 3 (22 votes) ---
Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

--- reply 4 (5 votes) ---
If you do get one, the campus does free registration and it's the only reason I got mine back after it was taken.
```

**Chunk 2** — source: `thread_first_year_regret.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: What do you wish you'd known in first year?

--- reply 1 (41 votes) ---
That the add/drop deadline and the withdrawal deadline are different dates and only one of them is on the calendar everyone reads.

--- reply 2 (28 votes) ---
That you can take a course pass/fail and declare it late — up to week eight. I carried a grade I didn't need to.

--- reply 3 (35 votes) ---
That the writing centre will read a draft for any course, not just writing courses. Free, and the appointments go unbooked.

--- reply 4 (52 votes) ---
Honestly: that nobody is watching as closely as you think. I spent a year worried about looking like I knew what I was doing.

--- reply 5 (17 votes) ---
That your adviser's job is partly to know the exceptions to rules. Ask before assuming a deadline is fixed.
```

**Chunk 3** — source: `thread_laundry_timing.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: When is laundry actually free in the dorms?

--- reply 1 (27 votes) ---
Tuesday and Wednesday mornings, every building. Sunday evening is the worst and it isn't close.

--- reply 2 (8 votes) ---
Depends heavily on your building. Morrow has more machines per person than Fenwick so it's less of a problem there.

--- reply 3 (16 votes) ---
The app that shows machine availability is wrong about half the time. It reports a machine as free for a few minutes after it finishes but before someone unloads it.
```

**Chunk 4** — source: `thread_printing.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Is the printing quota enough?

--- reply 1 (17 votes) ---
For most people yes. $30 is about 600 pages black and white. It's the colour printing that eats it — eight times the cost per page.

--- reply 2 (11 votes) ---
Doesn't roll over between semesters. Print your readings in December rather than losing it.
```

**Chunk 5** — source: `thread_roommate_conflict.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Roommate situation isn't working. What now?

--- reply 1 (28 votes) ---
Talk to your RA early, and frame it as 'we need help sorting this out' rather than 'move me'. Room changes are possible but the process starts with mediation and skipping that step slows it down.

--- reply 2 (14 votes) ---
Room changes happen at the semester boundary almost always, and mid-semester only in fairly serious cases.

--- reply 3 (33 votes) ---
Write down specifics before the meeting. 'It's not working' is hard to act on; 'guests four nights a week past 2am' is not.
```

## Sample Answer

**Question:** When are the dorm laundry machines actually free?

**Answer:**

```
  (best distance 0.270, cutoff 0.65)

Laundry is actually free in all buildings on Tuesday and Wednesday mornings.

Source: thread_laundry_timing.txt
```

**My relevance cutoff:** 0.65

I ran my five test questions and the five OUT_OF_SCOPE questions through `python app.py retrieve` and wrote down the best distance for each. The two groups came out with a clean gap: everything my corpus covers scored 0.23–0.40, and everything it doesn't scored 0.83–0.95, with nothing in between. I put the cutoff at 0.65 because it sits in the middle of that gap with margin on both sides: low enough that no junk question gets through, high enough that a slightly awkwardly worded real question still passes. I originally had it at 0.85, which turned out to be too loose: two of the five out-of-scope questions would have gotten past the gate and reached the model.

| Question | In corpus? | Best distance |
| -------- | ---------- | ------------- |
| Is it worth getting a bike to shorten my walk to campus? | yes | 0.233 |
| How much RAM do students say you actually need for CS courses? | yes | 0.259 |
| How many courses can I take pass fail in a year? | yes | 0.274 |
| What time of week is it easiest to find an open washing machine in the dorms? | yes | 0.366 |
| How many black and white pages does the printing quota cover? | yes | 0.399 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.828 |
| How do I write a for loop in Rust? | no | 0.871 |
| How do I change the oil in a diesel engine? | no | 0.930 |
| What is the capital of Mongolia? | no | 0.948 |
| Who won the 1994 World Cup? | no | 0.952 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I had set my relevance cutoff to 0.85 and asked Claude whether it was right. It ran my five out-of-scope questions through retrieval and showed me that two of them (ibuprofen at 0.79, the World Cup at 0.83 on the old index) came in under 0.85, meaning the gate would have passed them through to the model, so my own criterion 3 would have failed at 3 of 5. I moved the cutoff to 0.65, inside the gap between my two groups of distances, and re-verified that all five junk questions now get refused.

**2.** I asked Claude to explain `chunker.py` line by line and suggest improvements. It suggested one thread = one chunk and backed it up by measuring my corpus (23 threads, 317–793 characters each, all under the embedding model's input limit). I also learned from the retrieval output that my old index had chunks cut mid-word. The index was stale from an earlier chunk-size experiment, and I hadn't realized the index only changes when you rebuild it. After changing the chunker I re-indexed and re-ran all ten retrieve commands to confirm the distances myself; the out-of-scope group actually moved further away (0.79 → 0.83 at the closest).

**3.** (unit 2) My scorer wasn't producing verdicts and I asked Claude why. It found two problems I'd missed: my file was named `score.py` but `run_eval.py` imports `scorer`, and my one-liner had a parenthesis bug, `(answer or "".lower())` lowercases the empty string instead of the answer, so "tuesday" could never match "Tuesday". It rewrote `judge` with the fix plus refusal handling and tested it against six known answers before I re-ran the eval.

**4.** (unit 2) I asked Claude to read all 23 threads and find edge cases worth testing. It measured campus-adjacent questions my corpus can't answer and found they score 0.54 to 0.64, under my then cutoff of 0.65, while my out-of-scope test set scored 0.83 plus. That became my criterion 3 revision, my diagnosis, and my improvement. I also used the "argue the opposite verdict" exercise from the milestone on my five verdicts; the argument against criterion 5 was good (one bike answer led with "yes"), so I re-scored it strictly and reported the 2/3 runs.

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

| Criterion                              | Target | Run 1 | Run 2 | Run 3 | Verdict |
| -------------------------------------- | ------ | ----- | ----- | ----- | ------- |
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5   | 5/5   | 5/5   | MET     |
| 2. Every answer names a source         | 5 of 5 | 5/5   | 5/5   | 5/5   | MET     |
| 3. Gate stops out-of-corpus questions  | 4 of 5 | 5/5   | 5/5   | 5/5   | MET     |
| 4. Every chunk is one complete thread  | 5 of 5 | 5/5   | 5/5   | 5/5   | MET     |
| 5. Conflicting replies shown both ways | 2 of 3 | 3/3   | 3/3   | 2/3   | MET     |

The evidence files are `results/run_2026-10-11_1411_before.md` (criteria 1 to 3,
scored by `scorer.py::judge`) and `results/run_2026-10-11_1422_criterion5_before.md`
(criterion 5). Criteria 3 and 4 are measured in one deterministic pass, so the
same number fills all three run columns. Criterion 1 counts whether the sources
retrieved for each question include the thread that holds the answer, and
retrieval is deterministic too, so its runs match; criteria 2 and 5 depend on
the generated answer and genuinely could have varied, they just didn't.

**Criterion 1** (retrieval, from `run_eval.py::main` via `store.py::search`): for
every question the retrieved sources include the right thread, for example:

```
### What time of week is it easiest to find an open washing machine in the dorms? — run 1
- Best distance: 0.3658 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_late_work.txt, thread_laundry_timing.txt, thread_sleep_schedule.txt, thread_study_spots.txt
```

**Criterion 2** (source naming, answer produced by `generate.py::answer_from_chunks`):
all 15 answers name their source file. One of them:

```
The printing quota of $30 covers about 600 black and white pages. (Source: thread_printing.txt)
```

**Criterion 3** (the gate, from `run_eval.py::check_out_of_scope`, cutoff 0.65):

```
| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.948 | refused |
| How do I change the oil in a diesel engine? | 0.930 | refused |
| Who won the 1994 World Cup? | 0.952 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.828 | refused |
| How do I write a for loop in Rust? | 0.871 | refused |
```

**Criterion 4** (chunks, from `python app.py chunks -n 5`, chunks produced by
`chunker.py::split_documents`): all five sampled chunks are complete threads
starting with their title line:

```
Chunk 1  |  source: thread_bike_commute.txt#0  |  produced by: chunker.py::split_documents
THREAD: Is a bike worth it for a 20 minute walk commute?
```

**Criterion 5** (conflicting replies, questions from `questions.py::CONFLICT_QUESTIONS`,
answers by `generate.py::answer_from_chunks` with cache off): parking and textbook
kept both sides in every run; the bike answer did too in runs 1 and 2 but led with
"yes" in run 3, which I scored as a fail, leaving run 3 at 2 of 3. One of the
clean ones:

```
According to thread_parking.txt, a west permit is worth getting if you are
commuting daily; otherwise, it is not worth bothering.
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
| - | --------- | ------- | ------------- |
| 1 | Retrieved chunk contains the answer | MET | the sources retrieved for every question include the thread that holds the answer, in all three runs (5/5, target 4/5). retrieval is deterministic, so one check per question settles it. |
| 2 | Every answer names a source | MET | I read all 15 answers in the before log rather than trusting the scorer for this one; every single answer names a thread file (15/15, target all). |
| 3 | Gate stops out-of-corpus questions | MET | the gate refused all 5 OUT_OF_SCOPE questions, closest at 0.828 against the 0.65 cutoff. but this verdict is softer than it looks: the question set made it unmissable, see the revision under criterion 3 in criteria.md. |
| 4 | Every chunk is one complete thread | MET | all 5 sampled chunks start with their THREAD: line and end at the thread's end. the chunker emits whole files, so a broken chunk is impossible by construction, which is why one sample pass is enough. |
| 5 | Conflicting replies shown both ways | MET | parking and textbook answers kept the disagreement in all runs. bike run 3 was borderline, it led with "yes" and kept the downsides as caveats, so I scored it strictly as a fail, and the run still comes out 2 of 3, which meets the target. |

## Diagnoses

**The one miss: criterion 3 as revised.** The gate refuses only 1 of 5
campus-adjacent questions my documents don't cover (gym hours 0.638, grade
appeals 0.639, dorm food 0.606, overnight parking 0.538, all under the 0.65
cutoff; only the housing lottery at 0.725 gets refused).

**Stage: the gate, fed by embedding distances.** Not loading, chunking, or
generation. I checked by working backwards: for the gym question none of the
five retrieved chunks contains anything about a gym, so the problem is before
generation, and retrieval itself did nothing wrong, it returned the closest
chunks that exist. The failure is that the gate let the question through.

**Mechanism:** embedding distance measures how topically close a question is
to my corpus, not whether the corpus answers it. A question about gym hours
shares the campus vocabulary of my threads (buildings, schedules, student
life), so it lands at 0.638, while truly alien questions land at 0.83 plus.
And the gap I would need does not exist: "What do students say about Fenwick?"
is answerable from three threads and scores 0.628, which is further than the
unanswerable overnight parking question at 0.538. Answerable and unanswerable
campus questions overlap on this one number, so no cutoff separates them.
Lowering the cutoff to refuse the gym question would also refuse the Fenwick
question.

**Pattern:** all four leaked questions are the same single problem, campus
vocabulary without campus answers, not four separate failures.

**What actually happens after the leak:** I asked two of the leaked questions
end to end. Both times the model itself refused ("I do not have enough
information to answer this question"), because the grounding instruction in
`generate.py` tells it to answer only from the documents. So the second
defence layer currently catches what the gate misses. The cost of the miss is
a wasted model call per leaked question and the fact that I am relying on the
model following instructions, which gate.py's own comments warn is the less
reliable layer.

**On the five original criteria, which were all MET:** honestly, criteria 1,
2, and 4 were never in danger, because with one chunk per thread and only 23
threads, retrieval is close to a lookup table. The safe one was criterion 3,
and the revision above is the tightening: measured against campus-adjacent
questions it goes from unmissable to 1 of 5. If I tightened one more, it would
be criterion 2, from "names a source" to "names the correct source", which my
before run already satisfies 15 of 15 but which an answer could fail while
passing the current wording.

## The Improvement

**What I changed:** one number: the relevance cutoff in config.py, from 0.65
to 0.6.

**Why I picked it:** my diagnosis showed the gate letting through 4 of 5
campus-adjacent questions my corpus can't answer, and three of those four
(gym 0.638, grade appeals 0.639, dorm food 0.606) sit between 0.6 and 0.65,
so this is the change the diagnosis directly names. Before making it I wrote
down why it might not work: it moves the line instead of fixing the mechanism
(overnight parking at 0.538 still leaks whatever I do), and it sacrifices
answerable aggregation questions like the Fenwick one at 0.628, which now get
refused.

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion                              | Target | Run 1 | Run 2 | Run 3 | Verdict |
| -------------------------------------- | ------ | ----- | ----- | ----- | ------- |
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5   | 5/5   | 5/5   | MET     |
| 2. Every answer names a source         | 5 of 5 | 5/5   | 5/5   | 5/5   | MET     |
| 3. Gate stops out-of-corpus questions  | 4 of 5 | 5/5   | 5/5   | 5/5   | MET     |
| 4. Every chunk is one complete thread  | 5 of 5 | 5/5   | 5/5   | 5/5   | MET     |
| 5. Conflicting replies shown both ways | 2 of 3 | 3/3   | 2/3   | 2/3   | MET     |

The evidence files are `results/run_2026-10-11_1429_after.md` and
`results/run_2026-10-11_1429_criterion5_after.md`. Criterion 5's 2/3 cells are
me scoring the bike answers strictly, same as in the before run: two of them
led with "yes" and kept the other side as caveats.

**And the revised criterion 3**, the one the improvement was aimed at,
measured against the five campus-adjacent questions from the Diagnoses
section (one deterministic pass, like the gate itself):

| Measurement | Before (cutoff 0.65) | After (cutoff 0.6) | Target | Verdict |
| --- | --- | --- | --- | --- |
| Gate refuses campus-adjacent uncovered questions | 1 of 5 | 4 of 5 | 4 of 5 | MET |

**Did it help?**

Yes, and I can say how I know in one sentence: the revised criterion 3 went
from 1 of 5 to 4 of 5 refused, and no other criterion moved. My five real
questions all score 0.399 or lower, so the lower cutoff never touches them
(same distances, same 15 passes as before). The two costs I predicted both
showed up and are worth it: the overnight parking question (0.538) still gets
past the gate and is still caught by the grounding instruction instead, and
the answerable Fenwick-style aggregation question (0.628) is now refused,
which I'm accepting because none of my criteria cover aggregation questions
and the gate protecting against confident wrong answers matters more than
answering a question type I never promised.

## What's Still Broken

**The revised criterion 3 is at 4 of 5, not 5 of 5.** The overnight parking
question (0.538) still gets past the gate, and no cutoff can stop it: it
scores closer to my corpus than an answerable question does (the Fenwick
aggregation question at 0.628). What I'd do about it: stop trying to fix this
with the distance threshold, because the mechanism (embedding distance measures
topic, not answerability) doesn't give me the signal I need. The honest fix is
to treat the grounding instruction as the formal second layer and measure its
refusal reliability the way I measure everything else, three runs per leaked
question, since gate.py's comments warn that asking the model nicely is the
less reliable layer and so far I've only seen it refuse a handful of times.
Why I stopped: the milestone said one change, the leak is currently caught by
that second layer in every test I ran, and a proper fix needs a different
mechanism, not another number.

**The improvement has a cost I accepted but didn't fix.** Answerable
aggregation questions like "What do students say about Fenwick?" (0.628) are
now refused by the lower cutoff. What I'd do about it: a gate that looks at
more than the single best distance, for example how many of the top chunks
are close, since the Fenwick question has three moderately close threads
while the gym question has none. Why I stopped: none of my five criteria
cover aggregation questions, so fixing this would be improving something I
never promised while the unit asked me to fix something I did.

**Criterion 5 is met but drifting.** Two of three bike runs in the after log
led with "yes" and kept the other side as caveats, which I scored as fails
under my strict reading. What I'd do about it: add one rule to the grounding
instruction in generate.py, "if the replies disagree, present both sides
instead of picking one". Why I stopped: the criterion was met, and adding a
prompt change on top of the cutoff change would have been a second change in
the same measurement, which is exactly what the milestone said not to do.

## What I'd Do Differently

**Criterion 3 taught me the big lesson: test with near misses, not easy
misses.** I wrote my out-of-scope questions from a different world entirely
(Mongolia, Rust, diesel engines) and they all scored 0.83 plus, so the
criterion could not fail. The questions that actually probe the gate are
campus questions with no answer in the corpus, which score 0.54 to 0.64,
right at the cutoff. Next unit I'd write the out-of-scope set as the five
nearest misses I can think of, not the five farthest.

**Criterion 5 I'd define precisely enough to score the same way twice.**
"Reflects both positions" turned out to be a judgment call: I scored answers
that led with "yes" but kept the downsides as caveats differently on
different passes before forcing myself to a strict rule. Next time I'd write
the rule into the criterion itself, something like "the answer does not open
with an unqualified yes or no when the thread's replies disagree".

**Criteria 1, 2, and 4 I'd tighten, because they were nearly unmissable.**
With 23 whole-thread chunks, retrieval is close to a lookup table. I'd move
criterion 1 to "the answer-bearing chunk is the number one result" and
criterion 2 to "names the correct source, not merely a source". Both happen
to hold in my runs, so they'd be real targets rather than safe ones.
