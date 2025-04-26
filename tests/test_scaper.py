import pytest
from core.models import Film
from core.scraper.csfd_scraper import parse_movies, parse_actors_for_movie


@pytest.mark.django_db
def test_parse_movies_returns_films(mocker):
    mock_response = mocker.Mock()
    mock_response.text = """
        <html><body>
            <a class="film" href="/film/12345/">Some Film</a>
        </body></html>
    """
    mock_response.raise_for_status = mocker.Mock()
    mocker.patch('core.scraper.csfd_scraper.session.get', return_value=mock_response)

    films = parse_movies(1)
    assert len(films) == 1
    assert films[0].csfd_id == 12345
    assert films[0].title == 'Some Film'


@pytest.mark.django_db
def test_parse_actors_for_movie_returns_actors(mocker):
    film = Film.objects.create(csfd_id=12345, title="Some Film")

    mock_response = mocker.Mock()
    mock_response.text = """
        <html><body>
            <div>
                <h4>Hrají:</h4>
                <a href="/tvurce/67890/">Some Actor</a>
            </div>
        </body></html>
    """
    mock_response.raise_for_status = mocker.Mock()
    mocker.patch('core.scraper.csfd_scraper.session.get', return_value=mock_response)

    actors = parse_actors_for_movie(film)
    assert len(actors) == 1
    assert actors[0].csfd_id == 67890
    assert actors[0].name == 'Some Actor'
