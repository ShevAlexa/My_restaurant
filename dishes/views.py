from django.shortcuts import render, redirect
from django.views import View
from .models import Dish, Comment, LikeCommentUser


class DishView(View):
    def get(self, request):
        dishes = Dish.objects.all()
        return render(request, "dishes/dish_list.html", {"dish_list": dishes})


class AddCommentLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                LikeCommentUser.objects.create(user=request.user, comment_id=id)
            except:
                LikeCommentUser.objects.get(user=request.user, comment_id=id).delete()
        #     comment = Comment.objects.get(id=id)
        #     comment.like += 1
        #     comment.save()
        #     comment = Comment.objects.get(id=id)
        #     if request.user in comment.like.all():
        #         comment.like.filter(id=request.user.id).delete()
        #     else:
        #         comment.like.add(request.user)
        #     comment.save()
        return redirect('the-main-page')
