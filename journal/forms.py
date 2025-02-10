from django import forms
from .models import Article, ContactMessage, Rating, Profile, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):
    branch = forms.ChoiceField(choices=UserProfile.BRANCH_CHOICES, required=True)
    class Meta:
        model = Article
        fields = ['title', 'summary', 'pdf_file', 'image', 'branch']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3})
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment...'}),
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Your Message'})
        }

    def clean(self):
        cleaned_data = super().clean()
        if not all(cleaned_data.values()):
            raise forms.ValidationError("All fields are required.")
        return cleaned_data


class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role=self.cleaned_data['role'])
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'prof_picture', 'location', 'branch']
        widgets = {
            'branch': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass user when initializing the form
        super().__init__(*args, **kwargs)
        if user and user.userprofile.role != 'judge':  # Hide branch if not a judge
            self.fields.pop('branch')