from django.db import models
from django.contrib.auth import get_user_model


class Tag(models.Model):
    slug = models.CharField(primary_key=True, unique=True, max_length=20)
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.slug


class Article(models.Model):
    title = models.CharField(default="", max_length=30)
    text = models.TextField(default="")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='article_user')
    count = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag, blank=True)
    insert_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment = models.TextField(default='', max_length=500)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comment_user')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comment')
    insert_dttm = models.DateTimeField(auto_now_add=True)

