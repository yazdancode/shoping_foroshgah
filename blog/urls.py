from django.urls import path  # ایمپورت ماژول path برای تعریف مسیرهای URL

from blog.views import (PostListView, index,  # ایمپورت ویوهای موردنیاز
                        post_details)

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
    # مسیر نمایش جزئیات یک پست مشخص که بر اساس تاریخ انتشار و `slug` مشخص می‌شود
    # <int:year> = دریافت مقدار عددی برای سال
    # <int:month> = دریافت مقدار عددی برای ماه
    # <int:day> = دریافت مقدار عددی برای روز
    # <slug:post> = دریافت مقدار اسلاگ برای پست
]
