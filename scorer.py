"""
Decides whether an answer was right. `run_eval.py` finds this file and calls
`judge` once per question per run.

"Right" means the answer contains the `expects` value from questions.py, after
normalising the ways the same fact gets written: case, "week 10" vs "week ten",
"10pm" vs "10 p.m." vs "10:00 pm". This is criterion 5 in criteria.md.

It is deliberately strict in one way: a refusal is always a fail, even if the
question happened to be hard. And it is deliberately loose in another: it only
checks that the fact appears, not that the sentence around it is correct — so a
comparison answer ("Halden") still gets read by hand in the run log.
"""

import re

NUMBER_WORDS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "eleven": "11", "twelve": "12", "fifteen": "15", "twenty": "20",
    "forty": "40",
}


def normalise(text: str) -> str:
    text = text.lower()
    for word, digit in NUMBER_WORDS.items():
        text = re.sub(rf"\b{word}\b", digit, text)
    text = re.sub(r"(\d+):00", r"\1", text)          # 10:00pm -> 10pm
    text = re.sub(r"(\d+)\s*p\.?\s*m\.?", r"\1pm", text)
    text = re.sub(r"(\d+)\s*a\.?\s*m\.?", r"\1am", text)
    text = re.sub(r"(\d+)-minutes?\b|(\d+) minutes\b",
                  lambda m: f"{m.group(1) or m.group(2)} minute", text)
    text = re.sub(r"\s+", " ", text)
    return text


def judge(question, expects, answer, results) -> bool:
    if not expects or not answer:
        return False
    if "don't have enough information" in answer.lower():
        return False
    return normalise(expects) in normalise(answer)
