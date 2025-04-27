import pytest
from django.urls import reverse

from core.models import Film


@pytest.mark.django_db
def test_search_view_returns_ok(client):
    response = client.get(reverse('search'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_view_finds_film(client):
    Film.objects.create(csfd_id=1, title="Shawshank Redemption")
    response = client.get(reverse('search'), {'q': 'shawshank'})
    assert response.status_code == 200
    assert "Shawshank Redemption" in response.text


@pytest.mark.django_db
def test_search_view_finds_film_fuzzy_search(client):
    Film.objects.create(csfd_id=1, title="Shawshank Redemption")
    response = client.get(reverse('search'), {'q': 'shavshank'})
    assert response.status_code == 200
    assert "Shawshank Redemption" in response.text


@pytest.mark.django_db
def test_search_view_does_not_find_irrelevant_film(client):
    Film.objects.create(csfd_id=1, title="Shawshank Redemption")
    response = client.get(reverse('search'), {'q': 'Harry Potter'})
    assert response.status_code == 200
    assert "Shawshank Redemption" not in response.text
