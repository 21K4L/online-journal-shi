from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    summary = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='journal/pdfs/', blank=True, null=True)
    image = models.ImageField(upload_to='journal/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Rating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    judge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_scores')
    score = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('article', 'judge')

    def __str__(self):
        return f"Rating for {self.article.title} by {self.judge.username}: {self.score}"