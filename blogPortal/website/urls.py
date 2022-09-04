from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('add_article', views.add_article, name="add_article"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('search', views.search, name="search"),
    path('blogs/detail/<int:blog_id>/', views.detail, name='detail'),
    path('blogs/edit/<int:blog_id>/', views.editBlog, name='editBlog'),
    path('postComment', views.postComment, name="postComment"),
    path('like/<int:id>', LikeView, name="like_post"),
]
