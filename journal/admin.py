from django.contrib import admin
from .models import Article, ContactMessage

# Register your models here.


@admin.register(Article) # A cleaner way to register
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_featured') # Display these fields in the list view
    list_filter = ('author', 'created_at','is_featured')  # Add filters to the right sidebar
    search_fields = ('title', 'summary')  # Add a search bar
    date_hierarchy = 'created_at'  # Add date navigation
    ordering = ('-created_at',) #order by newest first
    prepopulated_fields = {'title': ('title',)} #automatically fill the slug field
    fields = ('title', 'author', 'summary', 'pdf_file', 'image', 'is_featured') #order the fields in the add/edit form
    # raw_id_fields = ('author',) # Use a raw ID field for ForeignKey (improves performance with many related objects)
    # readonly_fields = ('created_at', 'updated_at') #make fields read only
    
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')  # Fields to display in the admin list view
    search_fields = ('name', 'email', 'subject')  # Allow searching by these fields
    list_filter = ('created_at',)  # Filter messages by creation date