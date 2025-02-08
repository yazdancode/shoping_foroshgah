from django import forms
from django.core.validators import RegexValidator


class AccountForm(forms.Form):
    GENDER_CHOICES = [
        ("M", "مرد"),
        ("F", "زن"),
    ]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect, required=True, label="جنسیت"
    )
    address = forms.CharField(
        max_length=255,
        widget=forms.Textarea,
        required=True,
        label="آدرس",
        help_text="لطفاً آدرس خود را وارد کنید.",
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput,
        required=True,
        label="نام",
        validators=[
            RegexValidator(
                regex="^[\u0600-\u06ffa-zA-Z\s]+$", message="نام باید حروف باشد."
            )
        ],
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput,
        required=True,
        label="نام خانوادگی",
        validators=[
            RegexValidator(
                regex="^[\u0600-\u06ffa-zA-Z\s]+$",
                message="نام خانوادگی باید حروف باشد.",
            )
        ],
    )
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput,
        required=True,
        label="ایمیل",
        help_text="لطفا ایمیل خود را وارد کنید.",
    )
