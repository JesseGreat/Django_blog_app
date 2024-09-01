from django import template
from ..models import Post
from django.db.models import Count #This was imported to count and to get the posts that has the highest no of comment
import markdown 
from django.utils.safestring import mark_safe #importing the markdown text easy format


register = template.Library()

#This is a simple tag to return the total number of blog posts
@register.simple_tag
def total_posts():
    return Post.published.count()

#This is an inclusion tag to return the total number of blog posts
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

#a tag to show the post that has the highest comments
@register.simple_tag
def get_most_commented_posts(count=3):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

#implementing the markdown functionalities 
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))





