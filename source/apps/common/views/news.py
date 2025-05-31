from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.db.models import Q
import hashlib
from bs4 import BeautifulSoup
from django.views.generic import DetailView
from django.utils import translation

from apps.common.models import News

class NewsListView(ListView):
    template_name = 'news_list.html'
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

            news_html = render_to_string('partial/news_cards.html', {'news': page_obj.object_list, 'current_lang': get_language()})
            pagination_html = render_to_string('pagination.html', {'page_obj': page_obj, 'page_number': page_obj.number,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Определяем текущий язык
        current_lang = translation.get_language()

        # Получаем контент в зависимости от языка

        lang_field_map = {
            "kz": "content_kz",
            "eng": "content_en",
            "ru": "content_ru",
        }
        content = getattr(self.object, lang_field_map.get(current_lang, "content_ru"))

        # Извлекаем заголовки и добавляем их в контекст
        context['headings'], context['content'] = self.process_content(content)

        # Получаем последние 10 новостей с такими же тегами, как у текущей новости
        similar_news = News.objects.filter(
            is_active=True
        ).exclude(id=self.object.id).distinct().exclude(is_active=False).order_by('-created_at')[:10]

        context['similar_news'] = similar_news

        return context

    def process_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        headings = []
        for tag in ['h1', 'h2', 'h3']:  # можно добавить другие уровни заголовков, если необходимо
            for header in soup.find_all(tag):
                if not header.has_attr('id'):
                    # Генерация уникального id на основе текста заголовка
                    header_id = hashlib.md5(header.text.encode('utf-8')).hexdigest()[:8]
                    header['id'] = header_id
                headings.append((header.text, header['id']))

        # Обновленный контент с добавленными id
        updated_content = str(soup)

        return headings, updated_content
