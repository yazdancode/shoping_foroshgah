from django.contrib import admin
from jalali_date import datetime2jalali

from blog.models import Account, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "status", "get_jalali_publish")
    list_filter = ("status", "publish", "created", "author", "updated")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")
    list_editable = ("status",)
    list_display_links = ("slug",)

    def get_jalali_publish(self, obj):
        return datetime2jalali(obj.publish).strftime("%Y/%m/%d - %H:%M")

    get_jalali_publish.short_description = "تاریخ انتشار (شمسی)"


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    # نمایش فیلدهای مختلف مدل در صفحه‌ی لیست
    list_display = (
        "user",
        "first_name",
        "last_name",
        "email",
        "phone",
        "gender",
        "address",
        "created",
        "updated",
    )

    # فیلدهایی که می‌توانید در جستجو استفاده کنید
    search_fields = ("user__username", "first_name", "last_name", "email", "phone")

    # اضافه کردن فیلدهایی که می‌توان در صفحه ویرایش مدل مشاهده و ویرایش کرد
    list_filter = ("gender", "created", "updated")

    # افزودن امکان ویرایش مدل در صفحه‌ی جزئیات
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "address",
                    "gender",
                    "picture",
                )
            },
        ),
        (
            "تاریخچه",
            {
                "fields": ("created", "updated"),
                "classes": ("collapse",),
            },
        ),
    )

    # فیلدهای قابل ویرایش در صفحه‌ی ویرایش
    readonly_fields = ("created", "updated")
