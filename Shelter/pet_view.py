from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from Shelter.forms import CommentForm, PetForm
from Shelter.models import Pet, Profile, Shelter


def petapp(request):
    user = request.user
    if user.is_authenticated and user.profile.type == 'Owner':
        shelter = Shelter.objects.get(user=user.profile)
        apps = Pet.objects.filter(shelter=shelter)
    else:
        apps = Pet.objects.all()
    return render(request, 'pets.html', {'apps': apps})


def post_detail(request, id):
    post = Pet.objects.get(id=id)
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
                # return HttpResponseRedirect(f"/{id}")
                return JsonResponse({'id': id})
        else:
            return JsonResponse({})
    else:
        comment_form = CommentForm()
        return render(request,
                      'pet_detail_view.html',
                      {'post': post,
                       'comments': comments,
                       'new_comment': new_comment,
                       'comment_form': comment_form})


def addpet(request):
    profile = Profile.objects.get(user = request.user)
    shelter = Shelter.objects.get(user=profile)
    error = ''
    if request.method == 'POST':
        form = PetForm(request.POST)
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
            return HttpResponseRedirect("/pets")
        else:
            error = 'error'
    form = PetForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'pet_create.html', data)
