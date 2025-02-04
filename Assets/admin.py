from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Asset, StaffExtra, IssuedAsset, CarouselImage

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    extra_fields = ('is_staff',)
    existing_fields = [field[0] for field in UserAdmin.fieldsets]

    if 'Permissions' not in existing_fields:
        fieldsets = UserAdmin.fieldsets + (('Permissions', {'fields': extra_fields}),)

@admin.register(StaffExtra)
class StaffExtraAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment', 'department')
    search_fields = ('user__username', 'enrollment', 'department')
    list_filter = ('department',)

    def save_model(self, request, obj, form, change):
        """Ensure that the related user is marked as staff when a StaffExtra entry is saved."""
        obj.user.is_staff = True
        obj.user.save()
        super().save_model(request, obj, form, change)

@admin.register(IssuedAsset)
class IssuedAssetAdmin(admin.ModelAdmin):
    pass

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    pass


class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

admin.site.register(CarouselImage, CarouselImageAdmin)