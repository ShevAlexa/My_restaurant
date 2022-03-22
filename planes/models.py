from django.contrib.auth.models import User, AbstractUser
from django.db import models
from slugify import slugify


class Category(models.Model):
    name = models.CharField('Категория', max_length=50)
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if self.id is None:
            self.url = slugify(self.name)
        try:
            super().save(**kwargs)
        except:
            self.url += str(self.id)
            super().save(**kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Nation(models.Model):
    country = models.CharField("Страна", max_length=30)
    url = models.SlugField(max_length=150, unique=True)
    image = models.ImageField("Изображение", upload_to='planes/', null=True)

    def __str__(self):
        return self.country

    def save(self, **kwargs):
        if self.id is None:
            self.url = slugify(self.country)
        try:
            super().save(**kwargs)
        except:
            self.url += str(self.id)
            super().save(**kwargs)

    class Meta:
        verbose_name = "Нация"
        verbose_name_plural = "Нации"


class Airplane(models.Model):
    model = models.CharField("Модель", max_length=100, db_index=True)
    cruising_speed = models.CharField("Cкорость", max_length=5, null=True)
    constructor = models.CharField("Конструктор", max_length=30, null=True)
    engine_type = models.CharField("Тип двигателя", max_length=50, null=True)
    production_volume = models.PositiveIntegerField("Единиц произведено", default=0)
    reference = models.TextField("Справка")
    image = models.ImageField("Изображение", upload_to='planes/')
    nation = models.ForeignKey(Nation, verbose_name="Нация", on_delete=models.CASCADE)
    url = models.SlugField(max_length=150, unique=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    users_likes = models.ManyToManyField(User, through="LikeAirplaneUser", related_name="liked_airplane")
    likes = models.PositiveIntegerField(default=0)
    users_tags = models.ManyToManyField(User, through="TagAirplaneUser", related_name="taged_plane")
    tag = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.model

    def save(self, **kwargs):
        if self.id is None:
            self.url = slugify(self.model)
        try:
            super().save(**kwargs)
        except:
            self.url += str(self.id)
            super().save(**kwargs)

    class Meta:
        verbose_name = "Самолёт"
        verbose_name_plural = "Самолёты"


class Comment(models.Model):
    text = models.TextField("Комментарий", null=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name="Автор комментария",
                               null=True,
                               blank=True,
                               default=User)
    users_likes = models.ManyToManyField(User, through="LikeCommentUser", related_name="liked_comment")
    likes = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True, null=True)
    model = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)


class LikeCommentUser(models.Model):
    class Meta:
        unique_together = ("user", "comment")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_comment_table")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="liked_user_table")

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            LikeCommentUser.objects.get(user=self.user, comment=self.comment).delete()
            self.comment.likes -= 1
        else:
            self.comment.likes += 1
        finally:
            self.comment.save()


class LikeAirplaneUser(models.Model):
    class Meta:
        unique_together = ("user", "model")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_airplane_table")
    model = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="liked_user_table")

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            LikeAirplaneUser.objects.get(user=self.user, model=self.model).delete()
            self.model.likes -= 1
        else:
            self.model.likes += 1
        finally:
            self.model.save()


class TagAirplaneUser(models.Model):
    class Meta:
        unique_together = ("user", "model")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taged_airplane_table")
    model = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="taged_user_table")

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            TagAirplaneUser.objects.get(user=self.user, model=self.model).delete()
            self.model.tag -= 1
        else:
            self.model.tag += 1
        finally:
            self.model.save()


class NewsModel(models.Model):
    title = models.CharField("Заголовок", max_length=50)
    text = models.TextField("Текст")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


# class Users(AbstractUser):
#     pass
