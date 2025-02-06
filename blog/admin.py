from django.contrib import admin
from jalali_date import datetime2jalali

from blog.models import Post


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
