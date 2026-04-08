from django.urls import path
from .views import (
    NewsList, NewDetail, ArticleList, ArticleDetail,
    NewsSearch, ArticleSearch,
    NewsCreate, ArticleCreate, NewsUpdate, ArticleUpdate,
    NewsDelete, ArticleDelete, upgrade_me
)

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewDetail.as_view(), name='new_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/', ArticleList.as_view(), name='articles_list'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('articles/search/', ArticleSearch.as_view(), name='article_search'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('articles/upgrade/', upgrade_me, name='upgrade')
]