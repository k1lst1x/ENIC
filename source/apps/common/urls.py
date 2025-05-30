from django.urls import path
from .views import home_view, about_view, bologna_view

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('bologna/', bologna_view, name='bologna'),
    path('test/', home_view, name='test'),
]
