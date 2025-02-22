from django.urls import path

from blog.views import (
    change_password,
    index,
    logout_view,
    post_details,
    postlist,
    search,
    share_post,
    user_account,
    user_login,
)

urlpatterns = [
    path("", index, name="index"),
    path("postlist/", postlist, name="postlist"),
    path("postlist/<slug:tag_slug>/", postlist, name="postlist_tag"),
    path(
        "post_details/<slug:slug>/<int:pk>/",
        post_details,
        name="post_details",
    ),
    path("user_account/", user_account, name="user_account"),
    path("share/<int:post_id>/", share_post, name="share_post"),
    path("search/", search, name="search"),
    path("search/<slug:tag_slug>/", search, name="search_by_tag"),
    path("login/", user_login, name="login"),
    path("logout/", logout_view, name="logout"),
    path("change-password/", change_password, name="change_password"),
]
