from django.db import models
from django.utils import timezone 
from django.conf import settings #This is the project settings(settings.auth_user_model) imported to define relationship between users and posts, it allows us to know the exact user that made a post
from django.urls import reverse
from taggit.managers import TaggableManager #django taggit modules that allows categorizing posts which aid easy search, retreival or querying
# Create your models here.

#Customizing/creating my own model manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return(super().get_queryset().filter(status=Post.Status.PUBLISHED))

class Post(models.Model):
    
    """Adding a status field: This is a subclass thats used to manage the status of blog posts, it depicts if a particular post is to be saved
    as draft or published, meanwhine its being defualted to draft
    """
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
    #Blog Post fields
    tittle = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish') #creating a unique slug so that we dont have duplicate slug in the database
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts') 
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT) #select your choice if its to be saved as draft or publised
    objects = models.Manager() #setting the defaults manager to query database which is Object manager
    published = PublishedManager() #customized object manager
    tags = TaggableManager() #This manager will allow you one to add, retrieve, and remove tags from Post objects.
    
    #setting a query database indexes using the publish field for optimization sake
    class Meta:
        ordering = ['-publish'] #set a default sort order using the publish field in descending order, hence the reason for the hypen before publish
        indexes = [models.Index(fields=['-publish']),] #A database index is a way to improve the speed of data retrieval operations on a database table. Think of it like an index at the back of a book, which helps you quickly find the page number where a particular topic is discussed.
    
    
    def __str__(self):
        return self.tittle
    
    "using the post detail in the url patterns to build a canonical url for post objects"
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    """
    Model representing a comment on a blog post.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        """
        Meta options for the Comment model.
        """
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        """
        String representation of the Comment model.
        """
        return f'Comment by {self.name} on {self.post}'