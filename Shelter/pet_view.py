from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from Shelter import models
from Shelter.forms import CommentForm, PetForm, ReportForm
from Shelter.models import Pet, Profile, Shelter, Image, Report


def petapp(request, num):
    user = request.user
    if user.is_authenticated and user.profile.type == 'Owner':
        if num == 1:
            shelter = Shelter.objects.get(user=user.profile)
            pets = Pet.objects.filter(shelter=shelter)
            apps = [pet for pet in pets if pet.owner_id == None]
            images = [Image.objects.filter(pet=app).first() for app in apps]
        if num == 2:
            shelter = Shelter.objects.get(user=user.profile)
            pets = Pet.objects.filter(shelter=shelter)
            apps = [pet for pet in pets if pet.owner_id != None]
            images = [Image.objects.filter(pet=app).first() for app in apps]
    else:
        pets = Pet.objects.all()
        apps = [pet for pet in pets if pet.owner == None]
        images = [Image.objects.filter(pet=app).first() for app in apps]
    return render(request, 'pets.html', {'apps': zip(apps, images), 'num': num})


def list_pet(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    pets = Pet.objects.filter(owner=profile)
    images = [Image.objects.filter(pet=pet).first() for pet in pets]
    return render(request, 'clients_pets.html', {'apps': zip(pets, images)})


def post_detail(request, id):
    post = Pet.objects.get(id=id)
    images = list(Image.objects.filter(pet=post))
    comments = post.comments.filter()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if request.user.is_authenticated:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = Profile.objects.get(user=request.user)
                new_comment.pet = post
                new_comment.save()
                return JsonResponse({'id': id})
        else:
            return JsonResponse({})
    else:
        comment_form = CommentForm()
        return render(request,
                      'pet_detail_view.html',
                      {'post': post,
                       'images': images,
                       'comments': comments,
                       'new_comment': new_comment,
                       'comment_form': comment_form})


def addpet(request):
    profile = Profile.objects.get(user=request.user)
    shelter = Shelter.objects.get(user=profile)
    error = ''
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            pet = Pet()
            pet.name = form.cleaned_data['name']
            pet.age = form.cleaned_data['age']
            pet.sex = form.cleaned_data['sex']
            pet.type = form.cleaned_data['type']
            pet.color = form.cleaned_data['color']
            pet.wool = form.cleaned_data['wool']
            pet.character = form.cleaned_data['character']
            pet.description = form.cleaned_data['description']
            pet.shelter = shelter
            pet.save()
            if images:
                for i in images:
                    file_path = handle_uploaded_image(i, pet)
                    if file_path:
                        fl = Image(pet=pet, image=file_path)
                        fl.save()
            return HttpResponseRedirect("/pets")
        else:
            error = 'error'
    form = PetForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'pet_create.html', data)


def handle_uploaded_image(file, instance):
    try:
        if not file:
            return None
        path = models.user_directory_path_image(instance, file.name)
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return path
    except Exception as e:
        print(e)
        return None


def editpet(request, id):
    try:
        sexes = Pet.SEX_CHOICES
        types = Pet.TYPE_CHOICES
        colors = Pet.COLOR_CHOICES
        wools = Pet.WOOL_CHOICES
        characters = Pet.CHARACTER_CHOICES
        pet = Pet.objects.get(id=id)
        images = list(Image.objects.filter(pet=pet))
        if request.method == "POST":
            images = request.FILES.getlist('images')
            pet.name = request.POST.get("name")
            pet.age = request.POST.get("age")
            pet.sex = request.POST.get("sex")
            pet.type = request.POST.get("type")
            pet.color = request.POST.get("color")
            pet.wool = request.POST.get("wool")
            pet.character = request.POST.get("character")
            pet.description = request.POST.get("description")
            if request.POST.get("check") == 'check':
                pet.owner = Profile.objects.get(user=request.user)
            pet.save()
            if images:
                for i in images:
                    file_path = handle_uploaded_image(i, pet)
                    if file_path:
                        fl = Image(pet=pet, image=file_path)
                        fl.save()
            return HttpResponseRedirect("/pets/1")
        else:
            return render(request, "pet_edit.html",
                          {"pet": pet, "images": images, "sexes": sexes, "types": types, "colors": colors,
                           "wools": wools, "characters": characters})
    except Pet.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")


def deletepet(request, id):
    try:
        remove = Pet.objects.get(id=id)
        remove.delete()
        return HttpResponseRedirect("/pets")
    except Pet.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")


def deleteimages_pet(request, id):
    try:
        remove = Image.objects.get(id=id)
        id_pet = remove.pet.id
        remove.delete()
        return HttpResponseRedirect(f"/editpet/{id_pet}")
    except Pet.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")


def report_detail(request, id):
    post = Pet.objects.get(id=id)
    pet_images = list(Image.objects.filter(pet=post))
    reports = Report.objects.filter(pet=post)
    images_reports = [list(Image.objects.filter(report=report)) for report in reports]
    new_report = None
    if request.method == 'POST':
        report_form = ReportForm(request.POST, request.FILES)
        if report_form.is_valid():
            images = request.FILES.getlist('images')
            new_report = report_form.save(commit=False)
            new_report.user = Profile.objects.get(user=request.user)
            new_report.pet = post
            new_report.save()
            if images:
                for i in images:
                    file_path = handle_uploaded_image(i, new_report)
                    if file_path:
                        fl = Image(report=new_report, image=file_path)
                        fl.save()
            return HttpResponseRedirect(f"/report/{id}")
    else:
        report_form = ReportForm()
        return render(request,
                      'pet_report.html',
                      {'post': post,
                       'images': pet_images,
                       'reports': zip(reports, images_reports),
                       'new_report': new_report,
                       'report_form': report_form})
