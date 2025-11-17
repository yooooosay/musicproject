from django.contrib import admin
from .models import PlayListName, MusicPost
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
class PhotoPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(PlayListName, CategoryAdmin)

admin.site.register(MusicPost, PhotoPostAdmin)