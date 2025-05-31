from django.urls import path
from . import views as view

urlpatterns = [
    path('', view.HomeView.as_view(), name='home'),
    path('about/', view.about_view, name='about'),
    path('bologna/', view.bologna_view, name='bologna'),
    path('publications/', view.publications_view, name='publications'),
    path('test/', view.HomeView.as_view(), name='test'),

    # News
    path("news/<int:pk>/", view.NewsDetailView.as_view(), name="news_detail"),
    path("news/", view.NewsListView.as_view(), name="news_list"),

    # Events
    path('api/events-by-month/', view.EventsByMonthAPIView.as_view(), name='events_by_month'),
    path('events/<int:pk>/', view.EventDetailView.as_view(), name='event_detail'),
    path('events/', view.EventListView.as_view(), name='event_list'),

    # Search
    path('search/', view.SearchView.as_view(), name='search'),
]
