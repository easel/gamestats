from django.core.management.base import BaseCommand, CommandError
from gamestats.loot.models import Import

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        Import.load()

