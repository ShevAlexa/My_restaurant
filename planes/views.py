from django.db.models import Count, Prefetch
from django.shortcuts import render, redirect
from django.views import View
from .models import Airplane, Comment, LikeCommentUser, LikeAirplaneUser, TagAirplaneUser, Nation


class AirPlaneView(View):
    def get(self, request):
        context = {}
        nation = Nation.objects.all()
        plane = Airplane.objects.annotate(count_likes=Count("users_likes"))\
            .select_related("nation", "category")\
            .order_by("category_id")
        context["planes_list"] = plane
        context["nation"] = nation
        return render(request, "planes/planes_list.html", context)


class AddCommentLike(View):
    def get(self, request, id, url):
        if request.user.is_authenticated:
            try:
                LikeCommentUser.objects.create(user=request.user, comment_id=id)
            except:
                LikeCommentUser.objects.get(user=request.user, comment_id=id).delete()
        return redirect("plane_info", url)


class AddAirplaneLike(View):
    def get(self, request, id, redirect_address, nation_id):
        if request.user.is_authenticated:
            try:
                LikeAirplaneUser.objects.create(user=request.user, model_id=id)
            except:
                LikeAirplaneUser.objects.get(user=request.user, model_id=id).delete()
        if nation_id == 0:
            return redirect(redirect_address)
        return redirect(redirect_address, id=nation_id)


class TagPlane(View):
    def get(self, request, id, redirect_address, nation_id):
        if request.user.is_authenticated:
            try:
                TagAirplaneUser.objects.create(user=request.user, model_id=id)
            except:
                TagAirplaneUser.objects.get(user=request.user, model_id=id).delete()
        if nation_id == 0:
            return redirect(redirect_address)
        return redirect(redirect_address, id=nation_id)


class OrderByNation(View):
    def get(self, request, id):
        context = {}
        nation = Nation.objects.all()
        plane = Airplane.objects.filter(nation_id=id)\
            .annotate(count_likes=Count("users_likes"))\
            .select_related("nation", "category")\
            .order_by("category_id")
        chosen_nation = Nation.objects.get(id=id)
        context["planes_list"] = plane
        context["nation"] = nation
        context["chosen_nation"] = chosen_nation
        return render(request, "planes/order_by_nation.html", context)


class PlaneInfo(View):
    def get(self, request, url):
        context = {}
        comment_query = Comment.objects.annotate(count_likes=Count("users_likes")).select_related("author")
        comments = Prefetch("comments", comment_query)
        nation = Nation.objects.all()
        plane = Airplane.objects.select_related("nation", "category").prefetch_related(comments).get(url=url)
        context["plane"] = plane
        context["nation"] = nation
        return render(request, "planes/plane_info.html", context)


class SavedPlanes(View):
    def get(self, request):
        context = {}
        nation = Nation.objects.all()
        plane = Airplane.objects.annotate(count_likes=Count("users_likes")) \
            .select_related("nation", "category") \
            .order_by("nation_id")
        context["planes_list"] = plane
        context["nation"] = nation
        return render(request, "planes/saved_planes.html", context)


class AddComment(View):
    def post(self, request, url):
        if request.user.is_authenticated:
            Comment.objects.create(
                text=request.POST['comment_text'],
                author=request.user,
                model=Airplane.objects.get(url=url)
            )
        return redirect('plane_info', url=url)
