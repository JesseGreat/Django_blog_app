from django.contrib import admin
from .models import Post, Comment

# Customizing how Post model is displayed
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['tittle', 'slug', 'author', 'publish', 'status']  # Display specified Post fields in the admin panel
    list_filter = ['status', 'created', 'publish', 'author']  # Filter the Post fields by the specified values
    search_fields = ['tittle', 'body']  # Provide a search bar to search for a post by the given values
    prepopulated_fields = {'slug': ('tittle',)}  # Automatically fill the slug field with the title field
    raw_id_fields = ['author']
    date_hierarchy = 'publish'  # Provide navigation links to navigate through a date hierarchy
    ordering = ['status', 'publish']  # Specify the sorting criteria; posts are ordered by status and publish date by default


# Customizing how Comment model is displayed
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Comment model.
    """
    list_display = ['name', 'email', 'post', 'created', 'active']  # Display specified Comment fields in the admin panel
    list_filter = ['active', 'created', 'updated']  # Filter the Comment fields by the specified values
    search_fields = ['name', 'email', 'body']  # Provide a search bar to search for a comment by the given values
