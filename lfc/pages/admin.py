from django.contrib import admin
from .models import UserProfile, Messages, Friends


admin.site.register(UserProfile)
admin.site.register(Messages)
admin.site.register(Friends)