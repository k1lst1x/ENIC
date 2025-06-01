from django.views.generic import TemplateView


class AcademicIntegrityView(TemplateView):
    template_name = "common/academic_integrity.html"
