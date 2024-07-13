from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from website.models import Articles, Sites
from datetime import datetime
# This script receives input from another script to write into the Article model.
class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("title",type=str)
        parser.add_argument("url",type=str)
        parser.add_argument("image",type=str)
        parser.add_argument("published",type=str)
        parser.add_argument("site",type=str)


    def handle(self, *args: Any, **options: Any):
        a_title       = options["title"]
        a_url         = options["url"]
        a_image       = options["image"]
        a_published   = options["published"]
        a_created     = datetime.now()
        a_site        = options["site"]
        a_mod         = Sites.objects.get(pk=a_site).modifier

        try:
            article = Articles(
                title       = a_title,
                url         = a_url,
                image_url   = a_image,
                published   = a_published,
                created     = a_created,
                site        = Sites.objects.get(pk=a_site),
                modifier    = a_mod,
                clicks      = 1
            )
            article.save()
        except Exception as e:
            if str(e)[:24] == 'UNIQUE constraint failed':
                pass
            else:
                self.stderr.write(str(e))
