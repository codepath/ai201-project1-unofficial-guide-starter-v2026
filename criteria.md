# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** tested all my 5 questions and each of them retrieves the right thread as the first result at distance of 0.23-0.40. because the corpus of advice threads has 23 threads and one chunck per topic. if a wording in question drifts then there is no second chunck to fall back on. 4 out of 5 lives room for one wording mismatch.

<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** the pipeline attaches the source filename to every chunk before the model ever sees it, so naming a source doesn't depend on the model being smart, just on the plumbing working. that's why it's all 5 and not 4. if an answer comes back with no source it means my code dropped the label somewhere, not that I got unlucky.

<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:** I measured both groups with the retrieve command. my 5 real questions came back at 0.23-0.40 and the 5 out of scope questions came back at 0.83-0.95, so there was a clean gap between 0.40 and 0.83 with no overlap at all. I put the cutoff at 0.65 because it sits in the middle of that gap with margin on both sides. the target is 4 of 5 instead of 5 of 5 because the closest out of scope question (ibuprofen, 0.83) is still the nearest thing to the gap and a differently worded junk question could land closer.

> **Revised in unit 2:** When I ask a campus-adjacent question my documents
> don't cover (one that sounds like my corpus but has no answer in it, like
> "What time does the gym open?"), the gate stops it in at least 4 of 5 tries.
>
> **Why revised:** the original measured the wrong thing. The five OUT_OF_SCOPE
> questions are from a different world entirely and score 0.83-0.95, so the
> criterion could not fail no matter what cutoff I picked. But the claim is
> about "questions my documents clearly don't cover", and the dangerous ones
> are campus questions with no answer in the corpus. I measured five of those:
> gym hours 0.638, grade appeals 0.639, dorm food 0.606, overnight parking
> 0.538, housing lottery 0.725. At my 0.65 cutoff the gate refuses only 1 of 5.
> So the original criterion was passing while the thing it claimed to measure
> was failing. The original verdict stands as MET against its own question set;
> the revised version is currently MISSED, and that miss is what unit 2's
> improvement targets.

<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

---

## 4. Something about your chunks

Every chunk is one complete thread: it starts with a `THREAD:` title line and no reply is cut off mid sentence, in 5 of 5 sampled chunks.

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

**Why this target:** when I looked at what the fallback chunker did to my corpus it cut replies in half at the 800 character mark, and one retrieved chunk literally started mid word ("t...."). the THREAD: title line is what carries the question that the replies are answering, so a chunk without it matches questions badly. it's 5 of 5 and not 4 of 5 because my chunker splits on thread boundaries, so if even one sampled chunk is broken that means the code is wrong, not that I got unlucky.

---

## 5. Your choice

For questions whose thread contains conflicting replies, the answer reflects both positions instead of picking one, in at least 2 of 3 such test questions.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

**Why this target:** my corpus is advice threads and the replies disagree with each other on purpose. the bike thread has one reply saying yes get a bike, one saying no I sold mine, and one saying keep a cheap one for fall only. the honest answer is "it depends on the season" and the vote counts tempt the model to just crown the most upvoted reply as the winner. I picked 2 of 3 instead of 3 of 3 because in some threads one side is clearly fringe (like 5 votes against 31) and deciding whether the answer should still mention it is a judgment call I might score differently on different days.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
