from django.contrib import admin
from .models import NewUsers
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class UserAdminConfig(UserAdmin):
    model = NewUsers
    search_fields = ('user_name','phone_number')
    ordering = ['-start_date']
    list_display = [
        'user_name','phone_number','is_active','is_staff','start_date'
    ]
    fieldsets = (
        (None,{'fields':('user_name','phone_number')}),
        ('Permissions',{'fields':('is_staff','is_active')}),
        ('Personal',{'fields':('about',)}),
        ('Started_Date',{'fields':('start_date',)}),
    )

    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('phone_number','user_name','password1','password2')}
            ),
    )
    def save_form(self, request, form, change):
        if not change:
            form = self.model.objects.create_user(
                form.cleaned_data['phone_number'],
                form.cleaned_data['password1'],
                form.cleaned_data['user_name'],
            )
        return super().save_form(request, form, change)
admin.site.register(NewUsers,UserAdminConfig)

""""""


 