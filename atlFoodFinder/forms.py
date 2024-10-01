from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class CustomPasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")

        # Validate password strength
        try:
            validate_password(password1)
        except ValidationError as e:
            self.add_error('new_password1', e)

        return cleaned_data