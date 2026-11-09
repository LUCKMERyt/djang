from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Review


class UserForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=150)
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise ValidationError("Аккаунт с таким email уже существует.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmation = cleaned_data.get("password_confirm")
        if password and confirmation and password != confirmation:
            self.add_error("password_confirm", "Пароли не совпадают")
        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                self.add_error("password", error)
        return cleaned_data


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    def clean(self):
        username = self.data.get(self.add_prefix("username"), "").strip().lower()
        if username:
            self.data = self.data.copy()
            self.data[self.add_prefix("username")] = username
        return super().clean()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'text']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Как вас зовут?',
                'class': 'review-input'
            }),
            'rating': forms.Select(attrs={
                'class': 'review-input'
            }),
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Расскажите о вашем опыте...',
                'class': 'review-input'
            }),
        }
        labels = {
            'name': 'Ваше имя',
            'rating': 'Оценка',
            'text': 'Ваш отзыв',
        }
