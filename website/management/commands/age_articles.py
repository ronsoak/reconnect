from tkinter.tix import Tree
from typing import Any
from django.core.management.base import BaseCommand
from website.models import Articles
from datetime import date, timedelta

# Runs on a Monday, Gets articles older than 7 days, and reduces their modifier score by .1, 
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        today = date.today()
        if (today.weekday() == 0 ):
            cutdate = today - timedelta (days=7)
            c = Articles.objects.filter(published__lte=cutdate,hidden=False,site_hide=False, modifier__gte=0.3)
            for i in c:
                i.modifier = i.modifier - 0.1
                i.save()
        else:
            pass
