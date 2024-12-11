from django.contrib import admin
from .models import Asset, StaffExtra, IssuedAsset, CarouselImage

# Register your models here.
class AssetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Asset, AssetAdmin)

class StaffExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StaffExtra, StaffExtraAdmin)

class IssuedAssetAdmin(admin.ModelAdmin):
    pass
admin.site.register(IssuedAsset, IssuedAssetAdmin)

class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'created_at')  # Fields to display in the admin list view
    search_fields = ('title', 'description')  # Add a search bar for these fields
    list_filter = ('created_at',)  # Add filtering options


admin.site.register(CarouselImage, CarouselImageAdmin)