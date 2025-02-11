from django.urls import path

from blog.views import PostListView, share_post, index, post_details, user_account

urlpatterns = [
    path("", index, name="index"),
    path("postlist/", PostListView.as_view(), name="postlist"),
    path(
        "post_details/<slug:slug>/<int:pk>/",
        post_details,
        name="post_details",
    ),
    path("user_account/", user_account, name="user_account"),
    # path("contact-us/", contactus, name="contact-us"),
    path("share/<int:post_id>/", share_post, name="share_post"),
]
