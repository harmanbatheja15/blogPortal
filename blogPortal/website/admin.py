from django.contrib import admin
from django.utils.html import format_html
from .models import Article, BlogComment

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):

    def myimage(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.image.url))

    list_display = ('id', 'author', 'title', 'publish_date')
    list_display_links = ('id', 'author')
    search_fields = ('id', 'author', 'title')
    list_per_page = 10

class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'publish_date')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user')
    list_per_page = 10

admin.site.register(Article, ArticleAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
