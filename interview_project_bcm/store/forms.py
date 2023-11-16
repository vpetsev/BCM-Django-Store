from django import forms
from .models import Purchase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'quantity']


class CustomUserCreationForm(UserCreationForm):
    is_escalated = forms.BooleanField(required=False, help_text='Check to make the user escalated.')

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "is_escalated"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['is_escalated']:
            # Set escalated privileges here, e.g., make user staff or superuser
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
        return user