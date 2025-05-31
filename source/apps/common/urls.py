from django.urls import path
from . import views as view

urlpatterns = [
    path('', view.HomeView.as_view(), name='home'),
    path('about/', view.about_view, name='about'),
    path('bologna/', view.bologna_view, name='bologna'),
    path('test/', view.HomeView.as_view(), name='test'),

    path("news/<int:pk>/", view.NewsDetailView.as_view(), name="news_detail"),
    path("news/", view.NewsListView.as_view(), name="news_list"),
]
