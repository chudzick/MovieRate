from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nazwa użytkownika',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'password1': 'Hasło',
            'password2': 'Potwierdzenie hasła'
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = f'Pole {field.label} jest wymagane'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input'
