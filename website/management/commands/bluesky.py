# imports 
import os
from typing import Any
from django.core.management.base import BaseCommand
from atproto import Client, models, client_utils
from website.models import Articles
import ssl
import httpx

# function
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        # query to get curated articles that havn't been posted already
        bquery = Articles.objects.filter(hidden=False, site_hide=False,curated=True, bluesky=False).select_related("site").order_by('-published')[:1]
        bKey = os.getenv("BLUESKY_KEY")
        # if results are zero exit 
        if bquery.count() == 0: 
            quit() 
        else:
            for b in bquery:
                # start bluesky client  
                client = Client()
                # log in 
                client.login('antranaut.com',bKey)
                # Get query details
                aTitle = b.title
                aLink = b.url
                aSite = b.site.name
                iURL = b.image_url

                # Fixes issue with having an SSL cert
                ssl._create_default_https_context=ssl._create_unverified_context 

                # Get image thumbnail
                iPath = httpx.get(iURL).content
                aThumb = client.upload_blob(iPath).blob

                # Start Text Builder 
                text_builder = client_utils.TextBuilder()
                text_builder.text('Reconnect Recommends: \n\n')
                text_builder.text(aTitle+'\n\n')
                text_builder.tag('#gaming', 'gaming')
                text_builder.text(' ')
                text_builder.tag('#videogames', 'videogames')

                # AppBskyEmbedExternal is the same as "link card" in the app
                embed_external = models.AppBskyEmbedExternal.Main(
                    external=models.AppBskyEmbedExternal.External(
                        title=aTitle,
                        description='This article has been curated by Reconnect, the games writing discovery platform.',
                        uri= aLink,
                        thumb=aThumb,
                    )
                )
                client.send_post(text=text_builder, embed=embed_external)
                b.bluesky = True 
                b.save()
