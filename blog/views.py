from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from blog.forms import AccountForm
from blog.models import Account, Post


def index(request):
    return render(request, "blog/index.html", {})


class PostListView(ListView):
    queryset = Post.published.all()  # ✅ حالا از PublishedManager استفاده می‌کنیم
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/postlist.html"


def post_details(request, year, month, day, post):
    post = get_object_or_404(
        Post.published,  # ✅ فقط از پست‌های منتشر شده دریافت می‌کنیم
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )
    return render(request, "blog/post/post_details.html", {"post": post})


def user_account(request):
    user = request.user
    account, created = Account.objects.get_or_create(user=user)  # ✅ جلوگیری از خطای DoesNotExist

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
        # ✅ مقداردهی اولیه فرم با اطلاعات حساب کاربر
        form = AccountForm(initial={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": account.gender,
            "address": account.address,
            "age": account.age,
            "phone": account.phone,
        })

    return render(request, "blog/post/user_account.html", {"form": form, "account": account})
