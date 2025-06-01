from django.urls import path
from . import views as view

urlpatterns = [
    path('', view.HomeView.as_view(), name='home'),
    path('about/', view.AboutView.as_view(), name='about'),
    path('bologna/', view.BolognaView.as_view(), name='bologna'),
    path('publications/', view.publications_view, name='publications'),
    path('reference/', view.reference_view, name='reference'),
    path('activities/', view.activities_view, name='activities'),
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

    # 30 Op Po
    path('30_op_po/', view.OpPoView.as_view(), name='op_po'),

    # Faq
    path('faq/', view.FaqView.as_view(), name='faq'),

    # Quality
    path('quality/', view.QualityView.as_view(), name='quality'),

    # Academic Integrity
    path('academic_integrity/', view.AcademicIntegrityView.as_view(), name='academic_integrity'),

    # Kazakhstan In Bologna Process
    path('kazakhstan_in_bologna_process/', view.KazakhstanInBolognaProcessView.as_view(),
         name='kazakhstan_in_bologna_process'),

    # Research
    path('research/', view.ResearchView.as_view(), name='research'),

    # Reviews
    path('reviews/', view.ReviewsView.as_view(), name='reviews'),

    # Accreditation
    path('accreditation/', view.AccreditationView.as_view(), name='accreditation'),
]
