from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    summary = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='journal/pdfs/', blank=True, null=True)
    image = models.ImageField(upload_to='journal/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ('add_score', 'Can add score to articles'),
        ]

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

    def __str__(self):
        return self.title


class Rating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    judge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_scores')
    score = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('article', 'judge')

    def __str__(self):
        return f"Rating for {self.article.title} by {self.judge.username}: {self.score}"
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=100, blank=True)
    prof_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def has_profile_picture(self):
        return bool(self.prof_picture and self.prof_picture.url)


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('judge', 'Judge'),
        ('normaluser', 'Normal User'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='normaluser')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
