from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic import UpdateView

from KindHeart import settings
from Shelter.application_owner_view import password_generate
from Shelter.forms import SignUpForm, PasswordChangeForm
from Shelter.models import Profile, Shelter


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


def editprofileowner(request):
    try:
        form = PasswordChangeForm()
        sexes = Profile.SEX_CHOICES
        profile = Profile.objects.get(user=request.user)
        shelter = Shelter.objects.get(user=profile)
        if request.method == "POST":
            profile.first_name = request.POST.get("first_name")
            profile.last_name = request.POST.get("last_name")
            profile.phoneNum = request.POST.get("phoneNum")
            profile.sex = request.POST.get("sex")
            shelter.title = request.POST.get("title")
            shelter.address = request.POST.get("address")
            shelter.description = request.POST.get("description")
            profile.save()
            shelter.save()
            return HttpResponseRedirect("/owner/editprofile")
        else:
            return render(request, "owner_profile.html",
                          {"profile": profile, "shelter": shelter, "sexes": sexes, 'form': form})
    except Profile.DoesNotExist:
        return HttpResponseNotFound("<h2>Profile not found</h2>")


def editprofileclient(request):
    try:
        form = PasswordChangeForm()
        sexes = Profile.SEX_CHOICES
        profile = Profile.objects.get(user=request.user)
        if request.method == "POST":
            profile.first_name = request.POST.get("first_name")
            profile.last_name = request.POST.get("last_name")
            profile.phoneNum = request.POST.get("phoneNum")
            profile.sex = request.POST.get("sex")
            profile.save()
            return HttpResponseRedirect("/client/editprofile")
        else:
            return render(request, "client_profile.html",
                          {"profile": profile, "sexes": sexes, 'form': form})
    except Profile.DoesNotExist:
        return HttpResponseNotFound("<h2>Profile not found</h2>")


def changepassword(request):
    profile = Profile.objects.get(user=request.user)
    error = ' '
    form = PasswordChangeForm(request.POST)
    if request.method == "POST" and form.is_valid():
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        if len(password1) and len(password2) >= 8:
            if password1 == password2:
                user = request.user
                user.set_password(password1)
                user.save()
                user = authenticate(username=user.username, password=password1)
                login(request, user)
                if profile.type == 'Moderator':
                    return HttpResponseRedirect("/admin/editprofile")
                if profile.type == 'Client':
                    return HttpResponseRedirect("/client/editprofile")
                if profile.type == 'Owner':
                    return HttpResponseRedirect("/owner/editprofile")
            else:
                error = 'Проверьте пароли на соответствие требованиям и друг другу'
        else:
            error = 'Пароль должен содеражть минимум 8 символов'
    form = PasswordChangeForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, "admin_profile.html", data)


def new_password(request, response):
    try:
        user = User.objects.get(username=response)
        password = password_generate()
        user.set_password(password)
        user.save()
        authenticate(username=user.username, password=password)
        send_mail('Новый пароль', f'Ваш новый пароль для входа в систему {password}',
                  settings.EMAIL_HOST_USER, [response], fail_silently=False)
        return JsonResponse({})
    except User.DoesNotExist:
        return JsonResponse({"<h2>Нет пользователя с такой почтой</h2>"})
