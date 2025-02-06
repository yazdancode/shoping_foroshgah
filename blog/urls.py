from django.urls import path

from blog.views import index, post_details, postlist

urlpatterns = [
    path("", index, name="index"),
    path("postlist/", postlist, name="postlist"),
    path(
        "post_details/<int:year>/<int:month>/<int:day>/<slug:post>/",
        post_details,
        name="post_details",
    ),
]
