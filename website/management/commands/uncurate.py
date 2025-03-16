from typing import Any
from django.core.management.base import BaseCommand
from website.models import Articles
# This script un-curates articles to keep it at just 20, so the newer ones stay and the older ones are removed.
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        a = Articles.objects.filter(curated=True).order_by('-published')[21:99]
        for i in a:
            i.curated = False 
            i.save()