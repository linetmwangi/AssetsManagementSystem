from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render
from . import forms, models
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from .models import StaffExtra, Asset , IssuedAsset, CarouselImage
from .forms import AssetForm, IssuedAssetForm, StaffExtraForm , CarouselImageForm , StaffUserForm
from django.utils.timezone import now

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists() or user.is_staff

# Home view
def dashboard_view(request):
    if request.user.is_authenticated:
        return redirect('Assets:afterlogin')

    images = CarouselImage.objects.all()

    form = None
    if request.method == 'POST' and is_admin(request.user):  # Use is_admin()
        form = CarouselImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Assets:dashboard')
    else:
        form = CarouselImageForm()

    return render(request, 'Assets/dashboard.html', {
        'images': images,
        'form': form if request.user.is_staff else None,  # Check is_staff properly
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


def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'Assets/adminafterlogin.html', {
            'user': request.user  # Pass the user object to the template
        })
    elif StaffExtra.objects.filter(user=request.user).exists():
        return render(request, 'Assets/staffafterlogin.html', {
            'user': request.user  # Pass the user object to the template
        })
    else:
        return redirect('Assets:dashboard')


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

@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def viewasset_view(request):
    available_assets = Asset.objects.filter(available=True)  # Fetch only available assets
    requested_assets = Asset.objects.filter(available=False, requested_by__isnull=False)

    return render(request, 'Assets/viewasset.html', {
        'available_assets': available_assets,
        'requested_assets': requested_assets,
    })

@login_required(login_url='Assets:stafflogin')
def viewassetbystaff(request):
    assets = Asset.objects.filter(available=True)
    return render(request, 'Assets/viewassetbystaff.html', {'assets': assets})


@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def issue_asset_view(request):
    form = IssuedAssetForm()

    if request.method == 'POST':
        form = IssuedAssetForm(request.POST)
        if form.is_valid():
            issued_asset = form.save(commit=False)

            issued_asset.identifier.available = False
            issued_asset.identifier.save()

            issued_asset.save()
            return redirect('Assets:viewissuedasset')

    return render(request, 'Assets/issue_asset.html', {'form': form})


@login_required(login_url='Assets:adminlogin')
@user_passes_test(is_admin)
def viewissuedasset(request):
    issuedassets = IssuedAsset.objects.all()
    form = IssuedAssetForm(request.GET)

    if form.is_valid():
        if form.cleaned_data.get('enrollment'):
            issuedassets = issuedassets.filter(enrollment=form.cleaned_data['enrollment'])

        if form.cleaned_data.get('asset_identifier'):
            issuedassets = issuedassets.filter(identifier=form.cleaned_data['identifier'])

    return render(request, 'Assets/viewissuedasset.html', {'issuedassets': issuedassets})


@login_required(login_url='Assets:stafflogin')
def viewissuedassetbystaff(request):
    staff_extra = get_object_or_404(StaffExtra, user=request.user)
    issuedassets = IssuedAsset.objects.filter(enrollment=staff_extra)

    print(issuedassets)

    return render(request, 'Assets/viewissuedassetbystaff.html', {
        'issuedassets': issuedassets,
        'staff_extra': staff_extra,
    })


@user_passes_test(is_admin)
def addstaff_view(request):
    if request.method == 'POST':
        user_form = StaffUserForm(request.POST)
        staff_form = StaffExtraForm(request.POST)

        if user_form.is_valid() and staff_form.is_valid():
            # Save the user and staff details
            user = user_form.save(commit=False)
            user.is_staff = True
            user.is_superuser = False
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()

            return redirect('Assets:viewstaff')
    else:
        user_form = StaffUserForm()
        staff_form = StaffExtraForm()

    return render(request, 'Assets/addstaff.html', {
        'user_form': user_form,
        'staff_form': staff_form,
    })

@user_passes_test(is_admin)
def viewstaff_view(request):
    staff = models.StaffExtra.objects.all()
    staff_with_names = [(staff_member, staff_member.get_name()) for staff_member in staff]

    return render(request, 'Assets/viewstaff.html', {'staff_with_names': staff_with_names})

@user_passes_test(is_admin)
def viewstaff_view(request):
    staff = models.StaffExtra.objects.all()
    return render(request, 'Assets/viewstaff.html', {'staff': staff})

def aboutus_view(request):
    return render(request, 'assets/aboutus.html')

@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
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
    issued_asset = get_object_or_404(IssuedAsset, id=id)  # Get issued asset record

    if request.method == 'POST':
        # Retrieve the associated asset and mark it as available again
        asset = issued_asset.identifier
        asset.available = True  # Make asset available
        asset.requested_by = None  # Clear requester
        asset.requested_at = None  # Clear request time
        asset.save()

        issued_asset.delete()  # Delete the issued asset record

        messages.success(request, f'Issued asset "{asset.name}" has been deleted and is now available.')

        return redirect('Assets:viewissuedasset')

    return render(request, 'Assets/confirmdeleteissuedasset.html', {'asset': issued_asset})


@login_required(login_url='Assets:stafflogin')
def request_asset_view(request, id):
    asset = get_object_or_404(Asset, id=id)

    if asset.available:
        asset.available = False
        asset.requested_by = request.user  # Store requester
        asset.requested_at = now()  # Store request time
        asset.save()

        messages.success(request, f'You have successfully requested "{asset.name}".')

    else:
        messages.error(request, f'Asset "{asset.name}" is already requested.')

    return redirect('Assets:viewassetbystaff')