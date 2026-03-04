from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
            'author',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст поста', 'rows': 5}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and title[0].islower():
            raise ValidationError("Заголовок должен начинаться с заглавной буквы.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content) < 20:
            raise ValidationError("Текст не может быть менее 20 символов.")
        return content

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and content and title == content:
            raise ValidationError("Заголовок не должен быть равен тексту.")

        return cleaned_data