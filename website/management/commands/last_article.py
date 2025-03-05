from tkinter.tix import Tree
from typing import Any
from django.core.management.base import BaseCommand
from website.models import Articles
from datetime import date, timedelta
from website.models import Sites, Logic, Articles

# Counts days since last article and updates the site model with that information. 
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        # Get todays date
        today = date.today()
        today = today

        # get all sites
        sources = Sites.objects.filter(hidden=False)

        # per site query top 1 article
        for s in sources:
            id = s.pk 
            newest = Articles.objects.filter(site = id).order_by('-published')[:1]
            for n in newest:
                adate = n.published
                adiff = abs(today - adate).days
                s.lastarticle = adiff 
                s.save()
