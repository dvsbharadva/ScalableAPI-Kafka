from django.contrib import admin
from .models import Likes
# Register your models here.
class LikeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Likes, LikeAdmin)