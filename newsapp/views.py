from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .filters import NewsFilter
from .models import Post
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='NW').order_by('-date')


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_queryset(self):
        return Post.objects.filter(post_type='NW')


class SearchNews(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='NW')
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание новости'
        context['button_text'] = 'Создать новость'
        return context


class NewsUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='NW')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование новости'
        context['button_text'] = 'Сохранить изменения'
        return context


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='NW')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление новости'
        return context


class GlobalSearchView(ListView):
    model = Post
    template_name = 'global_search.html'
    context_object_name = 'results'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        post_type = self.request.GET.get('post_type', '')
        author = self.request.GET.get('author', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query))

        if post_type:
            queryset = queryset.filter(post_type=post_type)

        if author:
            queryset = queryset.filter(author__user__username__icontains=author)

        if date_from:
            queryset = queryset.filter(date__gte=date_from)

        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['selected_type'] = self.request.GET.get('post_type', '')
        context['author_query'] = self.request.GET.get('author', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        context['result_count'] = self.get_queryset().count()

        context['type_choices'] = [
            ('', 'Все'),
            ('NW', 'Новости'),
            ('AR', 'Статьи'),
        ]
        return context
