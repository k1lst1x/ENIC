from django.views.generic import TemplateView


class ReviewsView(TemplateView):
    template_name = 'common/reviews.html'
