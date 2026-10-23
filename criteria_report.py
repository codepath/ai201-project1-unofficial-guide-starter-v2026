#!/usr/bin/env python3
"""
Turn one results/ file from run_eval.py into the per-CRITERION counts the
README's run log wants.

    python criteria_report.py results/run_..._before.md

run_eval.py writes one row per question. This reads its "Real output" section
back and counts, for each run, how many questions met each criterion as defined
in criteria.md:

  1. every document in `answer_in` is among the retrieved sources
  2. the answer names a corpus .txt file
  3. the gate refused the out-of-scope question (one deterministic pass)
  4. the rank-1 chunk is one of the `answer_in` documents (retrieval is
     deterministic, so this re-runs `store.search` once per question)
  5. scorer.judge says the answer contains the expected fact

It changes nothing about the system — it only reads what a run produced.
"""

import re
import sys
from pathlib import Path

import config
import questions as qs
import scorer

HEADING = re.compile(r"^### (.+) — run (\d+)$")


def parse(path: Path):
    """Pull (question, run) -> {sources, answer} out of the Real output section."""
    lines = path.read_text(encoding="utf-8").splitlines()
    entries, gate_refused, gate_total = {}, 0, 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("| ") and line.rstrip().endswith(("| refused |", "| **let through** |")):
            gate_total += 1
            gate_refused += line.rstrip().endswith("| refused |")
        m = HEADING.match(line)
        if m:
            question, run = m.group(1), int(m.group(2))
            sources = []
            while not lines[i].startswith("```"):
                if lines[i].startswith("- Sources retrieved:"):
                    sources = [s.strip() for s in lines[i].split(":", 1)[1].split(",")]
                i += 1
            i += 1
            body = []
            while not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            entries[(question, run)] = {"sources": sources, "answer": "\n".join(body)}
        i += 1
    return entries, gate_refused, gate_total


def main():
    path = Path(sys.argv[1])
    entries, gate_refused, gate_total = parse(path)
    runs = sorted({run for _, run in entries})
    corpus_files = {p.name for p in config.corpus_path().glob("*.txt")}

    from store import search
    top1 = {q["question"]: search(q["question"], top_k=config.TOP_K)[0].source
            for q in qs.answered()}

    counts = {c: {r: 0 for r in runs} for c in (1, 2, 4, 5)}
    detail = []
    for q in qs.answered():
        question, wanted = q["question"], set(q["answer_in"])
        for run in runs:
            e = entries[(question, run)]
            c1 = wanted <= set(e["sources"])
            named = set(re.findall(r"[\w\-]+\.txt", e["answer"])) & corpus_files
            c2 = bool(named)
            c4 = top1[question] in wanted
            c5 = scorer.judge(question, q["expects"], e["answer"], [])
            for c, ok in ((1, c1), (2, c2), (4, c4), (5, c5)):
                counts[c][run] += ok
            detail.append((question, run, c1, c2, c4, c5, top1[question]))

    n = len(qs.answered())
    print(f"From {path}\n")
    print("| Criterion | " + " | ".join(f"Run {r}" for r in runs) + " |")
    print("|---|" + "---|" * len(runs))
    names = {1: "1. Retrieved chunks contain the answer",
             2: "2. Every answer names a source",
             4: "4. Rank-1 chunk is from the answer document",
             5: "5. Answer states the correct fact"}
    for c in (1, 2):
        print(f"| {names[c]} | " + " | ".join(f"{counts[c][r]}/{n}" for r in runs) + " |")
    print("| 3. Gate stops out-of-corpus questions | "
          + " | ".join(f"{gate_refused}/{gate_total}" for _ in runs) + " |")
    for c in (4, 5):
        print(f"| {names[c]} | " + " | ".join(f"{counts[c][r]}/{n}" for r in runs) + " |")

    print("\nPer question (c1 c2 c4 c5, rank-1 source):")
    for question, run, *flags, first in detail:
        marks = " ".join("Y" if f else "n" for f in flags)
        print(f"  run {run}  {marks}  {first:<38} {question}")


if __name__ == "__main__":
    main()
