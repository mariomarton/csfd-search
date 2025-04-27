from django.shortcuts import render, get_object_or_404
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

    return render(request, 'core/search/search.html', {
        'query': query,
        'film_page': film_page,
        'actor_page': actor_page,
    })


def detail_view(request, model_name, pk):
    model_mapping = {
        'film': Film,
        'actor': Actor,
    }

    model_class = model_mapping.get(model_name)

    if model_class is None:
        raise ValueError("Invalid model name")

    detail_object = get_object_or_404(model_class, pk=pk)
    return render(request, f'core/detail/{model_name}_detail.html', {'detail_object': detail_object})


def page_not_found_view(request, exception):
    return render(request, 'core/error.html', {'error_message': 'Stránka sa nenašla.'}, status=404)


def server_error_view(request):
    return render(request, 'core/error.html', {'error_message': 'Oops, chyba. Skúste to prosím neskôr.'}, status=500)
