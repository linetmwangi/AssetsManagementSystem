from django.contrib import admin
from .models import Asset, StaffExtra, IssuedAsset

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
