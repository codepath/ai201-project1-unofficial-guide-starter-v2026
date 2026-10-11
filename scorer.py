"""Decides whether an answer counts as correct. run_eval.py imports this."""

from gate import REFUSAL


def judge(question: str, expects: str, answer: str, results) -> bool:
    if not expects:
        return False

    # A refusal is never a correct answer to an in-scope question.
    if not answer or answer.strip() == REFUSAL:
        return False

    # expects can hold alternatives separated by |, e.g. "two|2".
    # The answer passes if any alternative appears, ignoring case.
    answer_lower = answer.lower()
    return any(
        option.strip().lower() in answer_lower
        for option in expects.split("|")
        if option.strip()
    )
