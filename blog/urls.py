from django.urls import path

from blog.views import PostListView, index, post_details, user_account

urlpatterns = [
    path("", index, name="index"),
    # مسیر صفحه اصلی که ویو `index` را اجرا می‌کند
    path("postlist/", PostListView.as_view(), name="postlist"),
    # مسیر نمایش لیست پست‌ها که از کلاس‌بیس ویو `PostListView` استفاده می‌کند
    # `.as_view()` برای تبدیل کلاس به ویو قابل اجرا استفاده می‌شود
    path(
        "post_details/<int:year>/<int:month>/<int:day>/<slug:post>/",
        post_details,
        name="post_details",
    ),
    path("user_account/", user_account, name="user_account"),
]
