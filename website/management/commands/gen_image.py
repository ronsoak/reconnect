import random
from typing import Any
from django.core.management.base import BaseCommand
import textwrap
from PIL import Image, ImageDraw, ImageFont
from website.models import Sites
# This script un-curates articles to keep it at just 20, so the newer ones stay and the older ones are removed.
class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        # Default Font
        # change this to a font in the server
        tfont = ImageFont.truetype("website/static/Font/Archivo-Bold.otf",size=18)

        # Background Image
        back = [
            "media/background/back1.png",
            "media/background/back2.png",
            "media/background/back3.png",
            "media/background/back4.png",
            "media/background/back5.png",
            "media/background/back6.png",
            "media/background/back7.png",
        ]

        # Site query 
        sQuery = Sites.objects.filter()

        # Site Loop
        for s in sQuery:
            site_name = s.name
            site_path = s.logo.url[1:]
            back_img = random.choice(back)

        # Text Changing
            image_text = textwrap.wrap(
                site_name,
                width=12,
                initial_indent='', 
                subsequent_indent='', 
                expand_tabs=False, 
                fix_sentence_endings=False, 
                break_long_words=False, 
                drop_whitespace=True, 
                break_on_hyphens=True, 
                max_lines=None, 
                placeholder=' [...]')

        # Background Image
            bim = Image.open(back_img,mode="r",formats=["png"])
            tdraw = ImageDraw.Draw(bim)
            tdraw.multiline_text(
                (300,300),"\n".join(image_text), 
                fill="Black", 
                font=tfont, 
                anchor="mm", 
                spacing=4, 
                align='center', 
                stroke_width=0, 
                stroke_fill=None,
                )
            tdraw.fontmode = "L"

        # Save Image
            bim.save(site_path)
            