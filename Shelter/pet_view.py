from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from Shelter.forms import CommentForm, PetForm
from Shelter.models import Pet


def petapp(request):
    apps = Pet.objects.all()
    return render(request, 'pets.html', {'apps': apps})


def post_detail(request,id):
    post = Pet.objects.get(id=id)
    comments = post.comments.filter()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.pet = post
            new_comment.save()
            return HttpResponseRedirect(f"/{id}")

    else:
        comment_form = CommentForm()
        return render(request,
                      'pet_detail_view.html',
                      {'post': post,
                       'comments': comments,
                       'new_comment': new_comment,
                       'comment_form': comment_form})


def addpet(request):
    error = ''
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'error'
    form = PetForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'pet_create.html', data)
