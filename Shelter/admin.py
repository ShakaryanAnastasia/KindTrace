from django.contrib import admin
from django.contrib import admin

from .models import OwnerApplication, Files, Shelter, Pet, Comment, Image, News, Task, Order
from .models import Profile

admin.site.register(OwnerApplication)
admin.site.register(Profile)
admin.site.register(Files)
admin.site.register(Image)
admin.site.register(Shelter)
admin.site.register(Pet)
admin.site.register(Comment)
admin.site.register(News)
admin.site.register(Task)
admin.site.register(Order)