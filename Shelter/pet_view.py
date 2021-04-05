from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from Shelter import models
from Shelter.forms import CommentForm, PetForm
from Shelter.models import Pet, Profile, Shelter, Image


def petapp(request):
    user = request.user
    if user.is_authenticated and user.profile.type == 'Owner':
        shelter = Shelter.objects.get(user=user.profile)
        apps = Pet.objects.filter(shelter=shelter)
        images = [Image.objects.filter(pet=app).first() for app in apps]
    else:
        apps = Pet.objects.all()
        images = [Image.objects.filter(pet=app).first() for app in apps]
    return render(request, 'pets.html', {'apps': zip(apps, images)})


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
            # form.save()
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
