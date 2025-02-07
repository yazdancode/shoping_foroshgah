from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from blog.models import Post


def index(request):
    return render(request, "blog/index.html", {})


def postlist(request):
    posts = Post.objects.filter(status="published")
    paginator = Paginator(posts, 2)
    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/postlist.html", {"posts": posts})


def post_details(
    request,
    year,
    month,
    day,
    post,
):
    post = get_object_or_404(
        Post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )
    return render(request, "blog/post/post_details.html", {"post": post})
