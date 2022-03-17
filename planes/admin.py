from django.contrib import admin
from .models import Category, Airplane, Comment, Nation, NewsModel

admin.site.register(Category)
admin.site.register(Nation)
admin.site.register(NewsModel)


class CommentAdmin(admin.StackedInline):
    extra = 1
    model = Comment
    readonly_fields = ['likes', 'author']


class AirPlaneAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin]
    readonly_fields = ['likes', 'tag']
    prepopulated_fields = {"url": ("model",)}


admin.site.register(Airplane, AirPlaneAdmin)
