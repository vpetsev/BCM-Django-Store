from django import forms
from .models import Purchase, ProductCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'quantity']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class PurchaseReportFilterForm(forms.Form):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    category_id = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(), required=False
    )

    def clean(self):
        data = super().clean()
        start, end = data.get('start_date'), data.get('end_date')
        if start and end and start > end:
            raise forms.ValidationError('Start date must not be after end date.')
        return data
