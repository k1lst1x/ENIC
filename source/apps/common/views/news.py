from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.db.models import Q
from django.views.generic import DetailView
from django.utils.translation import get_language

from apps.common.models import News, Tag


class NewsListView(ListView):
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    model = News

    ordering = ['-created_at']

    paginate_by = 8
    paginate_orphans = 1

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_active=False)
        selected_tag = self.request.GET.get('tag')
        search_query = self.request.GET.get('search_query', '')

        if selected_tag:
            queryset = queryset.filter(tags__slug=selected_tag).distinct()
        if search_query:
            queryset = queryset.filter(
                Q(title_ru__icontains=search_query) |
                Q(title_kz__icontains=search_query) |
                Q(title_en__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['selected_tag'] = self.request.GET.get('tag')
        context['search_query'] = self.request.GET.get('search_query', '')

        # Пагинация
        paginator = Paginator(self.get_queryset(), self.paginate_by, orphans=self.paginate_orphans)
        page_number = self.request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['page_obj'] = page_obj
        context['page_number'] = page_obj.number

        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            queryset = self.get_queryset()
            page_number = request.GET.get('page', 1)
            paginator = Paginator(queryset, self.paginate_by, orphans=self.paginate_orphans)

            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)

            news_html = render_to_string('news/partial/news_cards.html', {'news': page_obj.object_list, 'current_lang': get_language()})
            pagination_html = render_to_string('news/partial/pagination.html', {'page_obj': page_obj, 'page_number': page_obj.number,
                                                                   'request': request})

            response_data = {
                'news_html': news_html,
                'pagination_html': pagination_html,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
            }

            return JsonResponse(response_data)

        # В случае обычного запроса, возвращаем HTML
        return super().get(request, *args, **kwargs)


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = "object"
