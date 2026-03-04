from django.urls import path
from .views import ArticleList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete, ArticleSearch

urlpatterns = [
    path('', ArticleList.as_view(), name='articles_list'),
    path('<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('search/', ArticleSearch.as_view(), name='article_search'),
]
