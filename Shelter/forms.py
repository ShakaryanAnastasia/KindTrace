from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from Shelter.models import OwnerApplication, Pet, Comment, News, Task


class SignUpForm(UserCreationForm):
    username = forms.EmailField(max_length=30, label='Электронная почта')
    first_name = forms.CharField(max_length=100, label='Имя')
    last_name = forms.CharField(max_length=100, label='Фамилия')
    phoneNum = forms.CharField(max_length=12, label='Номер телефона')
    SEX_CHOICES = (
        ('male', "мужской"),
        ('female', "женский"),
    )
    sex = forms.ChoiceField(label='Пол', choices=SEX_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phoneNum', 'sex',
                  'password1', 'password2',)

    widgets = {
        'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        'phoneNum': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PhoneNum'}),
        'sex': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sex'}),
        'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    }


class ApplicationOwnerForm(ModelForm):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, label='Файлы')

    class Meta:
        model = OwnerApplication
        fields = ['name', 'surname', 'email', 'phoneNum', 'sex']


class PetForm(ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False,
                              label='Изображения')

    class Meta:
        model = Pet
        fields = ['name', 'age', 'sex', 'type', 'color', 'wool', 'character', 'description']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'body']

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-comment'}),

        }


class NewsForm(ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False,
                              label='Изображения')

    class Meta:
        model = News
        fields = ['title', 'body', 'anons']


class TaskForm(ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False,
                              label='Изображения')

    class Meta:
        model = Task
        fields = ['title', 'body']


class DateForm(forms.Form):
    dateExpiration = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        }), label='Дата выполнения'
    )
