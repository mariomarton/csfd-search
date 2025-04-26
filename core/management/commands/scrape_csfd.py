from django.core.management.base import BaseCommand
from core.scraper.csfd_scraper import scrape
from core.models import Film, Actor


class Command(BaseCommand):
    help = "Scrapes CSFD and saves the data into the database"

    def handle(self, *args, **kwargs):
        confirm = input(
            "This will delete all existing Films and Actors before scraping.\n"
            "Are you sure you want to continue? [y/N]: "
        ).strip().lower()

        if confirm != 'y':
            self.stdout.write(self.style.WARNING("Aborted. No data was deleted."))
            return

        self.stdout.write(self.style.WARNING("Deleting Films and Actors..."))
        Film.objects.all().delete()
        Actor.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Deleted."))

        self.stdout.write(self.style.NOTICE("Starting scrape..."))
        scrape()
        self.stdout.write(self.style.SUCCESS("Scraping completed."))
