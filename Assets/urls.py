from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import (
    dashboard_view, adminclick_view, staffclick_view, adminsignup_view,
    staffsignup_view, afterlogin_view, addasset_view, viewasset_view,
    issueasset_view, viewissuedasset, viewstaff_view,
    viewissuedassetbystaff, aboutus_view, custom_logout_view, edit_staff_view, edit_asset_view, edit_issued_asset_view,
    delete_issued_asset_view, delete_staff_view, dashboard_view
)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'assets'

urlpatterns = [
    path('', dashboard_view, name='dashboard'),

    # User Role Selection
    path('adminclick', adminclick_view, name='adminclick'),
    path('staffclick', staffclick_view, name='staffclick'),

    # Authentication
    path('adminsignup', adminsignup_view, name='adminsignup'),
    path('staffsignup', staffsignup_view, name='staffsignup'),
    path('adminlogin', LoginView.as_view(template_name='assets/adminlogin.html'), name='adminlogin'),
    path('stafflogin', LoginView.as_view(template_name='assets/stafflogin.html'), name='stafflogin'),
    path('logout', custom_logout_view, name='logout'),
    path('afterlogin', afterlogin_view, name='afterlogin'),

    # Asset Management
    path('viewasset/', viewasset_view, name='viewasset'),
    path('addasset/', addasset_view, name='addasset'),
    path('issueasset', issueasset_view, name='issueasset'),
    path('viewissuedasset', viewissuedasset, name='viewissuedasset'),
    path('viewstaff', viewstaff_view, name='viewstaff'),
    path('viewissuedassetbystaff', viewissuedassetbystaff, name='viewissuedassetbystaff'),
    path('edit_staff/<int:id>/', edit_staff_view, name='edit_staff' ),
    path('delete_staff/<int:id>/', delete_staff_view, name='delete_staff'),
    path('edit_asset/<int:id>/, edit_asset_view/', edit_asset_view, name='edit_asset'),
    path('edit_issued_asset/<int:id>/', edit_issued_asset_view, name='edit_issued_asset'),
    path('delete_issued_asset/<int:id>/', delete_issued_asset_view, name='delete_issued_asset')
,
    # Static Pages
    path('aboutus', aboutus_view, name='aboutus'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
