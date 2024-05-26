from typing import Any
from django.core.management.base import BaseCommand
from website.models import Votes
from datetime import date, timedelta
# This script deletes the votes from the model that are older than 2 days to prevent voter abuse, but to keep the model light.
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        today = date.today()
        datestart = today - timedelta (days=2)
        dateend = datestart - timedelta (days=100)
        v = Votes.objects.filter(date__range=[dateend,datestart])
        v.delete()