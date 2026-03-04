from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Article
from .forms import ArticleForm
from .filters import ArticleFilter


class ArticleList(ListView):
    model = Article
    ordering = '-date'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(post_type='AR').order_by('-date')


class ArticleDetail(DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.filter(post_type='AR')


class ArticleCreate(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('articles_list')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'AR'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание статьи'
        context['button_text'] = 'Создать статью'
        return context


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('articles_list')

    def get_queryset(self):
        return Article.objects.filter(post_type='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование статьи'
        context['button_text'] = 'Сохранить изменения'
        return context


class ArticleDelete(DeleteView):
    model = Article
    template_name = 'post_delete.html'
    success_url = reverse_lazy('articles_list')

    def get_queryset(self):
        return Article.objects.filter(post_type='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление статьи'
        return context


class ArticleSearch(ListView):
    model = Article
    template_name = 'article_search.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.filter(post_type='AR')
        self.filterset = ArticleFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
