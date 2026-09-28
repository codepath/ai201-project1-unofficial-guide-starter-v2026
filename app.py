#!/usr/bin/env python3
"""
The Unofficial Guide — command line.

    python app.py index                  build the search index (do this first)
    python app.py ask "your question"    ask one question
    python app.py ask                    ask questions until you quit
    python app.py chunks                 print sample chunks      (Milestone 3)
    python app.py retrieve "question"    show distances, no answer (Milestone 4)
    python app.py corpora                list the available corpora

Every command takes --corpus NAME to work with a different corpus without
editing config.py.
"""

import argparse
import sys
import time

import config


def cmd_corpora(args):
    from corpus_info import list_corpora

    for name, blurb in list_corpora():
        marker = "*" if name == config.CORPUS else " "
        print(f"{marker} {name}")
        print(f"    {blurb}\n")
    print("* = current default, set in config.py (AI201_CORPUS in .env wins)")


def cmd_index(args):
    from chunker import describe as describe_chunks
    from chunker import split_documents
    from ingest import describe as describe_docs
    from ingest import load_documents
    from store import build_index

    corpus = args.corpus or config.CORPUS
    print(f"Corpus: {corpus}")

    started = time.time()

    documents = load_documents(corpus)
    print(f"  loaded   {describe_docs(documents)}")

    chunks = split_documents(documents)
    print(f"  chunked  {describe_chunks(chunks)}")

    print(f"  embedding {len(chunks)} chunks (first run downloads the model)...")
    count = build_index(chunks, corpus=corpus, variant=args.variant)

    elapsed = time.time() - started
    print(f"  stored   {count} chunks in {elapsed:.1f}s")
    print(f"\nReady. Try: python app.py ask \"your question here\"")


def _chunks_from_doc(chunks, wanted):
    """Every chunk that came out of one source document, in order.

    This is the sample to use when you re-chunk and want to compare. The
    default sample is taken by stride across the whole corpus, so as soon as a
    new chunker changes the chunk count it lands on different documents and
    there is nothing to compare. One named document's chunks are the same
    material before and after, however many pieces it was cut into.
    """
    matches = [c for c in chunks if c.source == wanted]
    if not matches:
        matches = [c for c in chunks if wanted.lower() in c.source.lower()]
    if not matches:
        sources = sorted({c.source for c in chunks})
        raise SystemExit(
            f"No document matching '{wanted}'. This corpus has:\n  "
            + "\n  ".join(sources)
        )
    found = sorted({c.source for c in matches})
    if len(found) > 1:
        raise SystemExit(
            f"'{wanted}' matches more than one document:\n  "
            + "\n  ".join(found)
            + "\nBe more specific."
        )
    return sorted(matches, key=lambda c: c.index)


def _chunks_at(chunks, spec):
    """Chunks at the exact positions given, e.g. --indices 0,4,8,12,16."""
    try:
        positions = [int(piece) for piece in spec.split(",") if piece.strip()]
    except ValueError:
        raise SystemExit(f"--indices wants whole numbers separated by commas, not '{spec}'")

    picked = []
    for position in positions:
        if 0 <= position < len(chunks):
            picked.append(chunks[position])
        else:
            print(f"(no chunk at position {position} — this corpus has {len(chunks)})")
    return picked


def cmd_chunks(args):
    """Milestone 3. Print chunks so you can read them and paste them."""
    from ingest import load_documents
    from chunker import split_documents

    chunks = split_documents(load_documents(args.corpus or config.CORPUS))

    if args.from_doc:
        sample = _chunks_from_doc(chunks, args.from_doc)
        heading = (
            f"{len(chunks)} chunks total. Showing all {len(sample)} from "
            f"{sample[0].source}."
        )
    elif args.indices:
        sample = _chunks_at(chunks, args.indices)
        heading = (
            f"{len(chunks)} chunks total. Showing {len(sample)} at positions "
            f"{args.indices}."
        )
    else:
        step = max(len(chunks) // args.n, 1)
        sample = chunks[::step][: args.n]
        heading = (
            f"{len(chunks)} chunks total. Showing {len(sample)}, spread across "
            f"the corpus."
        )

    print(f"{heading}\n")
    print("Paste these into your README under Sample Chunks. The rubric asks")
    print("for the source file and the function that produced them — both are")
    print("printed for you below.\n")

    for i, chunk in enumerate(sample, 1):
        print("=" * 70)
        print(
            f"Chunk {i}  |  source: {chunk.source}#{chunk.index}  "
            f"|  produced by: {chunk.produced_by}"
        )
        print("=" * 70)
        print(chunk.text)
        print()

    print("For each one, ask: could someone answer a question using only this,")
    print("without reading what came before or after?")


def cmd_retrieve(args):
    """Milestone 4. Retrieval only, with distances, and no model call."""
    from store import search
    import gate

    results = search(
        args.question,
        top_k=args.top_k or config.TOP_K,
        corpus=args.corpus or config.CORPUS,
        variant=args.variant,
    )

    if not results:
        print("Nothing came back. Have you run `python app.py index`?")
        return

    print(f"\nQuestion: {args.question}\n")
    print(f"{'#':<3} {'distance':<10} {'source':<32} preview")
    print("-" * 100)
    for i, r in enumerate(results, 1):
        preview = r.text[:52].replace("\n", " ")
        print(f"{i:<3} {r.distance:<10.4f} {r.source:<32} {preview}...")

    decision = gate.check(results)
    print(f"\nGate: {decision.explanation}")
    print("\nLower is better. 0.3 is a close match, 0.9 is unrelated.")
    print("Milestone 4: run your five questions, then the five in OUT_OF_SCOPE")
    print("that your documents clearly don't cover, and look for the gap")
    print("between the two groups. Your cutoff goes in that gap.")


def ask_pipeline(
    question,
    corpus=None,
    variant="default",
    top_k=None,
    threshold=None,
    on_gate=None,
    on_prompt=None,
):
    """Retrieve, gate, answer. Returns the outcome and prints nothing.

    One question through all five stages, with the result handed back as a
    plain dict instead of printed. `_ask_one` below prints it for the command
    line; `serve.py` turns the same dict into JSON. The relevance gate is the
    reason this is one function rather than two: a web wrapper that re-decided
    when to refuse would be a second cutoff you'd have to keep in step with
    this one, and it would drift.

    The two optional callbacks let the command line print as it goes without
    this function knowing anything about printing: `on_gate` is handed the gate
    decision as soon as it's made, and `on_prompt` is handed the assembled
    prompt just before it goes out — that's how `--show-prompt` shows you the
    prompt while the model is still thinking rather than after.
    """
    from store import search
    import gate
    from generate import answer_from_chunks, build_prompt

    results = search(
        question,
        top_k=top_k or config.TOP_K,
        corpus=corpus or config.CORPUS,
        variant=variant,
    )
    decision = gate.check(results, threshold=threshold)
    if on_gate is not None:
        on_gate(decision)

    outcome = {
        "question": question,
        "refused": not decision.passed,
        "best_distance": decision.best_distance,
        "threshold": decision.threshold,
        "sources": [],
        "prompt": None,
    }

    if not decision.passed:
        outcome["answer"] = gate.REFUSAL
        return outcome

    prompt = build_prompt(question, results)
    if on_prompt is not None:
        on_prompt(prompt)

    outcome["prompt"] = prompt
    outcome["answer"] = answer_from_chunks(question, results)
    outcome["sources"] = sorted({r.source for r in results})
    return outcome


def _ask_one(
    question,
    corpus,
    variant,
    top_k,
    threshold,
    show_distances=True,
    show_prompt=False,
):
    import gate
    from generate import GROUNDING_INSTRUCTION

    def print_distances(decision):
        best = f"{decision.best_distance:.3f}"
        print(f"  (best distance {best}, cutoff {decision.threshold})")

    def print_prompt(prompt):
        print("\n" + "=" * 70)
        print("System instruction sent with the prompt")
        print("=" * 70)
        print(GROUNDING_INSTRUCTION)
        print("\n" + "=" * 70)
        print("The assembled prompt, exactly as sent")
        print("=" * 70)
        print(prompt)
        print("=" * 70)

    outcome = ask_pipeline(
        question,
        corpus=corpus,
        variant=variant,
        top_k=top_k,
        threshold=threshold,
        on_gate=print_distances if show_distances else None,
        on_prompt=print_prompt if show_prompt else None,
    )

    if outcome["refused"]:
        print(f"\n{gate.REFUSAL}\n")
        return gate.REFUSAL

    print(f"\n{outcome['answer']}\n")
    print(f"Sources retrieved: {', '.join(outcome['sources'])}\n")
    return outcome["answer"]


def cmd_ask(args):
    corpus = args.corpus or config.CORPUS
    import generate as gen

    try:
        if args.question:
            _ask_one(
                args.question,
                corpus,
                args.variant,
                args.top_k,
                args.threshold,
                show_prompt=args.show_prompt,
            )
        else:
            print("Ask a question, or press Enter on an empty line to quit.\n")
            while True:
                try:
                    question = input("> ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    break
                if not question:
                    break
                _ask_one(
                    question,
                    corpus,
                    args.variant,
                    args.top_k,
                    args.threshold,
                    show_prompt=args.show_prompt,
                )
    finally:
        print(gen.usage())


def build_parser():
    parser = argparse.ArgumentParser(
        prog="app.py",
        description="The Unofficial Guide",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--corpus", help="corpus folder name (see corpora/README.md)")
    parser.add_argument(
        "--variant",
        default="default",
        help="index variant, for holding two chunkings at once (unit 2)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("corpora", help="list available corpora").set_defaults(func=cmd_corpora)

    p_index = sub.add_parser("index", help="build the search index")
    p_index.set_defaults(func=cmd_index)

    p_chunks = sub.add_parser("chunks", help="print sample chunks (Milestone 3)")
    p_chunks.add_argument("-n", type=int, default=5, help="how many to print")
    p_chunks.add_argument(
        "--from-doc",
        metavar="NAME",
        help=(
            "print every chunk of one source document instead of a sample. "
            "Use this to compare the same material before and after a "
            "chunker change"
        ),
    )
    p_chunks.add_argument(
        "--indices",
        metavar="0,4,8",
        help="print the chunks at these exact positions instead of a sample",
    )
    p_chunks.set_defaults(func=cmd_chunks)

    p_ret = sub.add_parser("retrieve", help="show distances only (Milestone 4)")
    p_ret.add_argument("question")
    p_ret.add_argument("--top-k", type=int)
    p_ret.set_defaults(func=cmd_retrieve)

    p_ask = sub.add_parser("ask", help="ask a question")
    p_ask.add_argument("question", nargs="?")
    p_ask.add_argument("--top-k", type=int)
    p_ask.add_argument("--threshold", type=float, help="override the gate cutoff")
    p_ask.add_argument(
        "--show-prompt",
        action="store_true",
        help="print the assembled prompt before the answer",
    )
    p_ask.set_defaults(func=cmd_ask)

    return parser


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001 — students read this, not a traceback
        print(f"\n{type(exc).__name__}: {exc}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
