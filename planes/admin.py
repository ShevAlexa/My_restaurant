from django.contrib import admin
from .models import Category, Airplane, Comment, Nation

admin.site.register(Category)
admin.site.register(Nation)


class CommentAdmin(admin.StackedInline):
    extra = 1
    model = Comment


class AirPlaneAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin]
    readonly_fields = ['likes', 'tag']
    prepopulated_fields = {"url": ("model",)}


admin.site.register(Airplane, AirPlaneAdmin)
