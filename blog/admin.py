from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import *

class UsersAdmin(UserAdmin):
    pass

    fieldsets = (
        (None, {'fields': ('username', 'password', 'avatar')}),
        (_('Personal info'), {'fields': ('email', 'qq', 'mobile' )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    #list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', )
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

class ArticleAdmin(admin.ModelAdmin):

    list_display = ('title', 'user', 'category', 'get_tags', 'date_publish')

    class Media:
            js = (
                '/static/js/kindeditor-4.1.10/kindeditor-min.js',
                '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
                '/static/js/kindeditor-4.1.10/config.js',
            )

admin.site.register(User, UsersAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)