from django.contrib import admin
from jalali_date import datetime2jalali

from blog.models import Account, Post, Comment


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
    list_display = (
        "user",
        "first_name",
        "last_name",
        "email",
        "phone",
        "gender",
        "address",
        "age",
        "created",
        "updated",
    )
    search_fields = ("user__username", "first_name", "last_name", "email", "phone")
    list_filter = ("gender", "created", "updated")
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
                    "age",
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
    readonly_fields = ("created", "updated")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "body", "active", "publish")
    list_filter = ("created", "updated", "post")
    list_editable = ("active",)
    search_fields = ("name", "body", "active", "publish")
    ordering = ("-created",)
