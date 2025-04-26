from django.shortcuts import render
from django.core.paginator import Paginator
from core.models import Film, Actor
from core.services import fuzzy_search


def search_view(request):
    query = request.GET.get('q', '').strip()

    # run fuzzy search
    films_list = fuzzy_search(query, Film.objects.all(), attr="title")
    actors_list = fuzzy_search(query, Actor.objects.all(), attr="name")

    # paginate each list
    film_paginator = Paginator(films_list, 10)
    actor_paginator = Paginator(actors_list, 10)

    film_page_number = request.GET.get('film_page')
    actor_page_number = request.GET.get('actor_page')

    film_page = film_paginator.get_page(film_page_number)
    actor_page = actor_paginator.get_page(actor_page_number)

    return render(request, 'core/search.html', {
        'query': query,
        'film_page': film_page,
        'actor_page': actor_page,
    })
