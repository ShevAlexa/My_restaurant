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
    def get(self, request, id, redirect_address, chousen_url):
        if request.user.is_authenticated:
            try:
                LikeAirplaneUser.objects.create(user=request.user, model_id=id)
            except:
                LikeAirplaneUser.objects.get(user=request.user, model_id=id).delete()
        if chousen_url == 'None':
            return redirect(redirect_address)
        return redirect(redirect_address, url=chousen_url)


class TagPlane(View):
    def get(self, request, id, redirect_address, chousen_url):
        if request.user.is_authenticated:
            try:
                TagAirplaneUser.objects.create(user=request.user, model_id=id)
            except:
                TagAirplaneUser.objects.get(user=request.user, model_id=id).delete()
        if chousen_url == 'None':
            return redirect(redirect_address)
        return redirect(redirect_address, url=chousen_url)


class OrderByNation(View):
    def get(self, request, url):
        context = dict()
        filter_id = Nation.objects.get(url=url).id
        plane = Airplane.objects.filter(nation_id=filter_id)\
            .annotate(count_likes=Count("users_likes"))\
            .select_related("nation", "category")\
            .prefetch_related("users_tags", "users_likes")\
            .order_by("category_id", "model")
        context["planes_list"] = plane
        chosen_nation = Nation.objects.get(url=url)
        context["chosen_nation"] = chosen_nation
        nation = Nation.objects.all()
        context["nation"] = nation
        category = Category.objects.all()
        context['category'] = category
        return render(request, "planes/order_by_nation.html", context)


class OrderByCategory(View):
    def get(self, request, url):
        context = dict()
        filter_id = Category.objects.get(url=url).id
        plane = Airplane.objects.filter(category_id=filter_id)\
            .annotate(count_likes=Count("users_likes"))\
            .select_related("nation", "category")\
            .prefetch_related("users_tags", "users_likes")\
            .order_by("nation", "model")
        chosen_category = Category.objects.get(url=url)
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


# equipment for admin


# class CreatePlane(View):
#     def post(self, request):
#         if request.user.is_authenticated and request.user.is_superuser:
#             Airplane.objects.create(
#                 model=request.POST['model'],
#                 cruising_speed=request.POST['cruising_speed'],
#                 constructor=request.POST['constructor'],
#                 engine_type=request.POST['engine_type'],
#                 production_volume=request.POST['production_volume'],
#                 reference=request.POST['reference'],
#                 image=request.POST[],                                                                # should will fix
#                 nation=request.POST['nation'],
#                 category=request.POST['category'],
#
#                 likes=0,
#
#                 tag=0,
#             )
#         return redirect('the-main-page')
#
#
# class DeletePlane(View):
#     def get(self, request, id):
#         if request.user.is_authenticated and request.user.is_superuser:
#             Airplane.objects.get(id=id).delete()
#         return redirect("the-main-page")
#
#
# class CreateNation(View):
#     def post(self, request):
#         if request.user.is_authenticated and request.user.is_superuser:
#             Nation.objects.create(
#                 country=request.POST['nation'],
#                 image=request.POST[],                                                                # should will fix
#             )
#         return redirect('the-main-page')
#
#
# class DeleteNation(View):
#     def get(self, request, id):
#         if request.user.is_authenticated and request.user.is_superuser:
#             Nation.objects.get(id=id).delete()
#         return redirect("the-main-page")


class CreateCategory(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            context = dict()
            plane = Airplane.objects.annotate(count_likes=Count("users_likes")) \
                .select_related("nation", "category") \
                .prefetch_related("users_tags", "users_likes") \
                .order_by("nation_id", "category_id", "model")
            context["planes_list"] = plane
            nation = Nation.objects.all()
            context["nation"] = nation
            category = Category.objects.all()
            context['category'] = category
            return render(request, "planes/add_category.html", context)

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            Category.objects.create(
                name=request.POST['category_name'],
            )
        return redirect('the-main-page')


class DeleteCategory(View):
    def get(self, request, url):
        if request.user.is_authenticated and request.user.is_superuser:
            Category.objects.get(url=url).delete()
        return redirect("the-main-page")


class CreateNews(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            context = dict()
            plane = Airplane.objects.annotate(count_likes=Count("users_likes")) \
                .select_related("nation", "category") \
                .prefetch_related("users_tags", "users_likes") \
                .order_by("nation_id", "category_id", "model")
            context["planes_list"] = plane
            nation = Nation.objects.all()
            context["nation"] = nation
            category = Category.objects.all()
            context['category'] = category
            return render(request, "planes/add_news.html", context)

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            NewsModel.objects.create(
                title=request.POST['title'],
                text=request.POST['text'],
            )
            return redirect('news')


class DeleteNews(View):
    def get(self, request, id):
        if request.user.is_authenticated and request.user.is_superuser:
            NewsModel.objects.get(id=id).delete()
        return redirect("news")
