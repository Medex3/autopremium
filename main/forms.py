from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
#from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации нового пользователя"""
    email = forms.EmailField(required=True, label="Электронная почта")
    phone = forms.CharField(max_length=20, required=False, label="Телефон")
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'first_name', 'last_name',
                  'password1', 'password2', 'role')
        widgets = {
            'role': forms.HiddenInput(),  # Роль по умолчанию - клиент
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].initial = 'client'
        self.fields['role'].widget = forms.HiddenInput()


class CustomUserChangeForm(UserChangeForm):
    """Форма редактирования пользователя"""

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'first_name', 'last_name',
                  'avatar', 'birth_date', 'address', 'driver_license',
                  'preferred_brands')


class LoginForm(forms.Form):
    """Форма входа"""
    username = forms.CharField(label="Имя пользователя или Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            # Пробуем аутентифицировать по username
            user = authenticate(username=username, password=password)
            if user is None:
                # Пробуем по email
                try:
                    user = CustomUser.objects.get(email=username)
                    user = authenticate(username=user.username, password=password)
                except CustomUser.DoesNotExist:
                    user = None

            if user is None:
                raise forms.ValidationError("Неверное имя пользователя или пароль")
            if not user.is_active:
                raise forms.ValidationError("Аккаунт отключен")

            cleaned_data['user'] = user

        return cleaned_data


class ProfileForm(forms.ModelForm):
    """Форма редактирования профиля"""

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'address', 'birth_date', 'avatar',
                  'driver_license', 'preferred_brands']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }