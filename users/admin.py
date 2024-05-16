from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone',)
    list_filter = ('email', )
    search_fields = ('username',)
