from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from blog.forms import AccountForm
from blog.models import Post


def index(request):
    return render(request, "blog/index.html", {})


# def postlist(request):
#     posts = Post.objects.filter(status="published")
#     paginator = Paginator(posts, 2)
#     page = request.GET.get("page")

#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request, "blog/post/postlist.html", {"posts": posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/postlist.html"


def post_details(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )
    return render(request, "blog/post/post_details.html", {"post": post})


def user_account(request):
    if request.method == "POST":
        form = AccountForm(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AccountForm(data=request.GET)

    return render(request, "blog/post/user_account.html", {"form": form})
