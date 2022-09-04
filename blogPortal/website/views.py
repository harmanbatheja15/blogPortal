from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
import datetime
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Article, BlogComment
import os

# Create your views here.

def home(request):

    articles = Article.objects.all()

    context = {
        'articles': articles
    }

    return render(request, "home.html", context)

def register(request):
    
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already in use!')
                return redirect('/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already in use!')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                return redirect('/login')
        else:
            messages.info(request, 'Password not match!')
            return redirect('/register')

    return render(request, "register.html")

def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/login')

    else:
        return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_authenticated:
        author = request.user
        articles = Article.objects.filter(author=author)
        context = {
            'articles': articles,
        }

    return render(request, "dashboard.html", context)

def add_article(request):

    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']

        article = Article(title=title, content=content, image=image)
        article.author = request.user
        article.save()
        
        return redirect('/')

    return render(request, 'add_article.html')

def search(request):

    query = request.GET['query']
    if len(query)>78:
        allPosts = []
    else:
        allArticlesTitle = Article.objects.filter(title__icontains=query)
        allArticlesContent = Article.objects.filter(content__icontains=query)
        allArticles = allArticlesTitle.union(allArticlesContent)
    context = {
        'allArticles': allArticles,
        'query': query,
    }

    return render(request, 'search.html', context)

def detail(request, blog_id):

    article = get_object_or_404(Article, id=blog_id)
    comments = BlogComment.objects.filter(article=article)

    stuff = get_object_or_404(Article, id=blog_id)
    total_likes = stuff.total_likes()

    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True

    context = {
        'article': article,
        'comments': comments,
        'user': request.user,
        "total_likes": total_likes,
        "liked": liked,
    }
    
    return render(request, 'detail.html', context)

def postComment(request):

    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        articleId = request.POST.get("articleId")
        article = Article.objects.get(id=articleId)

        comment = BlogComment(comment=comment, user=user, article=article)
        comment.save()
        messages.success(request, "Your comment has been posted successfully!")

    return redirect('/')

def editBlog(request, blog_id):
    
        article = Article.objects.get(id=blog_id)
    
        if request.method == "POST":
            if len(request.FILES) != 0:
                if len(article.image) > 0:
                    os.remove(article.image.path)
                article.image = request.FILES['image']
            article.title = request.POST.get('title')
            article.content = request.POST.get('content')
    
            article.author = request.user
            article.save()
            messages.success(request, "Blog Updated Successfully!")
            return redirect('/dashboard')
    
        context = {
            'article': article
        }
    
        return render(request, 'editBlog.html', context)

def LikeView(request, id):
    article = get_object_or_404(Article, id=request.POST.get('article_id'))
    liked = False

    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True

    article.likes.add(request.user)
    return HttpResponseRedirect(reverse('detail', args=[str(id)]))
