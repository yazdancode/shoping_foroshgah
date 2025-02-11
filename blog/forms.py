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
                regex=r"^[\u0600-\u06FFa-zA-Z\s]+$",
                message="نام باید فقط شامل حروف فارسی یا انگلیسی باشد.",
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
                regex=r"^[\u0600-\u06FFa-zA-Z\s]+$",
                message="نام خانوادگی باید فقط شامل حروف فارسی یا انگلیسی باشد.",
            )
        ],
    )

    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        required=True,
        label="سن",
        error_messages={
            "min_value": "سن نمی‌تواند کمتر از 1 باشد.",
            "max_value": "سن نمی‌تواند بیشتر از 120 باشد.",
        },
    )

    phone = forms.CharField(
        max_length=11,
        required=True,
        label="تلفن",
        validators=[
            RegexValidator(
                regex=r"^09\d{9}$",
                message="شماره تلفن باید ۱۱ رقم باشد و با 09 شروع شود.",
            )
        ],
        widget=forms.TextInput(attrs={"placeholder": "مثلاً: 09123456789"}),
    )

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name and len(first_name) < 5:
            raise forms.ValidationError("نام باید حداقل ۵ حرف داشته باشد.")
        return first_name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن فقط باید شامل اعداد باشد.")
            if len(phone) != 11:
                raise forms.ValidationError("شماره تلفن باید دقیقاً ۱۱ رقم باشد.")
            if not phone.startswith("09"):
                raise forms.ValidationError("شماره تلفن باید با 09 شروع شود.")
        return phone


class ShareForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "پیام خود را وارد کنید...", "rows": 5, "cols": 40}
        ),
        required=True,
        label="پیام",
    )

    full_name = forms.CharField(
        max_length=25,
        required=True,
        label="نام",
        widget=forms.TextInput(attrs={"placeholder": "نام خود را وارد کنید"}),
    )

    to = forms.EmailField(
        required=True,
        label="ایمیل",
        widget=forms.EmailInput(attrs={"placeholder": "ایمیل خود را وارد کنید"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get("full_name")
        subject = cleaned_data.get("subject")

        if full_name and len(full_name) < 3:
            self.add_error("full_name", "نام باید حداقل ۳ کاراکتر باشد.")

        if subject and len(subject) < 5:
            self.add_error("subject", "موضوع باید حداقل ۵ کاراکتر باشد.")

        return cleaned_data
