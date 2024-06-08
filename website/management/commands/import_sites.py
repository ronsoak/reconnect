from tkinter.tix import Tree
from typing import Any
from django.core.management.base import BaseCommand
import csv
from website.models import Sites, Logic


# imports sites in bulk, images must be already loaded into the site.
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        with open("sites.tsv") as file:
            tsv_file = csv.reader(file, delimiter="\t")
            for line in tsv_file:
                i_name  = line[0]
                i_url   = line[1]
                i_feed  = line[2]
                i_description   = line[4]
                i_logo  = line[5]
                i_modifier  = line[6]
                try:
                    new_site = Sites(
                        name        = i_name,
                        url         = i_url,
                        feed        = i_feed,
                        feed_type   = Logic.objects.get(value='RSS'),
                        description = i_description,
                        logo        = i_logo,
                        modifier    = i_modifier,
                        hidden      = False
                    )
                    new_site.save()
                except Exception as e:
                    self.stderr.write(str(e))