from django.urls import path

from . import views


urlpatterns = [
    path("add-comment-like/<int:id>/", views.AddCommentLike.as_view(), name='add-comment-like'),
    path("", views.DishView.as_view(), name='the-main-page'),
]
