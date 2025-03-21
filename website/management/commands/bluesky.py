# imports 
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
        bquery = Articles.objects.filter(hidden=False, site_hide=False,curated=True, bluesky=False).select_related("site").order_by('published')[:1]
        bKey = 'password'
        # if results are zero exit 
        if bquery.count() == 0: 
            self.stdout.write("No sites to post, ending script") 
            quit() 
        else:
            for b in bquery:
                # start bluesky client  
                client = Client()
                # log in 
                self.stdout.write("Logging in") 
                client.login('antranaut.com',bKey)
                # Get query details
                aTitle = b.title
                aLink = b.url
                iURL = b.image_url
                self.stdout.write("values:"+aTitle+' '+aLink+' '+iURL) 

                # Fixes issue with having an SSL cert
                self.stdout.write("Setting SSL") 
                ssl._create_default_https_context=ssl._create_unverified_context 

                self.stdout.write("Trying to get image")
                # validate url 
                if iURL[:1] == 'h':
                    self.stdout.write("Image URL valid")
                    iPath = httpx.get(iURL).content
                    aThumb = client.upload_blob(iPath).blob
                else:
                    self.stdout.write("Image URL not valid, using backup")
                    rSite = httpx.get("https://www.reconnect.quest").content
                    aThumb = client.upload_blob(rSite).blob                    
                                        
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

                # # Backup linkcard 
                # embed_backup = models.AppBskyEmbedExternal.Main(
                #     external=models.AppBskyEmbedExternal.External(
                #         title=aTitle,
                #         description='This article has been curated by Reconnect, the games writing discovery platform.',
                #         uri= aLink,
                #         thumb=abackup,
                #     )
                # )
                self.stdout.write("Trying to post....")
                client.send_post(text=text_builder, embed=embed_external)

                # try:
                #     self.stdout.write("Trying to post....")
                #     client.send_post(text=text_builder, embed=embed_external)
                # except:
                #     self.stdout.write("Post failed, using backup post")
                #     client.send_post(text=text_builder, embed=embed_backup)
                self.stdout.write("Flipping flag")
                b.bluesky = True 
                b.save()
