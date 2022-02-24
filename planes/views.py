from django.db.models import Count, Prefetch
from django.shortcuts import render, redirect
from django.views import View
from .models import Airplane, Comment, LikeCommentUser, LikeAirplaneUser, TagAirplaneUser, Nation


class AirPlaneView(View):
    def get(self, request):
        context = {}
        comment_query = Comment.objects.annotate(count_likes=Count("users_likes")).select_related("author")
        comments = Prefetch("comments", comment_query)
        nation = Nation.objects.all()
        plane = Airplane.objects.prefetch_related(comments).select_related("nation", "category")
        context["planes_list"] = plane
        context["nation"] = nation
        return render(request, "planes/planes_list.html", context)


class AddCommentLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                LikeCommentUser.objects.create(user=request.user, comment_id=id)
            except:
                LikeCommentUser.objects.get(user=request.user, comment_id=id).delete()
        return redirect('the-main-page')


class AddAirplaneLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                LikeAirplaneUser.objects.create(user=request.user, model_id=id)
            except:
                LikeAirplaneUser.objects.get(user=request.user, model_id=id).delete()
        return redirect('the-main-page')


class TagPlane(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                TagAirplaneUser.objects.create(user=request.user, model_id=id)
            except:
                TagAirplaneUser.objects.get(user=request.user, model_id=id).delete()
        return redirect('the-main-page')


class OrderByNation(View):
    def get(self, request, id):
        context = {}
        comment_query = Comment.objects.annotate(count_likes=Count("users_likes")).select_related("author")
        comments = Prefetch("comments", comment_query)
        nation = Nation.objects.all()
        plane = Airplane.objects.filter(nation_id=id).prefetch_related(comments).select_related("nation", "category")
        context["planes_list"] = plane
        context["nation"] = nation
        return render(request, "planes/order_by_nation.html", context)
