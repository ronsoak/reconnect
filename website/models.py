from django.db import models
import uuid                         # needed for GUID
from django.utils import timezone   # needed for time delta 
from django.db.models import F      # needed for math
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
# Logic 
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
class Logic(models.Model):
    # Options
    CATEGORIES = (
        ("METHOD","Feed"),
        ("KEYWORD","Keyword")
    )
    # Fields
    id          = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    category    = models.CharField(max_length=256,blank=False,null=False,choices=CATEGORIES,help_text="Category of Logic", verbose_name="Logic Category")
    value       = models.CharField(max_length=512,blank=False,null=False,help_text="Logic Value", verbose_name="Logic Value")
    # Metadata
    class Meta:
        db_table = "logic"
        ordering = ['category']
        verbose_name = "Logic"
        verbose_name_plural = "Logic"
    # Methods 
    def __str__(self):
        return self.category + ": " + self.value
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
# Sites 
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
class Sites(models.Model):
    # Fields
    id          = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=256,blank=False,null=False,help_text="Name of the Site", verbose_name="Name")
    url         = models.URLField(blank=False,null=False, help_text="Top level URL of the Site", verbose_name="Site URL")
    feed        = models.URLField(blank=False,null=False, help_text="The URL of the Feed", verbose_name="Feed URL")
    feed_type   = models.ForeignKey(Logic, on_delete=models.PROTECT, limit_choices_to=models.Q(category="METHOD"))
    description = models.TextField(max_length=2000, blank=False,null=False,help_text="Explanation of the site", verbose_name="Site Description")
    logo        = models.ImageField(upload_to='media/sites', max_length=512,help_text="Upload the sites logo", verbose_name="Site Logo")
    modifier    = models.FloatField(default=1, blank=False, help_text="Rank Modifier", verbose_name="Modifier Value")
    hidden      = models.BooleanField(default=False, help_text="Indicates whether the site is hidden", verbose_name="Site Hidden")
    # Metadata
    class Meta:
        db_table = "sites"
        ordering = ['name']
        verbose_name = "Sites"
        verbose_name_plural = "Sites"
    # Methods 
    def __str__(self):
        return self.name
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
# Articles 
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
class Articles(models.Model):
    # Fields
    id          = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    title       = models.CharField(max_length=256,blank=False,null=False,help_text="", verbose_name="Article Title")
    url         = models.URLField(blank=False,null=False, help_text="", verbose_name="Article URL")
    image_url   = models.CharField(max_length=512,blank=False,null=False,help_text="", verbose_name="Image Reference")
    site        = models.ForeignKey(Sites, on_delete=models.CASCADE)
    published   = models.DateField(null=True, blank=True, help_text="The date the article was published", verbose_name="Published Date")
    created     = models.DateTimeField(auto_now_add=True,null=True, blank=True, help_text="The date the article was created in the site", verbose_name="Created Date") 
    boost       = models.FloatField(default=0,blank=False,help_text="Boosts the article artificially",verbose_name="Boost Count")
    clicks      = models.FloatField(default=0,blank=False,help_text="Count of link clicks",verbose_name="Click Count")
    modifier    = models.FloatField(default=1,blank=False,help_text="",verbose_name="Modifier Score")
    rank        = models.GeneratedField(
                    expression=((F("clicks")+ F("boost")) * F("modifier")),
                    output_field=models.IntegerField(default=0,blank=False,help_text="Rank in the feed", verbose_name="Rank Score"),
                    db_persist=True,
                )
    hidden      = models.BooleanField(default=False, help_text="The article is hidden", verbose_name="Article Hidden")
    site_hide   = models.BooleanField(default=False, help_text="The parent site is hidden", verbose_name="Site Hidden")
    curated     = models.BooleanField(default=False, help_text="The article is curate", verbose_name="Article Curated")
    # Metadata
    class Meta:
        db_table = "articles"
        ordering = ['created']
        verbose_name = "Articles"
        verbose_name_plural = "Articles"
        constraints = [models.UniqueConstraint(fields=["url"], name='unique_url')]
        indexes = [
            models.Index(fields=['hidden'], name='hidden_idx'),
            models.Index(fields=['site_hide'], name='site_hide_idx'),
            models.Index(fields=['-curated'], name='curated_idx'),
            models.Index(fields=['-published'], name='published_idx'),
        ]
    # Methods 
    def __str__(self):
        return self.title
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
# Votes 
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
class Votes(models.Model):
    # Fields
    id          = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    article     = models.UUIDField(default=uuid.uuid4, help_text="", verbose_name="Article ID")
    session     = models.CharField(max_length=128,blank=False,null=False,help_text="", verbose_name="Session ID")
    date        = models.DateField(default=timezone.now,help_text="",verbose_name="Vote Date")
    # Metadata
    class Meta:
        db_table = "votes"
        ordering = ['session']
        verbose_name = "Votes"
        verbose_name_plural = "Votes"
        indexes = [
            models.Index(fields=['session','article'], name='vote_exists_idx'),
        ]
    # Methods 
    def __str__(self):
        return str(self.id)