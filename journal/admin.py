from django.contrib import admin
from .models import Article, ContactMessage, UserProfile

# Register your models here.


@admin.register(Article)  # A cleaner way to register
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_featured', 'status')  # Added status field
    list_filter = ('author', 'created_at', 'is_featured', 'status')  # Added status to filters
    search_fields = ('title', 'summary')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    prepopulated_fields = {'title': ('title',)}
    fields = ('title', 'author', 'summary', 'pdf_file', 'image', 'is_featured', 'status')  # Added status to form
    actions = ['approve_articles', 'deny_articles']  # Added actions

    @admin.action(description='Approve selected articles')
    def approve_articles(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Deny selected articles')
    def deny_articles(self, request, queryset):
        queryset.update(status='denied')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)
    
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'status')
    list_filter = ('status', 'role')