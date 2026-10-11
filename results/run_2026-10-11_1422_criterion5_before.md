# Criterion 5 runs — before

- Produced by: a manual loop over `generate.py::answer_from_chunks` with cache off,
  same retrieval and gate as `run_eval.py::run_once`.
- Questions: the two in `questions.py::CONFLICT_QUESTIONS` not already in QUESTIONS
  (the bike question's three runs are in the main before run log).
- Corpus: `advice_threads`, top-k 5, cutoff 0.65
- When: 2026-10-11 14:22

### Is a parking permit worth getting? — run 1

- Best distance: 0.3708 (passed the gate)

```
According to thread_parking.txt, a west permit is worth getting if you are commuting daily; otherwise, it is not worth bothering.
```

### Is a parking permit worth getting? — run 2

- Best distance: 0.3708 (passed the gate)

```
A west permit is worth getting if you are commuting daily, but otherwise you should not bother (thread_parking.txt).
```

### Is a parking permit worth getting? — run 3

- Best distance: 0.3708 (passed the gate)

```
Whether a parking permit is worth getting depends on your commuting frequency and which lot you choose. If you are commuting daily, a west lot permit is worth the August scramble; otherwise, it is not worth bothering (*thread_parking.txt*). The west lots sell out in about three days in August, while the east lot never sells out, though it is a 12-minute walk (*thread_parking.txt*).
```

### Does the edition of the textbook matter? — run 1

- Best distance: 0.4983 (passed the gate)

```
For math and physics, the textbook edition almost never matters, as only the problem numbering shifts. However, for fields that change, it can matter a lot, and you should ask your instructor directly if the previous edition is fine (thread_textbook_editions.txt).
```

### Does the edition of the textbook matter? — run 2

- Best distance: 0.4983 (passed the gate)

```
For math and physics, the edition almost never matters (problem numbering just shifts), but for fields that move, it can matter a lot (thread_textbook_editions.txt). Most instructors will tell you a previous edition is fine if you ask them directly (thread_textbook_editions.txt).
```

### Does the edition of the textbook matter? — run 3

- Best distance: 0.4983 (passed the gate)

```
According to **thread_textbook_editions.txt**, the edition of the textbook almost never matters for maths and physics (only problem numbering shifts), but it can matter a lot for fields that move. You should ask the instructor directly, as most will say the previous edition is fine.
```
