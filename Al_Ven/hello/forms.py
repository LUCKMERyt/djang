from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import Review, ProductInquiry


class UserForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=150, widget=forms.TextInput(attrs={
        "autocomplete": "off",
    }))
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={
        "autocomplete": "off",
    }))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        "autocomplete": "new-password",
    }))
    password_confirm = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={
        "autocomplete": "new-password",
    }))

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
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        "autocomplete": "off",
    }))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        "autocomplete": "new-password",
    }))

    def clean(self):
        username = self.data.get(self.add_prefix("username"), "").strip().lower()
        if username:
            self.data = self.data.copy()
            self.data[self.add_prefix("username")] = username
        return super().clean()


class AccountNameForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "autocomplete": "name",
            "placeholder": "Введите ваше имя",
        }),
    )


class AccountUsernameForm(forms.Form):
    username = forms.EmailField(
        label="Логин (электронная почта)",
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            "autocomplete": "username",
            "placeholder": "Введите электронную почту",
        }),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"].strip().lower()
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=username).exclude(pk=self.user.pk).exists():
            raise ValidationError("Аккаунт с такой электронной почтой уже существует.")
        return username


class AccountPasswordForm(PasswordChangeForm):
    """Secure password change form with Django's password validation."""

    old_password = forms.CharField(
        label="Текущий пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    new_password2 = forms.CharField(
        label="Повторите новый пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'text']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Как вас зовут?',
                'class': 'review-input',
                'autocomplete': 'off',
            }),
            'rating': forms.Select(attrs={
                'class': 'review-input'
            }),
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Расскажите о вашем опыте...',
                'class': 'review-input',
                'autocomplete': 'off',
            }),
        }
        labels = {
            'name': 'Ваше имя',
            'rating': 'Оценка',
            'text': 'Ваш отзыв',
        }


class ProductInquiryForm(forms.ModelForm):
    """Заявка на товар/цену для B2B («напишите свои условия, пришлите ссылку на изделие»)."""

    class Meta:
        model = ProductInquiry
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'Ваше имя',
            'email': 'Email',
            'message': 'Сообщение (что и в какой цене нужно?)',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Как вас зовут?',
                'class': 'inquiry-input',
                'autocomplete': 'off',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Почта для связи',
                'class': 'inquiry-input',
                'autocomplete': 'off',
            }),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Какой товар или ссылка на изделие? В какой цене нужно? Сроки и объёмы...',
                'class': 'inquiry-input',
                'autocomplete': 'off',
            }),
        }
