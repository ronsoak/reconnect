from typing import Any
from django.core.management.base import BaseCommand
from website.models import Articles, Logic
# This script hides or un hides articles based on keywords in the logic model
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        l = Logic.objects.filter(category="KEYWORD")
        for k in l:
            w = k.value 
            a = Articles.objects.filter(title__icontains=w)
            for i in a:
                i.hidden = True
                i.save()
