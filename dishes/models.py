from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField('Категория', max_length=50)
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Dish(models.Model):
    name = models.CharField("Имя", max_length=100)
    composition = models.CharField("Состав", max_length=200)
    recipe = models.TextField("Рецепт")
    price = models.CharField("Цена", max_length=10, default=0, help_text="указать цену в долларах")
    image = models.ImageField("Изображение", upload_to='dishes/')
    cuisine = models.CharField("Кухня", max_length=50)
    url = models.SlugField(max_length=150, unique=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class Comment(models.Model):
    text = models.TextField("Комментарий")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария", default=User)
    like1 = models.ManyToManyField(User, through="LikeCommentUser", related_name="liked_comment")
    date = models.DateTimeField(auto_now_add=True, null=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="comments", blank=True)


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
