from django.db.models import Count, Prefetch
from django.shortcuts import render, redirect
from django.views import View
from .models import Dish, Comment, LikeCommentUser


class DishView(View):
    def get(self, request):
        comment_query = Comment.objects.annotate(count_likes=Count("users_likes"))
        comments = Prefetch("comments", comment_query)
        dishes = Dish.objects.prefetch_related(comments)
        return render(request, "dishes/dish_list.html", {"dish_list": dishes})


class AddCommentLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                LikeCommentUser.objects.create(user=request.user, comment_id=id)
            except:
                LikeCommentUser.objects.get(user=request.user, comment_id=id).delete()
        return redirect('the-main-page')
