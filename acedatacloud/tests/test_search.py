"""Unit tests for the client-side fan-out search helper (pure, no network)."""

from core.search import MAX_TERMS, rank_items, score_item, tokenize_query


class TestTokenizeQuery:
    def test_splits_on_whitespace_and_lowercases(self):
        assert tokenize_query("Music Video Generation") == ["music", "video", "generation"]

    def test_trims_surrounding_punctuation_keeps_internal(self):
        assert tokenize_query("suno, nano-banana!") == ["suno", "nano-banana"]

    def test_drops_short_tokens_and_dedupes(self):
        assert tokenize_query("a suno suno x") == ["suno"]

    def test_caps_number_of_terms(self):
        many = " ".join(f"term{i}" for i in range(MAX_TERMS + 5))
        assert len(tokenize_query(many)) == MAX_TERMS

    def test_empty_or_none(self):
        assert tokenize_query("") == []
        assert tokenize_query(None) == []

    def test_cjk_stays_single_term(self):
        assert tokenize_query("音乐生成") == ["音乐生成"]


class TestScoreItem:
    FIELDS = {"alias": 3, "title": 3, "tags": 2, "description": 1}

    def test_phrase_beats_single_term(self):
        item = {"title": "Suno Music Generation"}
        phrase_hit = score_item(item, "music generation", ["music", "generation"], self.FIELDS)
        one_term = score_item(
            {"title": "only music here"}, "music generation", ["music", "generation"], self.FIELDS
        )
        assert phrase_hit > one_term

    def test_weighted_fields(self):
        alias_hit = score_item({"alias": "suno"}, "suno", ["suno"], self.FIELDS)
        desc_hit = score_item({"description": "suno"}, "suno", ["suno"], self.FIELDS)
        assert alias_hit > desc_hit

    def test_tags_list_is_searched(self):
        item = {"tags": ["music", "audio"]}
        assert score_item(item, "audio", ["audio"], self.FIELDS) > 0

    def test_no_match_is_zero(self):
        assert score_item({"title": "nothing"}, "zzz", ["zzz"], self.FIELDS) == 0


class TestRankItems:
    FIELDS = {"alias": 3, "title": 3, "tags": 2, "description": 1}

    def test_multi_word_query_ranks_and_filters(self):
        items = [
            {"alias": "flux", "title": "Flux Image Generation"},
            {"alias": "suno", "title": "Suno Music Generation", "tags": ["music"]},
            {"alias": "serp", "title": "Google Search"},
        ]
        ranked = rank_items(items, "music generation", self.FIELDS)
        assert [it["alias"] for it in ranked] == ["suno", "flux"]  # serp dropped (no hit)

    def test_limit_truncates(self):
        items = [{"title": f"generation {i}"} for i in range(5)]
        assert len(rank_items(items, "generation", self.FIELDS, limit=2)) == 2

    def test_empty_query_preserves_order(self):
        items = [{"alias": "a"}, {"alias": "b"}]
        assert rank_items(items, "", self.FIELDS) == items
