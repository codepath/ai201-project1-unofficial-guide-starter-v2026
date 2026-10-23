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

**Why this target:**
Most campus_life posts are a single short paragraph and the answer sits in one
sentence, so a whole post usually lands in one chunk and retrieval only has to
find the right post. I allow one miss rather than demanding 5 of 5 because my
question 5 (Halden vs Kestrel cash price) needs *two* documents in the top 5,
and question 2 has to pick Morrow House out of seven nearly identical laundry
posts. "Contains the answer" is checked against the `answer_in` documents I
listed in `questions.py` — every listed document must be among the retrieved
sources.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
All five, because naming a source isn't something retrieval can make hard:
every excerpt in the prompt is labelled `[from filename]` and the grounding
instruction in `generate.py` tells the model to name the file. If this misses,
it's the model ignoring an instruction, which is exactly what I want to catch.
"Names a source" means the answer contains a `.txt` filename from the corpus.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

I'm using the five shipped `OUT_OF_SCOPE` questions in `questions.py`.

**Why this target:**
Four of the five (Mongolia, diesel engines, the World Cup, Rust) share almost
no vocabulary with a corpus about dorms, dining and registration, so they
should be far from every chunk. The ibuprofen question is the risky one: it's
health-related and `health_center.txt` exists, so it may land closer than the
others. Allowing one let-through covers that one case; letting two through
would mean the cutoff isn't doing its job.

---

## 4. Something about your chunks

For at least 4 of my 5 test questions, the **top-ranked** chunk (rank 1)
comes from one of the documents listed in `answer_in` for that question.

**Why this target:**
Because posts are short (about 317 characters on average, longest 554), each
chunk is a whole post. That keeps answers from being split, but it also means
chunks are *large relative to the fact being asked about* — a laundry post is
mostly boilerplate ("eight washers and six dryers... Sunday after 6pm you will
wait") that is word-for-word identical across seven buildings. Criterion 1 only
asks that the right chunk is somewhere in the top 5; this asks whether my chunks
are distinctive enough that the right one wins. 4 of 5 because question 5 has
two right documents and only one can be first.
---

## 5. Your choice

For at least 4 of my 5 test questions, the answer states the correct fact —
it contains the `expects` value from `questions.py` (or the same fact written
differently, e.g. "week 10" for "week ten") — in every one of the three runs.

**Why this target:**
Criteria 1–3 can all pass while the answer is still wrong: the right chunk can
be retrieved and a source named, and the model can still read the wrong
building's price or the drop deadline instead of the withdrawal one. This is
the one I actually care about as a user. 4 of 5 rather than 5 of 5 because the
library question has seven distractor chunks saying "open until 2am", and I
expect the model to be pulled toward that at least sometimes.


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
