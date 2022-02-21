from django.db.models import Count, Prefetch
from django.shortcuts import render, redirect
from django.views import View
from .models import Airplane, Comment, LikeCommentUser


class AirPlaneView(View):
    def get(self, request):
        # comment_query = Comment.objects.annotate(count_likes=Count("users_likes"))
        comments = Prefetch("comments")
        plane = Airplane.objects.prefetch_related(comments)
        return render(request, "planes/planes_list.html", {"planes_list": plane})


class AddCommentLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                LikeCommentUser.objects.create(user=request.user, comment_id=id)
            except:
                LikeCommentUser.objects.get(user=request.user, comment_id=id).delete()
        return redirect('the-main-page')
