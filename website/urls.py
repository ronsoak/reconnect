from django.urls import path
from . import views
from django.views.generic.base import TemplateView #needed for robots

urlpatterns = [
    path('',views.Home,{"filtr": 1},name='home'),
    path('new',views.Home,{"filtr": 1}, name='new'),
    path('latest',views.Home,{"filtr": 0}, name='latest'),
    path('curated',views.Home,{"filtr": 2}, name='curated'),
    path('random',views.Home,{"filtr": 3}, name='random'),
    path('search',views.Search, name='search'),
    path('about',views.About, name='about'),
    path('feeds',views.RSS, name='feeds'),
    path('more/<st_id>',views.More, name='more'),

    # Robots
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    # Error Pages
    path('400',views.page400, name='400Page'),
    path('404',views.page404, name='404Page'),
    path('500',views.page500, name='500Page'),

    # Functions 
    path('vote/l/<id>/<session>/',views.Vote,name='link vote'),  #user clicked the link
    path('feature/<id>', views.FeatureArticle, name='feature'),
    path('hide/<id>', views.HideArticle, name='hide'),
]