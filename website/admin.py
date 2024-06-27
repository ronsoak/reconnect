from django.contrib import admin
from website.models import Logic, Sites, Articles, Votes

# Register your models here.
admin.site.register(Logic)
admin.site.register(Votes)

# ===== ===== ===== ===== ===== ===== 
# Article View
# ===== ===== ===== ===== ===== ===== 
@admin.register(Articles)
class ArticleAdmin(admin.ModelAdmin):
    list_display=('title','rank','curated','site','published','hidden','site_hide')
    list_filter=['curated','hidden','site_hide','site']
    actions = ['mark_as_curated','mark_as_uncurated','mark_as_hidden']
    show_facets = admin.ShowFacets.ALWAYS
    search_fields = ['title']
    # Methods
    def get_ordering(self, request):
        return ['-published']
    
    def mark_as_curated(self, request, queryset):
        queryset.update(curated = True)
    mark_as_curated.short_description = "Curate"

    def mark_as_uncurated(self, request, queryset):
        queryset.update(curated = False)
    mark_as_uncurated.short_description = "Uncurate"

    def mark_as_hidden(self, request, queryset):
        queryset.update(hidden = True)
    mark_as_hidden.short_description = "Hidden"

# ===== ===== ===== ===== ===== ===== 
# Sites 
# ===== ===== ===== ===== ===== ===== 
@admin.register(Sites)
class SiteAdmin(admin.ModelAdmin):
    list_display=('name','feed_type','modifier','hidden')
    list_filter=['feed_type','modifier','hidden']
    list_per_page= 500
    actions = ['hide_site']
    show_facets = admin.ShowFacets.ALWAYS
    search_fields = ['name']
    # Methods
    def get_ordering(self, request):
        return ['-name']
    
    def hide_site(self, request, queryset):
        queryset.update(hidden = True)
    hide_site.short_description = "Hidden"
