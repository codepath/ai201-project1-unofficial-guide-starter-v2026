"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


MIN_CHUNK = 200   # below this a section is a heading with nothing under it
MAX_CHUNK = 800   # cap on a finished chunk, including the context line


def _heading_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """
    Pull a document apart at its `##` headings.

    Returns the document title (from the leading `#` line) and a list of
    (heading, body) pairs. Anything before the first `##` is returned under an
    empty heading so no text is lost.
    """
    lines = text.split("\n")
    title = ""
    sections: list[tuple[str, str]] = []
    heading = ""
    body: list[str] = []

    for line in lines:
        if line.startswith("## "):
            sections.append((heading, "\n".join(body).strip()))
            heading = line[3:].strip()
            body = []
        elif line.startswith("# ") and not title:
            title = line[2:].strip()
        else:
            body.append(line)

    sections.append((heading, "\n".join(body).strip()))
    return title, [(h, b) for h, b in sections if b or h]


def _split_long(body: str, budget: int) -> list[str]:
    """Break an over-long section at sentence ends rather than mid-word."""
    sentences = re.split(r"(?<=[.!?])\s+", body)
    pieces: list[str] = []
    current = ""

    for sentence in sentences:
        if current and len(current) + len(sentence) + 1 > budget:
            pieces.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}".strip()

    if current.strip():
        pieces.append(current.strip())
    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents at their section headings instead of by character count.

    These guides are all built the same way: a `#` town name, then seven `##`
    sections of two or three hundred characters each. A fixed 800-character
    window ignores every one of those boundaries, so it ends a chunk halfway
    through "Where to stay" and starts the next one halfway through "When to
    go". Splitting on the headings the documents already carry keeps each
    section whole.

    Two things this does beyond splitting:

      - Every chunk starts with "<town> — <section>". The town name only
        appears once per file, in the `#` title, so a section taken on its own
        would contain no mention of which town it describes — and nine files
        have a near-identical "Getting there". The context line puts the town
        back into the text that gets embedded.

      - Sections under MIN_CHUNK characters are folded into the previous chunk
        rather than stored alone, which is what produced the 24-character chunk
        the fixed-size version left in the index.

    Documents with no `##` headings fall back to fixed-size windows.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        title, sections = _heading_sections(doc.text)
        if not sections or not title:
            for chunk in fallback_split([doc]):
                chunks.append(
                    Chunk(
                        text=chunk.text,
                        source=chunk.source,
                        index=len(
                            [c for c in chunks if c.source == doc.source]
                        ),
                        produced_by="chunker.py::split_documents",
                    )
                )
            continue

        texts: list[str] = []
        for heading, body in sections:
            if not body:
                continue

            context = f"{title} — {heading}" if heading else title
            budget = MAX_CHUNK - len(context) - 2

            for piece in _split_long(body, budget):
                candidate = f"{context}\n\n{piece}"
                # A section too short to stand alone joins the one before it.
                if len(candidate) < MIN_CHUNK and texts:
                    texts[-1] = f"{texts[-1]}\n\n{piece}"
                else:
                    texts.append(candidate)

        for index, text in enumerate(texts):
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
