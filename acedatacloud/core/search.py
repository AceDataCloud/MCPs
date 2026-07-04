"""Client-side fan-out keyword search shared by catalog/read tools.

Mirrors the platform's documentation search (``/api/v1/search/``): split a query
on whitespace into keywords, then score each item by an exact-phrase hit plus
per-keyword hits across weighted fields, and rank best-first. Kept pure so it is
unit-testable without network access.
"""

from __future__ import annotations

import string
from collections.abc import Iterable, Mapping
from typing import Any

MIN_TERM_LEN = 2
MAX_TERMS = 10
_STRIP = string.punctuation

# Score weights: an exact phrase is worth far more than a single keyword, so an
# item matching the whole query outranks one matching just one word.
PHRASE_SCORE = 100
TERM_SCORE = 10


def tokenize_query(query: str | None) -> list[str]:
    """Split a query on whitespace into distinct lowercase keywords.

    Trims surrounding punctuation per token (keeps internal punctuation such as
    ``nano-banana``), drops tokens shorter than :data:`MIN_TERM_LEN`, de-dupes
    (order-preserving) and caps the count at :data:`MAX_TERMS`. CJK queries have
    no spaces, so they collapse to a single keyword (the phrase).
    """
    if not query:
        return []
    terms: list[str] = []
    seen: set[str] = set()
    for raw in query.split():
        tok = raw.strip(_STRIP).lower()
        if len(tok) < MIN_TERM_LEN or tok in seen:
            continue
        seen.add(tok)
        terms.append(tok)
        if len(terms) >= MAX_TERMS:
            break
    return terms


def _field_text(value: Any) -> str | None:
    """Flatten a field value to searchable text (joins list/tuple items)."""
    if value is None:
        return None
    if isinstance(value, list | tuple):
        return " ".join(str(v) for v in value)
    return value if isinstance(value, str) else str(value)


def _text_score(text: str | None, phrase: str, terms: Iterable[str]) -> int:
    if not text:
        return 0
    low = text.lower()
    score = 0
    if phrase and phrase.lower() in low:
        score += PHRASE_SCORE
    for term in terms:
        if term in low:
            score += TERM_SCORE
    return score


def score_item(
    item: Mapping[str, Any], phrase: str, terms: list[str], fields: Mapping[str, float]
) -> float:
    """Sum weighted field scores for one item. ``fields`` maps name → weight."""
    total = 0.0
    for field, weight in fields.items():
        total += weight * _text_score(_field_text(item.get(field)), phrase, terms)
    return total


def rank_items(
    items: Iterable[Mapping[str, Any]],
    query: str | None,
    fields: Mapping[str, float],
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Fan a query out across ``fields`` and return items ranked best-first.

    Items scoring 0 (no keyword matched) are dropped. With an empty query the
    input order is preserved. ``limit`` truncates the ranked list when set.
    """
    materialized = [dict(it) for it in items]
    phrase = (query or "").strip()
    terms = tokenize_query(query)
    if not phrase and not terms:
        return materialized[:limit] if limit is not None else materialized
    scored = [(score_item(it, phrase, terms, fields), it) for it in materialized]
    ranked = [it for score, it in sorted(scored, key=lambda p: p[0], reverse=True) if score > 0]
    return ranked[:limit] if limit is not None else ranked
