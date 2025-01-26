from .forms import RatingForm, RegisterUserForm, LoginForm, ArticleForm
from .models import Article, Rating
from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'journal/article_list.html', {'articles': articles})

@login_required
@permission_required('articles.add_score', raise_exception=True)
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    rating = None
    if request.user.has_perm('articles.add_rating'):
        try:
            rating = Rating.objects.get(article=article, judge=request.user)
            form = RatingForm(instance=rating)
        except Rating.DoesNotExist:
            form = RatingForm()

        if request.method == 'POST':
            form = RatingForm(request.POST, instance=rating)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.article = article
                rating.judge = request.user
                rating.save()
                return redirect('article_detail', pk=pk)
    else:
        form = None

    context = {'article': article, 'form': form}
    return render(request, 'articles/article_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!") # Optional message
                return redirect('article_list') # Redirect to your home page or another appropriate URL
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.") # Form errors
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST. request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'journal/create_article.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('article_list')
