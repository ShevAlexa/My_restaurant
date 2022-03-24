from django.contrib import admin
from .models import Category, Airplane, Comment, Nation, NewsModel

admin.site.register(NewsModel)


class CommentAdmin(admin.StackedInline):
    extra = 1
    model = Comment
    readonly_fields = ['likes', 'author']


class AirPlaneAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin]
    readonly_fields = ['likes', 'tag']
    prepopulated_fields = {"url": ("model",)}


class NationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("country",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("name",)}


admin.site.register(Airplane, AirPlaneAdmin,)
admin.site.register(Nation, NationAdmin)
admin.site.register(Category, CategoryAdmin)
