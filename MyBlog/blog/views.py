from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from .models import Post

def post_list(request):
    post_list = Post.published.all()
    
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer, get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range, get the last page of results
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/post/list.html', {'posts': posts})



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
                             publish__day=day)
    
    # Render the post detail template with the post context
    return render(request, 'blog/post/detail.html', {'post': post})