from tkinter.tix import Tree
from typing import Any
from django.core.management.base import BaseCommand
from website.models import Articles
from datetime import date, timedelta

# Gets articles older than 3 days with more than 3 clicks, and reduces their modifier score by .1, 
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        today = date.today()
        cutdate = today - timedelta (days=3)
        c = Articles.objects.filter(published__lte=cutdate,hidden=False,site_hide=False, modifier__gte=0.3, clicks__gte=3 )
        for i in c:
            i.modifier = i.modifier - 0.1
            i.save()

