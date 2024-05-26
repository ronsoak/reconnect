from typing import Any
from django.core.management.base import BaseCommand
from website.models import Articles, Sites
# This script hides or un hides articles based on the parent publication setting
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        s = Sites.objects.filter()
        for i in s:
            id = i.id
            flag = i.hidden
            a = Articles.objects.filter(site = id)
            for c in a:
                c.site_hide = flag
                c.save()
