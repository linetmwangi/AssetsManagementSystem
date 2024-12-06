from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from .models import StaffExtra, Asset
from .forms import AssetForm


# Helper function to check if the user is an admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

# Home view
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'assets/index.html')

# For showing signup/login button for staff
def staffclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'assets/staffclick.html')

# For showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'assets/adminclick.html')

# Admin signup view
def adminsignup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request, 'assets/adminsignup.html', {'form': form})

# Staff signup view
def staffsignup_view(request):
    form1 = forms.StaffUserForm()
    form2 = forms.StaffExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StaffUserForm(request.POST)
        form2 = forms.StaffExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()

            my_staff_group = Group.objects.get_or_create(name='STAFF')
            my_staff_group[0].user_set.add(user)

        return HttpResponseRedirect('stafflogin')
    return render(request, 'assets/staffsignup.html', context=mydict)

# After login view, redirect to the appropriate dashboard
def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'assets/adminafterlogin.html')
    else:
        return render(request, 'assets/staffafterlogin.html')

def custom_logout_view(request):
    logout(request)
    return HttpResponseRedirect('home')

# Add asset for admin
@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def addasset_view(request):
    form = forms.AssetForm()
    if request.method == 'POST':
        form = forms.AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'assets/viewasset.html')
    return render(request, 'assets/addasset.html', {'form': form})

# View all assets for admin
@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def viewasset_view(request):
    assets = models.Asset.objects.all()
    return render(request, 'assets/viewasset.html', {'assets': assets})

# Issue asset to a staff member
@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def issueasset_view(request):
    form = forms.IssuedAssetForm()
    if request.method == 'POST':
        form = forms.IssuedAssetForm(request.POST)
        if form.is_valid():
            obj = models.IssuedAsset()
            obj.enrollment = request.POST.get('enrollment2')
            obj.asset_identifier = request.POST.get('asset_identifier2')
            obj.save()
            return render(request, 'assets/assetissued.html')
    return render(request, 'assets/issueasset.html', {'form': form})

# View all issued assets for admin
@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def viewissuedasset_view(request):
    issuedassets = models.IssuedAsset.objects.all()
    li = []
    for ia in issuedassets:
        issdate = str(ia.issuedate.day) + '-' + str(ia.issuedate.month) + '-' + str(ia.issuedate.year)
        assets = list(models.Asset.objects.filter(identifier=ia.asset_identifier))
        staff = list(models.StaffExtra.objects.filter(enrollment=ia.enrollment))
        i = 0
        for l in assets:
            t = (staff[i].get_name, staff[i].enrollment, assets[i].name, assets[i].category, issdate)
            i += 1
            li.append(t)

    return render(request, 'assets/viewissuedasset.html', {'li': li})

# View all staff members
@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def viewstaff_view(request):
    staff = models.StaffExtra.objects.all()
    return render(request, 'assets/viewstaff.html', {'staff': staff})

# View issued assets by staff
@login_required(login_url='Assets:stafflogin')  # Assuming staff uses 'stafflogin' for login
def viewissuedassetbystaff(request):
    staff = models.StaffExtra.objects.filter(user_id=request.user.id).first()
    issuedassets = models.IssuedAsset.objects.filter(enrollment=staff.enrollment)

    li1 = []
    li2 = []

    for ia in issuedassets:
        assets = models.Asset.objects.filter(identifier=ia.asset_identifier)
        for asset in assets:
            t = (request.user, staff.enrollment, asset.name, asset.category)
            li1.append(t)

        issdate = str(ia.issuedate.day) + '-' + str(ia.issuedate.month) + '-' + str(ia.issuedate.year)
        t2 = (issdate)
        li2.append(t2)

    return render(request, 'assets/viewissuedassetbystaff.html', {'li1': li1, 'li2': li2})

# About us view
def aboutus_view(request):
    return render(request, 'assets/aboutus.html')

# Contact us view
def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            return render(request, 'assets/contactussuccess.html')
    return render(request, 'assets/contactus.html', {'form': sub})

def edit_staff_view(request, id):
    staff = get_object_or_404(StaffExtra, id=id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return render(request, 'assets/viewstaff.html')
    else:
        form = AssetForm(instance=staff)
    return render(request, 'assets/edit_staff.html', {'form': form})


def delete_staff_view(request, id):
    staff = get_object_or_404(StaffExtra, id=id)
    staff.delete()
    return render(request, 'assets/viewstaff.html')


def edit_asset_view(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return render(request, 'assets/viewasset.html')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'assets/edit_asset.html', {'form': form})

def delete_asset_view(request, id):
    asset = get_object_or_404(Asset, id=id)
    asset.delete()
    return render(request, 'assets/viewasset.html')




