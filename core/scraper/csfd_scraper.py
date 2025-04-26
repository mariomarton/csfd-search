import re
import time
import requests
from bs4 import BeautifulSoup, Tag
from django.db import transaction
from core.models import Film, Actor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = 'https://www.csfd.cz/zebricky/filmy/nejlepsi/'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
}

TIME_TO_SLEEP = 0.7  # Number of seconds to sleep before each request

# Setup session with retry logic (runs once when the module is imported)
session = requests.Session()
retries = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))


def parse_movies(first_movie_rank):
    """
    Returns a list of Film instances from one page (up to 100 movies).
    """
    query_params = {'from': first_movie_rank}
    response = session.get(BASE_URL, params=query_params, headers=HEADERS)
    response.raise_for_status()

    # Pause if this isn’t the first page
    if first_movie_rank > 1:
        time.sleep(TIME_TO_SLEEP)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    films = []
    for film_element in html_soup.select('a[class*=film]'):
        href = film_element.get('href')
        match = re.search(r'/film/(\d+)', href)
        if not match:
            continue

        film_csfd_id = int(match.group(1))
        title_text = film_element.get_text(strip=True)

        film_instance, _ = Film.objects.get_or_create(
            csfd_id=film_csfd_id,
            defaults={'title': title_text}
        )
        films.append(film_instance)

    return films


def parse_actors_for_movie(film):
    """
    Given a Film instance, fetch its detail page and return a list of Actor instances.
    Processes all actor links (including those hidden behind "show more").
    """
    detail_url = f"https://www.csfd.cz/film/{film.csfd_id}/"
    response = session.get(detail_url, headers=HEADERS)
    response.raise_for_status()
    time.sleep(TIME_TO_SLEEP)
    soup = BeautifulSoup(response.text, 'html.parser')

    # find the div with the "Hrají:" header and actor links
    header = soup.find('h4', string=re.compile(r'Hraj[ií]'))
    if not header:
        return []

    container_div = header.parent
    actors = []

    # loop processing every <a> under this div with href matching an actor
    for link in container_div.find_all('a', href=re.compile(r'/tvurce/(\d+)')):
        match = re.search(r'/tvurce/(\d+)', link['href'])
        if not match:
            continue
        actor_csfd_id = int(match.group(1))
        actor_name = link.get_text(strip=True)

        actor, _ = Actor.objects.get_or_create(
            csfd_id=actor_csfd_id,
            defaults={'name': actor_name}
        )
        actors.append(actor)

    return actors


def scrape():
    """
    Main function for the scraping of films and actors

    Scraping pipeline:
    1. Iterate over top movies in batches of 100
    2. Within each iteration, get and save the films and then actors for each film
    """
    for first_movie_rank in range(0, 1000, 100):
        try:
            first_rank = first_movie_rank if first_movie_rank != 0 else 1
            films = parse_movies(first_rank)
            print(f"Received {len(films)} movies starting at rank {first_rank}")
        except Exception as e:
            print(f"Failed to fetch movies from first_movie_rank {first_movie_rank}: {e}")
            continue

        for film in films:
            try:
                with transaction.atomic():
                    actors = parse_actors_for_movie(film)
                    film.actors.set(actors)
                    print(f"Set {len(actors)} actors for the film with CSFD ID: {film.csfd_id}")
            except Exception as e:
                print(f"Failed to get/set actors for film {film.csfd_id}: {e}")