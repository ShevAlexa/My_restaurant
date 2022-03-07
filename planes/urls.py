from django.urls import path

from . import views


urlpatterns = [
    path("plane_info/<str:url>/", views.PlaneInfo.as_view(), name="plane_info"),
    path("add-comment-like/<int:id>/<str:url>/", views.AddCommentLike.as_view(), name='add-comment-like'),
    path("add-airplane-like/<int:id>/<str:redirect_address>/<int:nation_id>/",
         views.AddAirplaneLike.as_view(), name='add-airplane-like'),
    path("tag-plane/<int:id>/<str:redirect_address>/<int:nation_id>/", views.TagPlane.as_view(), name='tag-plane'),
    path("order_by_nation/<int:id>/", views.OrderByNation.as_view(), name='order_by_nation'),
    path("saved_planes/", views.SavedPlanes.as_view(), name='saved_planes'),
    path("add_comment_to_plane/<str:url>", views.AddComment.as_view(), name='add_comment_to_plane'),
    path("", views.AirPlaneView.as_view(), name='the-main-page'),
]
