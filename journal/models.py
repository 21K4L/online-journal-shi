from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Profile(models.Model):
    BRANCH_CHOICES = [
        ('data_science', 'Data Science'),
        ('artificial_intelligence', 'Artificial Intelligence'),
        ('web_development', 'Web Development'),
        ('cybersecurity', 'Cybersecurity'),
        ('machine_learning', 'Machine Learning'),
        # Add more as needed
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=100, blank=True)
    prof_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def has_profile_picture(self):
        return bool(self.prof_picture and self.prof_picture.url)
    
    
class UserProfile(models.Model):
    BRANCH_CHOICES = [
        ('data_science', 'Data Science'),
        ('artificial_intelligence', 'Artificial Intelligence'),
        ('web_development', 'Web Development'),
        ('cybersecurity', 'Cybersecurity'),
        ('machine_learning', 'Machine Learning'),
        # Add more as needed
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    ROLE_CHOICES = [
        ('judge', 'Judge'),
        ('normaluser', 'Normal User'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='normaluser')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    branch = models.CharField(max_length=50, null=True, choices=BRANCH_CHOICES, default='')


    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()} - {self.status}"


class Article(models.Model):
    BRANCH_CHOICES = UserProfile.BRANCH_CHOICES
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    summary = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='journal/pdfs/', blank=True, null=True)
    image = models.ImageField(upload_to='journal/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES, default='data_science')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
        
    class Meta:
        permissions = [
            ('add_score', 'Can add score to articles'),
        ]
    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class Rating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    judge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_scores')
    score = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('article', 'judge')

    def __str__(self):
        return f"Rating for {self.article.title} by {self.judge.username}: {self.score}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"