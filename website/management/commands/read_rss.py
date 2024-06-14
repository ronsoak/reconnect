from typing import Any
from django.core.management.base import BaseCommand
import feedparser
import requests
import ssl
import warnings
from datetime import datetime
from zoneinfo import ZoneInfo
from website.models import Sites, Logic
from django.core import management
from bs4 import BeautifulSoup
from bs4 import MarkupResemblesLocatorWarning
# This script reads the RSS feeds of sites that have an RSS method listed against them.
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        # Supress guessing parser warning for pure XML feeds
        warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning)
        
        # Fixes Feedparser not getting an SSL cert
        ssl._create_default_https_context=ssl._create_unverified_context 
        
        # Gets the RSS identifier from the Logic Page
        rss_id = Logic.objects.get(category="METHOD", value = "RSS").id

        # Gets the sites that are using the RSS method
        sources = Sites.objects.filter(feed_type=rss_id, hidden=False)

        # Start to cycle through the sites
        for s in sources:
            url = s.feed.strip()
            name = s.name
            id = s.id 
            logo = s.logo.url
            error_check = False
            self.stdout.write("Reading Site: "+s.name) 

            # Check URL response 
            # Requests is more reliable than feed.status
            response = requests.get(url)
            self.stdout.write(str(response.status_code))

            # Attempt to parse the URL
            try:
                content = feedparser.parse(url)
            except:
                error_check = True
                self.stdout.write("failed to parse feed: " + name)

            while error_check == False:
                # Try to ascertain the status of the feed
                # If it fails, the script will still try to get content
                try:
                    feed_status = content.status
                except:
                    feed_status = 195

                self.stdout.write("Site Status: "+ str(feed_status)) 

                if feed_status >= 400:
                    error_check = True
                    self.stdout.write("Bad HTTP Status: "+ name +"["+str(feed_status)+"]")

                if content.bozo == 1:
                    error_check = True
                    self.stdout.write("Bad Bozo Flag: "+ name +"["+str(content.bozo)+"]")

                # Get the feed entries
                for c in content.entries:
                    # Try and get the date
                    try:
                        pub_date = datetime(*c.published_parsed[:6],tzinfo=ZoneInfo('Pacific/Auckland'))
                        pub_date = datetime.date(pub_date)
                    except:
                        pub_date = datetime.today()
                        pub_date = datetime.date(pub_date)
                    # Get article Image 
                    try:
                    # Embedded Closures 
                        if c.enclosures[0].type == "image/jpeg":
                            post_image = str(c.enclosures[0].href)
                        else:
                            raise Exception
                    except:
                        try:
                        # Media Content Image
                            post_image = str(c.media_content[0]["href"])
                        except:
                            try:
                                # Media Content Image
                                post_image = str(c.media_content[0]["url"])
                            except:
                                # Scan the content for the first Img reference
                                try:
                                    item_content = str(c.content)
                                    soup1 = BeautifulSoup(item_content, 'html5lib')
                                    image1 = soup1.find('img')
                                    post_image = image1['src']
                                except:
                                    # Scan the description for the first Img reference
                                    try:
                                        item_desc = str(c.description)
                                        soup2 = BeautifulSoup(item_desc, 'html5lib')
                                        image2 = soup2.find('img')
                                        post_image = image2['src']
                                    except:
                                        post_image = 'media/'+str(logo)
                    management.call_command("import_articles",c.title,c.link,post_image,str(pub_date),str(id))
                    error_check = True