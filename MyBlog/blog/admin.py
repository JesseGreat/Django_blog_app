from django.contrib import admin
from .models import Post

# Register your models here.
@admin.register(Post)

#customizing how models are displayed
class PostAdmin(admin.ModelAdmin):
    list_display = ['tittle', 'slug', 'author', 'publish', 'status'] #display some specified Post field in the admin panel 
    list_filter = ['status', 'created', 'publish', 'author'] #filter the Post field by the value of list_filter specified
    search_fields = ['tittle', 'body'] #provide a search bar for you to be able to searh for a post by the given value
    prepopulated_fields = {'slug':('tittle',)} #this allow your slug field to be automatically filled with the tittle field
    raw_id_fields = ['author']
    date_hierarchy = 'publish' #provide navigation links to navigate through a date hierarchy
    ordering = ['status', 'publish'] #specified the sorting criteria, This by default, post are ordered by status and publish
    show_facets = admin.ShowFacets.ALWAYS #cacet filters, these counts indicate the number of objects corresponding to each specific filter, making it easier to identify matching objects in the admin changelist view.
        