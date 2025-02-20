from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import Greatest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from taggit.models import Tag

from blog.forms import AccountForm, CommentForm, ShareForm, LoginForm, SearchForm
from blog.models import Account, Post


def index(request):
    return render(request, "blog/index.html", {})


def postlist(request, tag_slug=None):
    posts = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=tag)

    paginator = Paginator(posts, 10)
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return render(request, "blog/post/postlist.html", {"posts": posts, "tag": tag})


def post_details(request, slug, pk):
    post = get_object_or_404(Post, status="published", slug=slug, id=pk)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(s_count=Count("title")).order_by(
        "-s_count", "-publish"
    )[:2]

    context = {
        "post": post,
        "new_comment": new_comment,
        "comments": comments,
        "comment_form": comment_form,
        "similar_posts": similar_posts,
    }
    return render(request, "blog/post/post_details.html", context)


def user_account(request):
    user = request.user
    account, created = Account.objects.get_or_create(user=user)

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()
            account.gender = form.cleaned_data["gender"]
            account.address = form.cleaned_data["address"]
            account.age = form.cleaned_data["age"]
            account.phone = form.cleaned_data["phone"]
            account.save()
            return redirect("index")
    else:
        form = AccountForm(
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "gender": account.gender,
                "address": account.address,
                "age": account.age,
                "phone": account.phone,
            }
        )

    return render(
        request, "blog/form/user_account.html", {"form": form, "account": account}
    )


def share_post(request, post_id):
    post = get_object_or_404(Post, status="published", id=post_id)
    sent = False
    if request.method == "POST":
        form = ShareForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            full_name = cd["full_name"]
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = "{} شما را به خواندن {} دعوت کرده است".format(
                full_name, post.title
            )
            to = cd["to"]
            message = cd["message"]

            msg = '{} شما را به خواندن پست "{}" در آدرس زیر دعوت کرده است:\n\n{}\n\n{}'.format(
                full_name, post.title, message, post_url
            )

            send_mail(subject, msg, "yshabanei@gmail.com", [to], fail_silently=False)

            sent = True
            form = ShareForm()
    else:
        form = ShareForm()

    return render(
        request, "blog/form/share_post.html", {"form": form, "sent": sent, "post": post}
    )


def search(request, tag_slug=None):
    form = SearchForm(request.GET)
    query = ""
    tag = None
    results = Post.published.all()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        results = results.filter(tags=tag)

    if form.is_valid():
        query = form.cleaned_data["search_input"].strip()
        if query:
            request.session["query"] = query
        else:
            query = request.session.get("query", "")

    if query:
        search_vector = SearchVector("body", weight="B", config="persian") + \
                        SearchVector("title", weight="A", config="persian")
        search_query = SearchQuery(query, config="persian", search_type="plain")

        results = (
            results.annotate(
                similarity=Greatest(
                    TrigramSimilarity("body", query), TrigramSimilarity("title", query)
                ),
                search=search_vector,
                rank=SearchRank(search_vector, search_query),
            )
            .filter(rank__gte=0.2, similarity__gte=0.05)
            .order_by("-rank", "-similarity")
        )

    paginator = Paginator(results, 4)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    return render(
        request,
        "blog/post/postlist.html",
        {"posts": posts, "tag": tag, "page": page, "form": form},
    )


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "شما با موفقیت وارد شدید.")
                    return redirect(reverse("index"))
                else:
                    messages.error(request, "حساب کاربری شما غیرفعال است.")
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = LoginForm()

    return render(request, "blog/form/account/login.html", {"form": form})
