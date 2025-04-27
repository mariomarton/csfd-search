import pytest
from django.urls import reverse
from django.test import RequestFactory
from core.models import Film, Actor
from core import views


@pytest.mark.django_db
def test_detail_view_returns_film_page(client):
    film = Film.objects.create(csfd_id=1, title="Inception")
    url = reverse('detail', args=['film', film.pk])

    response = client.get(url)

    assert response.status_code == 200
    assert response.context['detail_object'] == film
    template_names = [t.name for t in response.templates]
    assert f'core/detail/film_detail.html' in template_names
    assert "Inception" in response.text


@pytest.mark.django_db
def test_detail_view_returns_actor_page(client):
    actor = Actor.objects.create(csfd_id=2, name="Leonardo DiCaprio")
    url = reverse('detail', args=['actor', actor.pk])

    response = client.get(url)

    assert response.status_code == 200
    assert response.context['detail_object'] == actor
    template_names = [t.name for t in response.templates]
    assert 'core/detail/actor_detail.html' in template_names
    assert "Leonardo DiCaprio" in response.text


def test_detail_view_invalid_model_name_raises_error(request_factory=None):
    rf = request_factory or RequestFactory()
    request = rf.get('/detail/invalid/1/')

    with pytest.raises(ValueError):
        views.detail_view(request, 'invalid', pk=1)
