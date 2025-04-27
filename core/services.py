import unicodedata
from rapidfuzz import fuzz


def strip_accent(text: str) -> str:
    """
    Strip accents from the given string, e.g.
    “čučoriedka” → “cucoriedka”.
    """
    return unicodedata.normalize('NFKD', text) \
        .encode('ascii', 'ignore') \
        .decode('ascii')


def compute_fuzzy_score(query: str, text: str) -> float:
    """
    Compare two strings and return a similarity score,
    considering full matches, partial matches, and matches
    that ignore word order or extra words.
    """
    # normalize inputs
    query_norm = strip_accent(query).lower()
    text_norm = strip_accent(text).lower()

    # boost exact substring matches
    if query_norm in text_norm:
        return 100.0

    # calculate fuzzy scores
    ratio_score = fuzz.ratio(query_norm, text_norm)
    partial_score = fuzz.partial_ratio(query_norm, text_norm)
    token_score = fuzz.token_set_ratio(query_norm, text_norm)

    # return the highest
    return max(ratio_score, partial_score, token_score)


def fuzzy_search(
        query: str,
        queryset,
        attr: str,
        threshold: float = 78.0
):
    """
    Run fuzzy search over a Django queryset, on the given attribute name.

    :param query: the raw user string
    :param queryset: e.g. Film.objects.all()
    :param attr: name of the model field to match, e.g. "title" or "name"
    :param threshold: minimum score to include
    :return: a list of model instances sorted by descending score
    """
    if not query:
        return []

    results = []
    for obj in queryset:
        text = getattr(obj, attr, "")
        score = compute_fuzzy_score(query, text)
        if score >= threshold:
            results.append((score, obj))

    # highest-score first
    results.sort(key=lambda pair: pair[0], reverse=True)

    # strip off the score
    return [obj for score, obj in results]
