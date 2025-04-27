import pytest
from core import services


def test_strip_accent():
    assert services.strip_accent("čučoriedka") == "cucoriedka"
    assert services.strip_accent("čšžíáýťřůô") == "csziaytruo"
    assert services.strip_accent("helloworld") == "helloworld"
    assert services.strip_accent("m") == "m"
    assert services.strip_accent("") == ""


def test_compute_fuzzy_score_exact_match():
    score = services.compute_fuzzy_score("Harry Potter", "Harry Potter")
    assert score == 100.0


def test_compute_fuzzy_score_fuzzy_match():
    score = services.compute_fuzzy_score("Hary Potter", "Harry Potter")
    assert 80 <= score <= 100

    score = services.compute_fuzzy_score("Harry Potter", "Harry Potter and Order of The Phoenix")
    assert 80 <= score <= 100

    score = services.compute_fuzzy_score("Inter stellar", "Interstellar")
    assert 80 <= score <= 100

    score = services.compute_fuzzy_score("Interstaler", "Interstellar")
    assert 80 <= score <= 100


def test_fuzzy_search_returns_sorted_relevant_results():
    class TestFilmObject:
        def __init__(self, title):
            self.title = title

    objs = [TestFilmObject("Wall Street"),
            TestFilmObject("Wall Street 2"),
            TestFilmObject("The Wolf of Wall Street"),
            TestFilmObject("Wonder Woman")]

    results = services.fuzzy_search("wall stret", objs, attr="title", threshold=80)

    titles = [obj.title for obj in results]

    assert "Wall Street" in titles
    assert "Wall Street 2" in titles
    assert "The Wolf of Wall Street" in titles
    assert "Wonder Woman" not in titles

    # Test the order
    assert titles[0] == "Wall Street"
    assert titles[1] == "Wall Street 2"
    assert titles[2] == "The Wolf of Wall Street"


def test_fuzzy_search_empty_query_returns_empty_list():
    class TestFilmObject:
        name = "Pictures of the Old World"

    assert services.fuzzy_search("", [TestFilmObject()], attr="name") == []
