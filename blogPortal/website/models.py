from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class Article(models.Model):

    # visibility_choices = (
    #     ('public', 'public'),
    #     ('private', 'private'),
    # )

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = RichTextField()
    publish_date = models.DateField(auto_now_add=True)
    # visibility = models.CharField(choices=visibility_choices, max_length=100, default="Public")
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class BlogComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    publish_date = models.DateField(auto_now_add=True)
