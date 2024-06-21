from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import date, timedelta,datetime
from django.urls import reverse
from website.models import Articles, Votes, Sites
from django.views.decorators.csrf import csrf_protect
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
# Functions 
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
#
# ===== ===== =====
# Content Query
# ===== ===== =====
def ContentQuery(filtr):
        # ----- -----
        f = filtr
        date_start  = date.today()
        date_end    = date_start - timedelta(days=90)
        # Content Query
        query       = Articles.objects.filter(hidden=False,site_hide=False,published__range=[date_end,date_start]).order_by('-published')
        # ----- -----
        # Filter View
        if f == 1: # Newest 
            content = query.filter(hidden=False,site_hide=False).select_related("site").order_by('-published')[:100]
        elif f == 2: #Curated 
            content = query.filter(hidden=False,site_hide=False,curated=True).select_related("site").order_by('-published')[:20]
        elif f == 3: #Random 
            content = query.filter(hidden=False,site_hide=False).select_related("site").order_by('?')[:100]
        else: # Trending
            content = query.filter(hidden=False,site_hide=False).select_related("site").order_by('-rank','-published')[:100]
        return(content)
# ===== ===== =====
# Vote for Article
# ===== ===== =====
def Vote(self,id,session): 
    i = id 
    s = session
    c = 0 # can vote flag
    if Votes.objects.filter(article=i,session=s).exists():
        c = 0
        return HttpResponse('User has already voted')
    else:
        c = 1
    if c == 1:
        a = Articles.objects.get(id=i)
        a.clicks = a.clicks + 1
        a.save()
        # Write Vote to Vote Log
        new_vote = Votes(article=i,session=s)
        new_vote.save()
    return HttpResponse('Vote Successful')
# ===== ===== =====
# Hide Article
# ===== ===== =====
def HideArticle(request,id):
    if request.user.is_authenticated:
        a = Articles.objects.get(id = id)
        a.hidden = True
        a.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else: 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# ===== ===== =====
# Feature Article
# ===== ===== =====
def FeatureArticle(request,id):
    if request.user.is_authenticated:
        a = Articles.objects.get(id = id)
        a.curated = True
        a.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else: 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# ===== ===== =====
# RSS Feeds
# ===== ===== =====
class LatestArticles(Feed):
    title = "Reconnect Latest Articles"
    link = "/"
    description = "Newest Articles on Reconnect"

    def items(self):
        return Articles.objects.filter(hidden=False,site_hide=False).order_by('-published')[:50]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.site
    
    def item_link(self, item):
        return item.url
    
    def item_pubdate(self, item):
        return item.created
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
# Pages 
# ===== ===== ===== ===== ===== ===== ===== ===== ===== 
#
# ===== ===== =====
# Home
# ===== ===== =====
@csrf_protect
def Home(request,filtr):
    # Create a Session ID if one isn't already available for JS
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session = request.session.session_key
    # ----- -----
    f = filtr   # filter for page view type
    p = 20      # page limit
    page = request.GET.get("page")
    # ----- -----
    # Filter View
    if f == 1: # Newest 
        items = ContentQuery(f)
    elif f == 2: #Curated 
        items = ContentQuery(f)
    elif f == 3: #Random 
        items = ContentQuery(f)
    else: # Trending
        items = ContentQuery(f)
    paginator = Paginator(items,p)
    page_obj = paginator.get_page(page)
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    # ----- -----
    context = {
        "session"       : session,
        "content"       : content,
        "filtr"         : f,
        "page_obj"      : page_obj,
    }
    return render(request,'home.html',context)
# ===== ===== =====
# About
# ===== ===== =====
def About(request):
    s_count = Sites.objects.filter(hidden=False).count()
    a_count = Articles.objects.filter(hidden=False,site_hide=False).count()
    context = {
        "s_count" : s_count,
        "a_count" : a_count
    }
    return render(request,'about.html',context)
# ===== ===== =====
# Search
# ===== ===== =====
def Search(request):
    # Create a Session ID if one isn't already available for JS
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session = request.session.session_key
    # Search results model
    if request.method == "POST":
        squery = request.POST.get('Search Terms', None)
        if squery:
            qlimit = 500
            results = Articles.objects.filter(Q(title__icontains=squery, hidden = False, site_hide = False) | Q(site__name__icontains=squery)).order_by('-published')[:qlimit]
            return render(request, 'search.html', {"content":results,"session": session,})
    return render(request, 'search.html')
# ===== ===== =====
# RSS Feeds
# ===== ===== =====
def RSS(request):
    siteQuery = Sites.objects.filter(hidden=False).order_by('name')
    return render(request,'feeds.html',{"sites":siteQuery})
# ===== ===== =====
# Sites
# ===== ===== =====
def More(request, st_id):
    moreQuery = Articles.objects.filter(site__id=st_id,hidden = False, site_hide = False)[:500]
    moreDetails = Sites.objects.filter(id=st_id, hidden = False)
    moreList = Sites.objects.filter(hidden = False)
    context = {
        "content": moreQuery,
        "moreInfo": moreDetails,
        "moreSelect": moreList,
    }
    return render(request,'more.html',context)
# ===== ===== =====
# 400 PAGE
# ===== ===== =====
def page400(request):
    return render(request,'400.html')
# ===== ===== =====
# 404 PAGE
# ===== ===== =====
def page404(request):
    return render(request,'404.html')
# ===== ===== =====
# 500 PAGE
# ===== ===== =====
def page500(request):
    return render(request,'500.html')