from django.core.management.base import BaseCommand
from core.scraper.csfd_scraper import scrape


class Command(BaseCommand):
    help = "Scrapes CSFD and updates the database"

    def handle(self, *args, **options):
        scrape()
        self.stdout.write(self.style.SUCCESS("Scraping CSFD completed!"))
