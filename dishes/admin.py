from django.contrib import admin
from .models import Category, Dish, Comment

admin.site.register(Category)


class CommentAdmin(admin.StackedInline):
    extra = 1
    model = Comment


class DishAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin]


admin.site.register(Dish, DishAdmin)
