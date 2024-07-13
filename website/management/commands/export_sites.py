from typing import Any
from django.core.management.base import BaseCommand
import csv
from website.models import Sites


# imports sites in bulk, images must be already loaded into the site.
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        sites = Sites.objects.filter()
        with open("sites.tsv", 'w', newline='') as efile:
            filewrite = csv.writer(efile, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
            for i in sites:
                filewrite.writerow([i.name,i.url,i.feed,i.description,i.logo,i.modifier])