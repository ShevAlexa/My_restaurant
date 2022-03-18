from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count, Prefetch
from django.shortcuts import render, redirect
from django.views import View
from .models import Airplane, Comment, LikeCommentUser, LikeAirplaneUser, TagAirplaneUser, Nation, NewsModel, Category


class AirPlaneView(View):
    def get(self, request):
        context = dict()
        search_query = request.GET.get('search', '')

        if search_query:
            plane = Airplane.objects.filter(model__icontains=search_query)\
                .annotate(count_likes=Count("users_likes")) \
                .select_related("nation", "category")\
                .prefetch_related("users_tags", "users_likes")\
                .order_by("category_id", "model")
        else:
            plane = Airplane.objects.annotate(count_likes=Count("users_likes"))\
                .select_related("nation", "category")\
                .prefetch_related("users_tags", "users_likes")\
                .order_by("category_id", "model")
        context["planes_list"] = plane
        nation = Nation.objects.all()
        context["nation"] = nation
        category = Category.objects.all()
        context['category'] = category
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
    def get(self, request, id, redirect_address, chousen_id):
        if request.user.is_authenticated:
            try:
                LikeAirplaneUser.objects.create(user=request.user, model_id=id)
            except:
                LikeAirplaneUser.objects.get(user=request.user, model_id=id).delete()
        if chousen_id == 0:
            return redirect(redirect_address)
        return redirect(redirect_address, id=chousen_id)


class TagPlane(View):
    def get(self, request, id, redirect_address, chousen_id):
        if request.user.is_authenticated:
            try:
                TagAirplaneUser.objects.create(user=request.user, model_id=id)
            except:
                TagAirplaneUser.objects.get(user=request.user, model_id=id).delete()
        if chousen_id == 0:
            return redirect(redirect_address)
        return redirect(redirect_address, id=chousen_id)


class OrderByNation(View):
    def get(self, request, id):
        context = dict()
        plane = Airplane.objects.filter(nation_id=id)\
            .annotate(count_likes=Count("users_likes"))\
            .select_related("nation", "category")\
            .prefetch_related("users_tags", "users_likes")\
            .order_by("category_id", "model")
        context["planes_list"] = plane
        chosen_nation = Nation.objects.get(id=id)
        context["chosen_nation"] = chosen_nation
        nation = Nation.objects.all()
        context["nation"] = nation
        category = Category.objects.all()
        context['category'] = category
        return render(request, "planes/order_by_nation.html", context)


class OrderByCategory(View):
    def get(self, request, id):
        context = dict()
        plane = Airplane.objects.filter(category_id=id)\
            .annotate(count_likes=Count("users_likes"))\
            .select_related("nation", "category")\
            .prefetch_related("users_tags", "users_likes")\
            .order_by("nation", "model")
        chosen_category = Category.objects.get(id=id)
        context["chosen_category"] = chosen_category
        context["planes_list"] = plane
        nation = Nation.objects.all()
        context["nation"] = nation
        category = Category.objects.all()
        context['category'] = category
        return render(request, "planes/order_by_category.html", context)


class PlaneInfo(View):
    def get(self, request, url):
        context = dict()
        comment_query = Comment.objects.annotate(count_likes=Count("users_likes")).select_related("author")
        comments = Prefetch("comments", comment_query)
        plane = Airplane.objects.select_related("nation", "category").prefetch_related(comments).get(url=url)
        context["plane"] = plane
        nation = Nation.objects.all()
        context["nation"] = nation
        category = Category.objects.all()
        context['category'] = category
        return render(request, "planes/plane_info.html", context)


class SavedPlanes(View):
    def get(self, request):
        context = dict()
        plane = Airplane.objects.annotate(count_likes=Count("users_likes")) \
            .select_related("nation", "category")\
            .prefetch_related("users_tags", "users_likes") \
            .order_by("nation_id", "category_id", "model")
        context["planes_list"] = plane
        nation = Nation.objects.all()
        context["nation"] = nation
        category = Category.objects.all()
        context['category'] = category
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


class DeleteComment(View):
    def get(self, request, id, url):
        if request.user.is_authenticated and request.user.is_superuser:
            Comment.objects.get(id=id).delete()
        return redirect("plane_info", url=url)


class News(View):
    def get(self, request):
        context = dict()
        news = NewsModel.objects.order_by("-date")
        context["news"] = news
        nation = Nation.objects.all()
        context["nation"] = nation
        category = Category.objects.all()
        context['category'] = category
        return render(request, "planes/news.html", context)


class Login(LoginView):
    template_name = 'planes/login.html'


class Logout(LogoutView):
    template_name = 'planes/logout.html'


# UserRegistration

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, "planes/registration.html", {'form': form})
