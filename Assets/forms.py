from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

class StaffUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

class StaffExtraForm(forms.ModelForm):
    class Meta:
        model = models.StaffExtra
        fields = ['enrollment', 'department']

class AssetForm(forms.ModelForm):
    class Meta:
        model = models.Asset
        fields = ['name', 'identifier', 'description', 'category']

class IssuedAssetForm(forms.Form):
    # to_field_name value will be stored when form is submitted.....__str__ method of Asset model will be shown there in html
    asset_identifier2 = forms.ModelChoiceField(queryset=models.Asset.objects.all(), empty_label="Name and Identifier", to_field_name="identifier", label='Name and Identifier')
    enrollment2 = forms.ModelChoiceField(queryset=models.StaffExtra.objects.all(), empty_label="Name and Enrollment", to_field_name='enrollment', label='Name and Enrollment')