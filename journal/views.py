from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Rating
from .forms import RatingForm, RegisterUserForm, LoginForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Avg
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group, Permission


# Create your views here.

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'journal/article_list.html', {'articles': articles})

@login_required
@permission_required('articles.add_score', raise_exception=True)
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    average_rating = article.ratings.aggregate(Avg('score'))['score__avg'] or 0
    form = RatingForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                article=article, user=request.user, defaults=form.cleaned_data
            )
            return redirect('article_detail', pk=pk)

    return render(request, 'journal/article_detail.html', {
        'article': article, 'average_rating': average_rating, 'form': form
    })

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
                return redirect('home') # Redirect to your home page or another appropriate URL
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
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'journal/create_article.html', {'form': form})