from django.urls import path

from . import views


urlpatterns = [
    path("add-comment-like/<int:id>/", views.AddCommentLike.as_view(), name='add-comment-like'),
    path("add-airplane-like/<int:id>/", views.AddAirplaneLike.as_view(), name='add-airplane-like'),
    path("tag-plane/<int:id>/", views.TagPlane.as_view(), name='tag-plane'),
    path("order_by_nation/<int:id>/", views.OrderByNation.as_view(), name='order_by_nation'),
    path("", views.AirPlaneView.as_view(), name='the-main-page'),
]
