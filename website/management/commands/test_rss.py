from typing import Any
from django.core.management.base import BaseCommand
import feedparser
import ssl
from datetime import datetime
from zoneinfo import ZoneInfo
from website.models import Articles
from linkpreview import link_preview
import requests

# This script is manually triggered to test whether an RSS will work.
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        # Fixes Feedparser not getting an SSL cert
        ssl._create_default_https_context=ssl._create_unverified_context 

        siteUrl = "https://rss.beehiiv.com/feeds/2WtWfTwjg3.xml"
        # Set Error Check to default
        error_check = False

        # Check URL response 
        # Requests is more reliable than feed.status
        response = requests.get(siteUrl)

        if response.status_code >= 400:
            self.stdout.write("URL did not resolve: [" +str(response.status_code) + "]")

        if response.status_code == 301:
            self.stdout.write("URL Redirects, please check: [" + str(response.status_code) + "]")

        # Attempt to parse the URL
        try:
            content = feedparser.parse(siteUrl)
        except:
            error_check = True
            self.stdout.write("failed to parse feed: " + content)

        while error_check == False:
            # Check Bozo Flag
            if content.bozo == 1:
                error_check = True
                self.stdout.write("Bad Bozo Flag: "+"["+str(content.bozo_exception)+"]")

            # Get content entries
            for c in content.entries[0:5]:
                if Articles.objects.filter(url=c.link).exists():
                    self.stdout.write("URL Already in the site.")
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
                        post_image = str("No Image Found")
                    print (c.title,c.link,post_image,str(pub_date))
                    error_check = True



                
