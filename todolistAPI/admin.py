from django.contrib import admin
from .models import TodoItem, UserProfile


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    search_fields = ('user__username',)


admin.site.register(TodoItem)
admin.site.register(UserProfile, UserProfileAdmin)
