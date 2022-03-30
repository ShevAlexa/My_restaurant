import shutil

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


class OrderBy(View):
    def get(self, request, url):
        context = dict()

        # Order by nation
        try:
            filter_id = Nation.objects.get(url=url).id
            plane = Airplane.objects.filter(nation_id=filter_id) \
                .annotate(count_likes=Count("users_likes")) \
                .select_related("nation", "category") \
                .prefetch_related("users_tags", "users_likes") \
                .order_by("category_id", "model")
            chosen_nation = Nation.objects.get(url=url)
            context["chosen_nation"] = chosen_nation
            render_url = "planes/order_by_nation.html"

        # Order by category
        except:
            filter_id = Category.objects.get(url=url).id
            plane = Airplane.objects.filter(category_id=filter_id) \
                .annotate(count_likes=Count("users_likes")) \
                .select_related("nation", "category") \
                .prefetch_related("users_tags", "users_likes") \
                .order_by("nation", "model")
            chosen_category = Category.objects.get(url=url)
            context["chosen_category"] = chosen_category
            render_url = "planes/order_by_category.html"

        # General part
        context["planes_list"] = plane
        nation = Nation.objects.all()
        context["nation"] = nation
        category = Category.objects.all()
        context['category'] = category
        return render(request, render_url, context)


class PlaneInfo(View):
    def get(self, request, url):
        return render(request, "planes/plane_info.html", plane_info_context(url))


class SavedPlanes(View):
    def get(self, request):
        return render(request, "planes/saved_planes.html", create_context())


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


class Registration(View):
    def get(self, request):
        form = UserCreationForm()
        mistake = ""
        return render(request, "planes/registration.html", {'form': form, "mistake": mistake})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = UserCreationForm()
            mistake = "Any mistake, please TRY again"
            return render(request, "planes/registration.html", {'form': form, "mistake": mistake})


# equipment for admin


class CreatePlane(View):
    # class for creating plane in nav-bar module

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, "planes/add_plane.html", create_context())

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            shutil.copy(f"C:/Users/User/OneDrive/Рабочий стол/images/{request.POST['image']}",
                        "D:/PyCharm/IT_OVERONE/my_restaurant/my_restaurant/media/planes")
            image = f"planes/{request.POST['image']}"

            Airplane.objects.create(
                model=request.POST['model'],
                cruising_speed=request.POST['cruising_speed'],
                constructor=request.POST['constructor'],
                engine_type=request.POST['engine_type'],
                production_volume=request.POST['production_volume'],
                reference=request.POST['reference'],
                image=image,
            )
        plane = Airplane.objects.get(model=request.POST['model'])
        plane.nation = Nation.objects.get(country__icontains=request.POST['nation'])
        plane.category = Category.objects.get(name__icontains=request.POST['category'])
        plane.save()
        return redirect('the-main-page')


class EditPlane(PlaneInfo):
    # class for make some changes in plane

    def get(self, request, url):
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, "planes/edit_plane.html", plane_info_context(url))

    def post(self, request, url):
        if request.user.is_authenticated and request.user.is_superuser:

            plane = Airplane.objects.get(url=url)

            try:
                shutil.copy(f"C:/Users/User/OneDrive/Рабочий стол/images/{request.POST['image']}",
                            "D:/PyCharm/IT_OVERONE/my_restaurant/my_restaurant/media/planes")
            except:
                print("image already in dir")

            plane.model = request.POST.get('model')
            plane.cruising_speed = request.POST.get('cruising_speed')
            plane.constructor = request.POST.get('constructor')
            plane.engine_type = request.POST.get('engine_type')
            plane.production_volume = int(request.POST.get('production_volume'))
            plane.reference = request.POST.get('reference')
            plane.image = f"planes/{request.POST['image']}"
            plane.nation = Nation.objects.get(country__icontains=request.POST['nation'])
            plane.category = Category.objects.get(name__icontains=request.POST['category'])
            plane.save()

            return redirect("plane_info", url=plane.url)


class DeletePlane(View):
    # class for delete plane from plane_list

    def get(self, request, url):
        if request.user.is_authenticated and request.user.is_superuser:
            Airplane.objects.get(url=url).delete()
            return redirect('the-main-page')


class CreateNation(View):
    # class for creating nation in nav-bar module

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, "planes/add_nation.html", create_context())

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            shutil.copy(f"C:/Users/User/OneDrive/Рабочий стол/images/{request.POST['image']}",
                        "D:/PyCharm/IT_OVERONE/my_restaurant/my_restaurant/media/planes")

            image = f"planes/{request.POST['image']}"
            Nation.objects.create(
                country=request.POST['country'],
                image=image,
            )
        return redirect('the-main-page')


class DeleteNation(View):
    # class for delete nation from nation_list

    def get(self, request, url):
        if request.user.is_authenticated and request.user.is_superuser:
            nation = Nation.objects.get(url=url)
            Airplane.objects.filter(nation=nation).delete()
            nation.delete()
        return redirect("the-main-page")


class CreateCategory(View):
    # class for creating categories in nav-bar module

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, "planes/add_category.html", create_context())

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            Category.objects.create(
                name=request.POST['category_name'],
            )
        return redirect('the-main-page')


class DeleteCategory(View):
    # class for deleting category in nav-bar module

    def get(self, request, url):
        if request.user.is_authenticated and request.user.is_superuser:
            Category.objects.get(url=url).delete()
        return redirect("the-main-page")


class CreateNews(View):
    # class for creating news in news-section

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, "planes/add_news.html", create_context())

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            NewsModel.objects.create(
                title=request.POST['title'],
                text=request.POST['text'],
            )
            return redirect('news')


class DeleteNews(View):
    # class for deleting news in nav-bar module or news-section

    def get(self, request, id):
        if request.user.is_authenticated and request.user.is_superuser:
            NewsModel.objects.get(id=id).delete()
        return redirect("news")


def create_context():
    # collection function for all plane information (without prefetch to comments)

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
    return context


def plane_info_context(url):
    context = dict()
    comment_query = Comment.objects.annotate(count_likes=Count("users_likes")).select_related("author")
    comments = Prefetch("comments", comment_query)
    plane = Airplane.objects.select_related("nation", "category").prefetch_related(comments).get(url=url)
    context["plane"] = plane
    nation = Nation.objects.all()
    context["nation"] = nation
    category = Category.objects.all()
    context['category'] = category
    return context
