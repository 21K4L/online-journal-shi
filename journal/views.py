from sqlite3 import IntegrityError
from django.conf import settings
from .forms import ContactMessageForm, RatingForm, LoginForm, ArticleForm, ContactMessageForm, UserForm, ProfileForm, UserRegistrationForm
from .models import Article, Rating, Profile
from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import datetime


# Create your views here.


def home(request):
    featured_articles = Article.objects.filter(is_featured=True).order_by('-created_at')[:5]  # Get the 3 most recent featured articles
    recent_articles = Article.objects.order_by('-created_at')[:5]  # Get the 5 most recent articles
    return render(request, 'journal/home.html', {
                'featured_articles': featured_articles,
                'recent_articles': recent_articles
                })


def about(request):
    about_content = "<h1>This is dynamic content from the view.</h1><p>You can add more HTML here.</p>"
    return render(request, 'journal/about.html', {'about_content': about_content})


def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()  # This will automatically save to the ContactMessage model
            messages.success(request, 'Your message has been sent successfully!')
            submitted = True
            return redirect('contact')  # Redirect after form submission
    else:
        form = ContactMessageForm()

    return render(request, 'journal/contact.html', {
        'form': form,
        'submitted': submitted,
        'contact_email': 'test@test.com',
        'contact_phone': '1234567890',
        'contact_address': 'test address',
    })


@login_required
def create_article(request):
    # Check if the user is approved
    if request.user.userprofile.status != 'approved':
        messages.error(request, "Your account is not approved to submit articles.")
        return redirect('article_list')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Article successfully submitted!")
            return redirect('article_list')
    else:
        form = ArticleForm()

    return render(request, 'journal/create_article.html', {'form': form})


def article_list(request):
    articles = Article.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'journal/article_list.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    # Calculate the average rating for the article
    average_rating = article.ratings.aggregate(Avg('score'))['score__avg'] or 0

    # Retrieve all ratings with comments
    ratings_with_comments = article.ratings.filter(comment__isnull=False).order_by('-id')

    # Fetch the user's rating if they are a judge
    user_rating = None
    if request.user.is_authenticated and request.user.userprofile.role == 'judge':
        try:
            user_rating = Rating.objects.get(article=article, judge=request.user)
        except Rating.DoesNotExist:
            user_rating = None

    context = {
        'article': article,
        'average_rating': average_rating,
        'ratings_with_comments': ratings_with_comments,
        'user_rating': user_rating,  # Show user's previous rating if needed
    }
    return render(request, 'journal/article_detail.html', context)


@login_required
def add_rating(request, pk):
    # Ensure the user is authenticated and has the Judge role
    if request.user.userprofile.role != 'judge':
        messages.error(request, "You are not authorized to rate articles.")
        return redirect('article_detail', pk=pk)

    # Ensure the user's account is approved
    if request.user.userprofile.status != 'approved':
        messages.error(request, "Your account is not approved to add ratings.")
        return redirect('article_detail', pk=pk)

    article = get_object_or_404(Article, pk=pk)

    # Ensure the judge's branch matches the article's branch
    if request.user.userprofile.branch != article.branch:
        messages.error(request, "You can only rate articles in your designated branch.")
        return redirect('article_detail', pk=pk)

    try:
        # Try to fetch the existing rating for the article by the user
        rating = Rating.objects.get(article=article, judge=request.user)
        form = RatingForm(instance=rating)
    except Rating.DoesNotExist:
        rating = None
        form = RatingForm()

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            try:
                rating = form.save(commit=False)
                rating.article = article
                rating.judge = request.user
                rating.save()
                messages.success(request, "Your rating was successfully submitted.")
            except IntegrityError as e:
                messages.error(request, f"Database error occurred: {e}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
            return redirect('article_detail', pk=pk)
        else:
            messages.error(request, "Please correct the errors below.")

    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'journal/add_rating.html', context)


def recent_articles(request):
    recent = Article.objects.filter(created_at__gte=timezone.now() - datetime.timedelta(days=1)).order_by('-created_at')
    return render(request, 'journal/recent.html', {'recent_articles': recent})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
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


def logout_view(request):
    logout(request)
    return redirect('article_list')


@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Create a profile if it doesn't exist
        profile = Profile.objects.create(user=request.user)
    # Check if the user has uploaded any articles
    articles = Article.objects.filter(author=request.user)
    return render(request, 'profile/profile.html', {'profile': profile, 'articles': articles})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile, user=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile, user=request.user)

    return render(request, 'profile/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


def users_guide(request):
    return render(request, 'journal/users_guide.html')


def judges_guide(request):
    return render(request, 'journal/judges_guide.html')