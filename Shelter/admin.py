from django.contrib import admin
from django.contrib import admin

from .models import OwnerApplication, Files, Shelter, Pet, Comment
from .models import Profile

admin.site.register(OwnerApplication)
admin.site.register(Profile)
admin.site.register(Files)
admin.site.register(Shelter)
admin.site.register(Pet)
admin.site.register(Comment)