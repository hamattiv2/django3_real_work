from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from mysite.models import User, Profile, Prefecture
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    # 削除用チェックボックスが表示されるかどうか。Trueなら表示される
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (None, {
            'fields': ('is_admin', 'is_active')
        })
    )

    list_display = ('email', 'password')
    list_filter = ()
    ordering = ()
    filter_horizontal = ()

admin.site.unregister(Group) # admin画面に表示しない
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Prefecture)