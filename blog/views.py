from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from blog.forms import AccountForm, ShareForm
from blog.models import Account, Post
from django.core.mail import send_mail


def index(request):
    return render(request, "blog/index.html", {})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/postlist.html"


def post_details(request, slug, pk):
    post = get_object_or_404(Post, status="published", slug=slug, id=pk)
    return render(request, "blog/post/post_details.html", {"post": post})


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
