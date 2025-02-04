from django import forms
from django.contrib.auth.models import User
from . import models

class StaffUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class StaffExtraForm(forms.ModelForm):
    class Meta:
        model = models.StaffExtra
        fields = ['enrollment', 'department']  # Removed the user field


class AssetForm(forms.ModelForm):
    class Meta:
        model = models.Asset
        fields = ['name', 'identifier', 'description', 'category', 'condition']


class IssuedAssetForm(forms.ModelForm):
    class Meta:
        model = models.IssuedAsset
        fields = ['enrollment', 'identifier', 'condition']

    identifier = forms.ModelChoiceField(
        queryset=models.Asset.objects.all(),
        empty_label="Name and Identifier",
        to_field_name="identifier",
        label='Name and Identifier'
    )
    enrollment = forms.ModelChoiceField(
        queryset=models.StaffExtra.objects.all(),
        empty_label="Name and Enrollment",
        to_field_name='enrollment',
        label='Name and Enrollment'
    )


class CarouselImageForm(forms.ModelForm):
    class Meta:
        model = models.CarouselImage
        fields = ['title', 'description', 'image']
