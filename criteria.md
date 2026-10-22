# Acceptance criteria — The Unofficial Guide

These are my five Unit 1 acceptance criteria. The original targets and reasons are preserved below. Clarifications added after grading feedback are labeled explicitly; they do not change the targets.

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
We want to generate and provide users with accurate results. We may also not have enough documentation to generate 5 correct answers all the time so this accepts that retrieval may miss relevant information. So retrieval might not generate an accurate answer even though the answer exists in the documents in my questions.

**Post-feedback clarification:** All five test questions have answers in the campus_life documents. The possible failure is retrieval selecting the wrong chunks, not missing documentation. Similar topics such as dropping and withdrawal, and misspellings in the withdrawal question, make retrieval imperfect. The 4-of-5 target allows one retrieval miss while requiring success on most questions; generation is a separate stage.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
This generates credibility for everything that they say and also gives us a way to trace back. Knowing that every provided answer has a source will create more confidence when the user uses it for something else.

**Post-feedback clarification:** Each retrieved chunk carries its source filename, and the grounding instruction tells the model to name that file. That makes a source citation a reasonable requirement for every substantive answer, rather than accepting one uncited answer. A citation lets the user trace campus advice back to its post; it does not by itself prove that the answer is correct.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
This is to ensure that we are not providing information that we don't have knowledge of. I expect 4 unrelated questions to be refused because my first criteria says at least 4 of my 5 test will contain the answer

**Post-feedback clarification:** This target is independent of criterion 1 and uses the five different questions in OUT_OF_SCOPE, not repeated searches for one answer. A similarity cutoff can admit an unrelated question that resembles campus text, so 4 of 5 allows one mistaken acceptance. In the recorded measurements, in-corpus distances were 0.2302–0.3938 and out-of-scope distances were 0.8236–0.8859; the 0.6 cutoff separated these examples.

---

## 4. Chunks contain at most three body sentences

Chunks should be concise with as little details needed to provide a correct answer and support it.
Maximum of 3 sentences. We don't wan't to overflow the user with information.

**Why this target:**
We don't want to overflow the user with irrelevant data that they may not need.

**Post-feedback clarification:** The maximum applies to three body sentences per chunk, excluding the repeated title, and can be checked on the generated chunks. Campus posts contain several short facts about courses, housing, or dining, so grouping a few complete sentences keeps retrieval focused while the title identifies the topic. This is a chunk-size target, not a promise about final answer length.

---

## 5. Every response ends with a relevant follow-up question

Ask user a question at the end of every response for things that could give them more information if they want.
If they asked about printing cost. Then you can followup with "would you like to know where to access printers"

**Why this target:**

One of the questions ask about how much to print. But the user may not know where to access a printer or relevant information. Asking them if they would like to know more will give them all the information they need.

**Post-feedback clarification:** The target remains a relevant follow-up question at the end of every response. It is observable by inspecting the final sentence. Campus questions often lead to related practical needs, such as printing locations after asking about printing costs. This is an acceptance target, not a claim that the current implementation meets it: the recorded sample answer has no follow-up question.

---
