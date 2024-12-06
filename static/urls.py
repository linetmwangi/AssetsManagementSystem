from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import (
    home_view, adminclick_view, staffclick_view, adminsignup_view,
    staffsignup_view, afterlogin_view, addasset_view, viewasset_view,
    issueasset_view, viewissuedasset_view, viewstaff_view,
    viewissuedassetbystaff, aboutus_view, contactus_view, custom_logout_view, edit_staff_view, edit_asset_view,
)

urlpatterns = [
    # Home Page
    path('home', home_view, name='home'),

    # User Role Selection
    path('adminclick', adminclick_view, name='adminclick'),
    path('staffclick', staffclick_view, name='staffclick'),

    # Authentication
    path('adminsignup', adminsignup_view, name='adminsignup'),
    path('', staffsignup_view, name='staffsignup'),
    path('adminlogin', LoginView.as_view(template_name='assets/adminlogin.html'), name='adminlogin'),
    path('stafflogin', LoginView.as_view(template_name='assets/stafflogin.html'), name='stafflogin'),
    path('logout', custom_logout_view, name='logout'),
    path('afterlogin', afterlogin_view, name='afterlogin'),

    # Asset Management
    path('addasset', addasset_view, name='addasset'),
    path('viewasset', viewasset_view, name='viewasset'),
    path('issueasset', issueasset_view, name='issueasset'),
    path('viewissuedasset', viewissuedasset_view, name='viewissuedasset'),
    path('viewstaff', viewstaff_view, name='viewstaff'),
    path('viewissuedassetbystaff', viewissuedassetbystaff, name='viewissuedassetbystaff'),
    path('edit_staff/<int:id>/', edit_staff_view, name='edit_staff' ),
    path('edit_asset/<int:id>/, edit_asset_view/', edit_asset_view, name='edit_asset')

,
    # Static Pages
    path('aboutus', aboutus_view, name='aboutus'),
    path('contactus', contactus_view, name='contactus'),
]
