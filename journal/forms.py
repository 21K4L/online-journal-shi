from django import forms
from .models import Article, Rating
from django.contrib.auth.forms import UserCreationForm

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'pdf_file', 'image']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3})
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']
        widgets = {
            'score': forms.RadioSelect(choices=Rating.score.field.choices),
        }

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = UserCreationForm.Meta.fields

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
