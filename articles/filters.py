from django import forms
from django_filters import FilterSet, CharFilter, DateFilter
from .models import Article


class ArticleFilter(FilterSet):
    name = CharFilter(field_name='title', lookup_expr='icontains', label='Название')
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Автор')
    date = DateFilter(field_name='date', lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}), label='Дата после')

    class Meta:
        model = Article
        fields = ['name', 'author', 'date']