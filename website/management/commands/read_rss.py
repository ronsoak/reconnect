from typing import Any
from django.core.management.base import BaseCommand
import feedparser
import requests
import ssl
from datetime import datetime
from zoneinfo import ZoneInfo
from website.models import Sites, Logic, Articles
from django.core import management
from linkpreview import link_preview
# This script reads the RSS feeds of sites that have an RSS method listed against them.
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        # Fixes Feedparser not getting an SSL cert
        ssl._create_default_https_context=ssl._create_unverified_context 
        
        # Gets the RSS identifier from the Logic Page
        rss_id = Logic.objects.get(category="METHOD", value = "RSS").pk

        # Gets the sites that are using the RSS method
        sources = Sites.objects.filter(feed_type=rss_id, hidden=False)

        # Start to cycle through the sites
        for s in sources:
            url = s.feed.strip()
            name = s.name
            id = s.pk 
            logo = s.logo.url
            
            # Set Error Check to default
            error_check = False
            
            # Write URL Name to Log
            self.stdout.write("Reading Site: "+s.name) 

            # Check URL response 
            # Requests is more reliable than feed.status
            response = requests.get(url)

            if response.status_code >= 400:
                self.stdout.write("URL did not resolve: "+ name + "[" +str(response.status_code) + "]")

            if response.status_code == 301:
                self.stdout.write("URL Redirects, please check: "+ name + "[" + str(response.status_code) + "]")

            # Attempt to parse the URL
            try:
                content = feedparser.parse(url)
            except:
                error_check = True
                self.stdout.write("failed to parse feed: " + name)

            while error_check == False:
                # Check Bozo Flag
                if content.bozo == 1:
                    error_check = True
                    self.stdout.write("Bad Bozo Flag: "+ name +"["+str(content.bozo)+"]")

                # Get the feed entries
                for c in content.entries:
                    if Articles.objects.filter(url=c.link).exists():
                        # self.stdout.write("URL Already in the site.")
                        error_check = True
                    else:
                        # clear variable
                        post_image = None
                        # Try and get the date
                        try:
                            pub_date = datetime(*c.published_parsed[:6],tzinfo=ZoneInfo('Pacific/Auckland'))
                            pub_date = datetime.date(pub_date)
                        except:
                            pub_date = datetime.today()
                            pub_date = datetime.date(pub_date)
                        # Get article Image 
                        try:
                            lp = link_preview(c.link, parser="lxml")
                            post_image = lp.image
                        except:
                            post_image = str(logo)
                        management.call_command("import_articles",c.title,c.link,post_image,str(pub_date),str(id))
                        error_check = True