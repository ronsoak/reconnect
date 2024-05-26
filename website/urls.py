from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,{"filtr": 0},name='home'),
    path('new',views.Home,{"filtr": 1}, name='new'),
    path('curated',views.Home,{"filtr": 2}, name='curated'),
    path('random',views.Home,{"filtr": 3}, name='random'),
    path('search',views.Search, name='search'),
    path('about',views.About, name='about'),
    path('feeds',views.RSS, name='feeds'),
    path('more/<uuid:st_id>',views.More, name='more'),

    # Error Pages
    path('400',views.page404, name='400Page'),
    path('404',views.page404, name='404Page'),
    path('500',views.page500, name='500Page'),

    # Functions 
    path('vote/l/<uuid:id>/<session>/',views.Vote,name='link vote'),  #user clicked the link
    path('feature/<id>', views.FeatureArticle, name='feature'),
    path('hide/<id>', views.HideArticle, name='hide'),
]