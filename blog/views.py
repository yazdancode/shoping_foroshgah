from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from blog.models import Post


def index(request):
    return HttpResponse("be weblog welcome")


def postlist(request):
    posts = Post.objects.filter(status="published")
    return render(request, "blog/postlist.html", {"posts": posts})


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
    return render(request, "blog/post_details.html", {"post": post})
