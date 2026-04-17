from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Post, TicketType

# User (your existing)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user   # auto admin
        obj.save()

admin.site.register(Post, PostAdmin)


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_editable = ('price', 'is_active')
