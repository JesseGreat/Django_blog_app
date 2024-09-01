from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
# from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag #This is use to categorize post of the same or similar contents
from django.db.models import Count


"""
class PostListView(ListView): #Alternative post list view
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
"""

    
def post_list(request, tag_slug=None):
    # Get all published posts
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        # Filter posts by the selected tag
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        # Get the posts for the current page
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer, return the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range, return the last page of results
        posts = paginator.page(paginator.num_pages)

    # Render the template with the posts and selected tag
    return render(request, 'blog/post/list.html', {
        'posts': posts,
        'tag': tag,
    })

def post_detail(request, year, month, day, post):
    """
    View function to display a single post detail.

    Args:
        request (HttpRequest): The request object sent by the user.
        year (int): Year part of the post's publication date.
        month (int): Month part of the post's publication date.
        day (int): Day part of the post's publication date.
        post (str): Slug of the post to be displayed.

    Returns:
        HttpResponse: Rendered template with the post detail.

    Raises:
        Http404: If the requested post does not exist or is not published.

    """
    # Retrieve the post using get_object_or_404 shortcut, ensuring it is published
    post = get_object_or_404(Post, 
                             status=Post.Status.PUBLISHED, 
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day) #list of active comments for this post
    comments = post.comments.filter(active=True) #form for users to comment
    form = CommentForm()
    
    #List of similar posts (implementing the django taggit)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    
    
    # Render the post detail template with the post context
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form, 'similar_posts':similar_posts})

# Define a function called post_share that takes a request and a post_id as arguments
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{cd['name']} ({cd['email']}) recommends you read {post.tittle}")
            message = (f"Read {post.tittle} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}")
            
            # Send email
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid(): #create a coment object without saving it to the database
        comment = form.save(commit=False) #Assign the post to the comment
        comment.post = post # save the comment to the database
        comment.save()
        return render(request, 'blog/post/comment.html',{'post':post, 'form':form, 'comment':comment})
            
        
    
