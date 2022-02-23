from django.urls import path

from . import views


urlpatterns = [
    path("add-comment-like/<int:id>/", views.AddCommentLike.as_view(), name='add-comment-like'),
    path("add-airplane-like/<int:id>/", views.AddAirplaneLike.as_view(), name='add-airplane-like'),
    path("tag-plane/<int:id>/", views.TagPlane.as_view(), name='tag-plane'),
    path("", views.AirPlaneView.as_view(), name='the-main-page'),
]
