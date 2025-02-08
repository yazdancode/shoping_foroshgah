from django.urls import path

from blog.views import PostListView, index, post_details, user_account

urlpatterns = [
    path("", index, name="index"),
    path("postlist/", PostListView.as_view(), name="postlist"),
    path(
        "post_details/<int:year>/<int:month>/<int:day>/<slug:post>/",
        post_details,
        name="post_details",
    ),
    path("user_account/", user_account, name="user_account"),
]
