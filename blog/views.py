from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from blog.models import Post  # ایمپورت مدل پست از اپلیکیشن بلاگ


def index(request):
    """
    صفحه اصلی وبلاگ را رندر می‌کند.
    """
    return render(request, "blog/index.html", {})


# نسخه‌ی مبتنی بر فانکشن ویو برای نمایش لیست پست‌ها (کامنت شده)
# def postlist(request):
#     """
#     نمایش لیست پست‌های منتشر شده همراه با قابلیت صفحه‌بندی
#     """
#     posts = Post.objects.filter(status="published")  # دریافت پست‌های منتشر شده
#     paginator = Paginator(posts, 2)  # ایجاد صفحه‌بندی با نمایش ۲ پست در هر صفحه
#     page = request.GET.get("page")  # دریافت شماره صفحه از URL

#     try:
#         posts = paginator.page(page)  # دریافت پست‌های مربوط به صفحه مورد نظر
#     except PageNotAnInteger:
#         posts = paginator.page(1)  # اگر مقدار صفحه عدد نباشد، صفحه اول نمایش داده می‌شود
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)  # اگر صفحه از محدوده خارج باشد، آخرین صفحه نمایش داده می‌شود

#     return render(request, "blog/post/postlist.html", {"posts": posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'  # مقدار 'posts' را در قالب ارسال می‌کند
    paginate_by = 2
    template_name = 'blog/post/postlist.html'


def post_details(request, year, month, day, post):
    """
    نمایش جزئیات یک پست خاص براساس تاریخ انتشار و اسلاگ
    """
    post = get_object_or_404(
        Post,  # مدل موردنظر
        status="published",  # فیلتر کردن پست‌های منتشر شده
        publish__year=year,  # فیلتر بر اساس سال انتشار
        publish__month=month,  # فیلتر بر اساس ماه انتشار
        publish__day=day,  # فیلتر بر اساس روز انتشار
        slug=post,  # فیلتر بر اساس اسلاگ (نامک) پست
    )
    return render(request, "blog/post/post_details.html", {"post": post})  # ارسال پست به قالب جهت نمایش
