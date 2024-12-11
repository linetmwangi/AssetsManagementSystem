from django.contrib.auth import logout
from django.shortcuts import render
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from .models import StaffExtra, Asset , IssuedAsset, CarouselImage
from .forms import AssetForm, IssuedAssetForm, StaffExtraForm , CarouselImageForm


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

# Home view
def dashboard_view(request):
    if request.user.is_authenticated:
        return redirect('Assets:afterlogin')

    images = CarouselImage.objects.all()

    form = None
    if request.method == 'POST' and request.user.is_admin:
        form = CarouselImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Assets:dashboard')
    else:
        form = CarouselImageForm()

    return render(request, 'Assets/dashboard.html', {
        'images': images,
        'form': form if request.user.is_staff else None,
    })
# For showing signup/login button for staff
def staffclick_view(request):
    if request.user.is_authenticated:
        return redirect('Assets:afterlogin')
    return render(request, 'Assets/staffclick.html')

# For showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return redirect('Assets:afterlogin')
    return render(request, 'Assets/adminclick.html')

# Admin signup view
def adminsignup_view(request):
    form = forms.AdminSignupForm()
    if request.method == 'POST':
        form = forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return redirect('Assets:adminlogin')
    return render(request, 'Assets/adminsignup.html', {'form': form})

# Staff signup view
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from . import forms


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

            if not f2.username:
                f2.username = "default_username"
            f2.save()

            my_staff_group = Group.objects.get_or_create(name='STAFF')
            my_staff_group[0].user_set.add(user)

            return redirect('Assets:stafflogin')

    return render(request, 'Assets/staffsignup.html', context=mydict)


# After login view, redirect to the appropriate dashboard
def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'Assets/adminafterlogin.html')
    else:
        return render(request, 'Assets/staffafterlogin.html')

def custom_logout_view(request):
    logout(request)
    return redirect('Assets:dashboard')

# Add asset for admin
@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def addasset_view(request):
    form = forms.AssetForm()
    if request.method == 'POST':
        form = forms.AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Assets:viewasset')
    return render(request, 'Assets/addasset.html', {'form': form})

# View all assets for admin
@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def viewasset_view(request):
    assets = models.Asset.objects.all()
    return render(request, 'Assets/viewasset.html', {'assets': assets})

# Issue asset to a staff member
@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def issueasset_view(request):
    form = IssuedAssetForm()
    if request.method == 'POST':
        form = IssuedAssetForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('Assets:viewissuedasset')
    return render(request, 'Assets/issueasset.html', {'form': form})

@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def viewissuedasset(request):
    issued_assets = IssuedAsset.objects.all()
    form = IssuedAssetForm(request.GET)

    if form.is_valid():
        if form.cleaned_data['enrollment']:
            issued_assets = issued_assets.filter(enrollment=form.cleaned_data['enrollment'])
        if form.cleaned_data['asset_identifier']:
            issued_assets = issued_assets.filter(identifier=form.cleaned_data['identifier'])

    return render(request, 'Assets/viewissuedasset.html', { 'issued_assets': issued_assets})


# View all staff members
@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def viewstaff_view(request):
    staff = models.StaffExtra.objects.all()
    return render(request, 'Assets/viewstaff.html', {'staff': staff})

# View issued assets by staff
@login_required(login_url='Assets:stafflogin')
def viewissuedassetbystaff(request):
    staff = models.StaffExtra.objects.filter(user_id=request.user.id).first()

    return render(request, 'Assets/viewissuedassetbystaff.html', {'staff':staff})

# About us view
def aboutus_view(request):
    return render(request, 'assets/aboutus.html')


def edit_staff_view(request, id):
    staff = get_object_or_404(StaffExtra, id=id)
    if request.method == 'POST':
        form = StaffExtraForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('Assets:viewstaff')
    else:
        form = StaffExtraForm(instance=staff)

    return render(request, 'Assets/edit_staff.html', {'form': form})


def delete_staff_view(request, id):
    staff = get_object_or_404(StaffExtra, id=id)

    if request.method == 'POST':
        staff.delete()
        return redirect('Assets:viewstaff')

    return render(request, 'Assets/confirmdeletestaff.html', {'staff': staff})

def edit_asset_view(request, id):

    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('Assets:viewasset')  # Redirect after saving
    else:
        form = AssetForm(instance=asset)

    return render(request, 'Assets/edit_asset.html', {'form': form})


def edit_issued_asset_view(request, id):
    asset = get_object_or_404(IssuedAsset, id=id)

    if request.method == 'POST':
        form = IssuedAssetForm(request.POST, instance=asset)

        if form.is_valid():
            form.save()
            return redirect('Assets:viewissuedasset')

    else:
        form = IssuedAssetForm(instance=asset)

    return render(request, 'Assets/editissuedasset.html', {'form': form, 'asset': asset})


def delete_issued_asset_view(request, id):
    asset = get_object_or_404(IssuedAsset, id=id)

    if request.method == 'POST':
        asset.delete()
        return redirect('Assets:viewissuedasset')

    return render(request, 'Assets/confirmdeleteissuedasset.html', {'asset': asset})

