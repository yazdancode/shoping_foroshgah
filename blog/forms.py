from django import forms

from blog.models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("phone",)
