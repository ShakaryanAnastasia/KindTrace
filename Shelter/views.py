from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import UpdateView

from Shelter.forms import SignUpForm
from Shelter.models import Profile


def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    error = ' '
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.phoneNum = form.cleaned_data.get('phoneNum')
            user.profile.sex = form.cleaned_data.get('sex')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            error = 'Проверьте пароли на соответствие требованиям и друг другу'
    form = SignUpForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'signup.html', data)

class PersonUpdateView(UpdateView):
    model = Profile
    form_class = SignUpForm
    template_name = 'person_update_form.html'


