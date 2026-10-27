from django import forms
from .models import RegisteredUser


class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label="Повторите",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = RegisteredUser
        fields = ["name", "email", "password"]
        widgets = {"password": forms.PasswordInput()}

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            self.add_error("password_confirm", "Пароли не совпадают")
        return cleaned_data