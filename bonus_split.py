"""Bonus: question 12 needs facts from two documents (E5 and E7).
One search returns 3 chunks that rarely hold both numbers, so we split it into
one search per car and merge the results. Free: no Claude call.

  python bonus_split.py
"""
from eval_retrieval import build_index
from rag.search import search

QUESTION = "לאיזה רכב חשמלי של החברה יש טווח נסיעה ארוך יותר, ובכמה?"
SUB_QUERIES = ["טווח נסיעה של OF-E5", "טווח נסיעה של OF-E7"]  # one search per car
NEEDLES = ["420 ק״מ", "510 ק״מ"]


def search_split(index, queries, per_query=2):
    """Runs each sub-query, keeps the top `per_query` chunks of each, and merges them without duplicates."""
    merged = []
    for q in queries:
        for c in search(index, q, "hybrid", per_query, current_only=True):
            if c not in merged:
                merged.append(c)
    return merged


def report(name, chunks):
    text = "\n".join(c.text for c in chunks)
    ok = all(n in text for n in NEEDLES)
    print(f"{name:<14} {'✓' if ok else '✗'}  {[c.id for c in chunks]}")


if __name__ == "__main__":
    index = build_index("headings")
    report("one search", search(index, QUESTION, "hybrid", 3, current_only=True))
    report("split search", search_split(index, SUB_QUERIES))
