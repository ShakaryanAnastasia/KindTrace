import mimetypes
import os

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import FileField
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse, Http404, FileResponse
from django.shortcuts import redirect, render

from KindHeart.settings import BASE_DIR
from Shelter import models
from Shelter.forms import ApplicationOwnerForm
from Shelter.models import OwnerApplication, Files, Profile, Shelter


def download_file(request, id):
    file = Files.objects.get(id=id)
    if os.path.exists(file.file.path):
        response = FileResponse(open(file.file.path, 'rb'))
        return response
    raise Http404


def create(request):
    error = ''
    if request.method == 'POST':
        form = ApplicationOwnerForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            application = OwnerApplication()
            application.name = form.cleaned_data['name']
            application.surname = form.cleaned_data['surname']
            application.email = form.cleaned_data['email']
            application.phoneNum = form.cleaned_data['phoneNum']
            application.sex = form.cleaned_data['sex']
            application.save()
            if files:
                for f in files:
                    file_path = handle_uploaded_file(f, application)
                    if file_path:
                        fl = Files(o_application=application, file=file_path)
                        fl.save()
            return redirect('home')
        else:
            error = 'error'
    form = ApplicationOwnerForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'owner_application.html', data)


def handle_uploaded_file(file, instance):
    try:
        if not file:
            return None
        path = models.user_directory_path(instance, file.name)
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return path
    except Exception as e:
        print(e)
        return None


def app(request):
    apps = OwnerApplication.objects.all()
    return render(request, 'owner_applications.html', {'apps': apps})


def read_application_owner(request, id):
    try:
        application = OwnerApplication.objects.get(id=id)
        files = Files.objects.filter(o_application=application).all()
        data = {
            'application': application,
            'files': files
        }
        return render(request, 'detail_view_owner_application.html', data)
    except OwnerApplication.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def delete(request, id):
    try:
        remove = OwnerApplication.objects.get(id=id)
        remove.delete()
        return HttpResponseRedirect("/owner/applications")
    except OwnerApplication.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")



def applay(request, id):
    try:
        owner = OwnerApplication.objects.get(id=id)
        user = User.objects.create_user(owner.email, owner.email, 'qwerty123')
        user.save()
        profile = Profile.objects.get(user=user)
        profile.first_name = owner.name
        profile.last_name = owner.surname
        profile.phoneNum = owner.phoneNum
        profile.type = 'Owner'
        profile.sex = owner.sex
        profile.save()
        Shelter.objects.create(title="", address="", description="", user=profile)
        return HttpResponseRedirect("/owner/applications")
    except OwnerApplication.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
