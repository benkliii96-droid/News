from django.contrib.auth.models import User
from django.db import models
from django.db.models.aggregates import Sum


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)
    def update_rating(self):
        post_rating_sum = Post.objects.filter(author=self).aggregate(Sum('postRating'))['postRating__sum'] or 0
        author_comments_sum = Comment.objects.filter(userComment=self.user).aggregate(Sum('commentRating'))['commentRating__sum'] or 0
        posts_of_author = Post.objects.filter(author=self)
        comments_to_posts_sum = Comment.objects.filter(post__in=posts_of_author).aggregate(Sum('commentRating'))['commentRating__sum'] or 0

        self.author_rating = post_rating_sum * 3 + author_comments_sum + comments_to_posts_sum
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    post_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    content = models.TextField()
    postRating = models.SmallIntegerField(default=0)


    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        return f"{self.content[:124]}..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    userComment = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()
