from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .filters import PostFilter
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        return context


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='NW').order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_queryset(self):
        return Post.objects.filter(post_type='NW')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


class ArticleList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='AR').order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


class ArticleDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Post.objects.filter(post_type='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='NW')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


class ArticleSearch(ListView):
    model = Post
    template_name = 'article_search.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='AR')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


# Представления, требующие прав на добавление/изменение/удаление
class NewsCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'newsapp.add_post'  # только для пользователей с правом добавления постов

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание новости'
        context['button_text'] = 'Создать новость'
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('articles_list')
    permission_required = 'newsapp.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание статьи'
        context['button_text'] = 'Создать статью'
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'newsapp.change_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='NW')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование новости'
        context['button_text'] = 'Сохранить изменения'
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('articles_list')
    permission_required = 'newsapp.change_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование статьи'
        context['button_text'] = 'Сохранить изменения'
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'newsapp.delete_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='NW')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление новости'
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('articles_list')
    permission_required = 'newsapp.delete_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление статьи'
        if self.request.user.is_authenticated:
            context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        else:
            context['is_not_premium'] = True
        return context
