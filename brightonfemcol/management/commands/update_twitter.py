from django.core.management.base import BaseCommand

from brightonfemcol.models import TwitterAccount


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """Should be run by cron every ten minutes or so."""
        [account.update() for account in TwitterAccount.objects.all()]
