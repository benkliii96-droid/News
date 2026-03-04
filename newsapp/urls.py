from django.urls import path
from .views import NewsList, NewDetail, SearchNews, NewsCreate, NewsUpdate, NewsDelete, GlobalSearchView

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewDetail.as_view(), name='new_detail'),
    path('search/', SearchNews.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('global-search/', GlobalSearchView.as_view(), name='global_search'),
]
