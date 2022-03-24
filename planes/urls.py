from django.urls import path
from . import views


urlpatterns = [
    path("add-comment-like/<int:id>/<str:url>/", views.AddCommentLike.as_view(), name='add-comment-like'),
    path("add-airplane-like/<int:id>/<str:redirect_address>/<str:chousen_url>/",
         views.AddAirplaneLike.as_view(), name='add-airplane-like'),
    path("tag-plane/<int:id>/<str:redirect_address>/<str:chousen_url>/", views.TagPlane.as_view(), name='tag-plane'),
    # path("order-by-nation/<str:url>/", views.OrderByNation.as_view(), name='order_by_nation'),
    # path("order-by-category/<str:url>/", views.OrderByCategory.as_view(), name='order_by_category'),
    path("order-by-nation/<str:url>/", views.OrderBy.as_view(), name='order_by_nation'),
    path("order-by-category/<str:url>/", views.OrderBy.as_view(), name='order_by_category'),
    path("saved-planes/", views.SavedPlanes.as_view(), name='saved_planes'),
    path("plane_info/<str:url>/", views.PlaneInfo.as_view(), name="plane_info"),
    path("add-comment-to-plane/<str:url>", views.AddComment.as_view(), name='add_comment_to_plane'),
    path("delete-comment/<str:url>/<int:id>", views.DeleteComment.as_view(), name='delete_comment'),
    path("", views.Login.as_view(), name='login'),
    path("logout/", views.Logout.as_view(), name='logout'),
    path("registration/", views.Registration.as_view(), name="registration"),
    path("news/", views.News.as_view(), name="news"),
    path("add-news/", views.CreateNews.as_view(), name="add_news"),
    path("delete_news/<int:id>/", views.DeleteNews.as_view(), name="delete_news"),
    path("add-category/", views.CreateCategory.as_view(), name="add_category"),
    path("delete-category/<str:url>/", views.DeleteCategory.as_view(), name="delete_category"),
    path("add-nation/", views.CreateNation.as_view(), name="add_nation"),
    path("add-plane/", views.CreatePlane.as_view(), name="add_plane"),
    path("the-main-page", views.AirPlaneView.as_view(), name='the-main-page'),
]
