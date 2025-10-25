from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm,UserCreationForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin) :

    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser

    list_display = ('mobile_number','first_name','last_name','is_active','is_staff','is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active','groups')
    search_fields = ('mobile_number','first_name','last_name')
    ordering = ('-register_date',)


    fieldsets = (
        (None,{'fields':('mobile_number','password')}),
        ('Personal Info',{'fields':('first_name','last_name','email','gender')}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'register_date')}),
    )

    add_fieldsets = (
        (None,{'fields':('mobile_number','first_name','last_name','password_1','password_2')}),     
    )

    filter_horizontal =  (
        "groups",
        "user_permissions",
        )
    
    readonly_fields = ('last_login', 'register_date',)
    # -------------------------------------------------------------------
    staff_fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups')}), 
        ('Important dates', {'fields': ('last_login', 'register_date')}),
    )

    def get_queryset(self, request):
        qs =  super().get_queryset(request)
        if request.user.is_superuser :
            return qs
        return  qs.filter(is_superuser=False)
    # -------------------
    def get_fieldsets(self, request, obj = None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        return self.staff_fieldsets
    # -------------------
    def has_change_permission(self, request, obj = None):
        if obj is None :
            return True
        if request.user.is_superuser:
            return True
        return not obj.is_superuser
    # -------------------
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return not obj.is_superuser

admin.site.register(CustomUser,CustomUserAdmin)
# ---------------------------------------------------------------------------------------