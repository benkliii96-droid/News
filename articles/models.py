from django.db import models
from newsapp.models import Post

class Article(Post):
    class Meta:
        proxy = True
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'