from django.urls import path
from . import views as view

urlpatterns = [
    path('', view.HomeView.as_view(), name='home'),
    path('about/', view.AboutView.as_view(), name='about'),
    path('bologna/', view.BolognaView.as_view(), name='bologna'),
    path('publications/', view.publications_view, name='publications'),
    path('reference/', view.reference_view, name='reference'),
    path('registryop/', view.registryop_view, name='registryop'),
    path('activities/', view.activities_view, name='activities'),
    path('recognition/', view.recognition_view, name='recognition'),
    path('tokyo_convention/', view.tokyo_convention_view, name='tokyo_convention'),

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

    # Site Map
    path('sitemap/', view.SiteMapView.as_view(), name='sitemap'),

    # Open Access
    path('open_access/', view.OpenAccessView.as_view(), name='open_access'),

    # Corporate Ethics
    path('corporate_ethics/', view.CorporateEthicsView.as_view(), name='corporate_ethics'),

    # Foreign Specialists
    path('foreign_specialists/', view.ForeignSpecialistsView.as_view(), name='foreign_specialists'),

    # Mamandigim Bolashagim
    path('mamandigim_bolashagim/', view.MamandigimBolashagimView.as_view(), name='mamandigim_bolashagim'),

    # Projects
    path('projects/', view.ProjectsView.as_view(), name='projects'),
]
