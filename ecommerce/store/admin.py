from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Shop, Category, Product, Order, Cart, CartDetail, OrderDetail

admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartDetail)
admin.site.register(OrderDetail)

from django.contrib import admin


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     pass

# class ShopAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description', 'address', 'phone', 'delivery', 'email')
#     search_fields = ('name', 'phone', 'email')
#
#
# admin.site.register(Shop, ShopAdmin)


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'username', 'phone', 'address', 'profile_pic')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'DOB')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(get_user_model(), CustomUserAdmin)

# Register your models here.
