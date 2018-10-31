from django.contrib import admin
from .models import User, Post, Profile

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'email',
                    )


class PostAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'creator',
                    'text',
                    'no_of_likes'
                    )


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Post, PostAdmin)
