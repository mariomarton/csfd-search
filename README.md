
# csfd-search

### Features

- Search for the TOP 1000 films and actors that play in those films
- Click on search results to display relevant information (e.g., films the actor played in)
- Scrape the ČSFD website for data with a simple command

## Installation

1. After cloning the repository, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root of the project (the same directory as `manage.py`).

3. Add your secret key to the `.env` file like this:

```env
DJANGO_SECRET_KEY=your-secret-key-here
```

4. Run the database migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

The server should then run on port 8000: `http://127.0.0.1:8000/`

## Scraping Data

The project already comes with the scraped data saved in the database. You can scrape from ČSFD again though, using the following command:

```bash
python manage.py scrape_csfd
```

## Running Tests

To run the tests for this project, simply use `pytest`:

```bash
pytest
```
