from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

from Shelter.forms import CommentForm, TaskForm, DateForm
from Shelter.models import Shelter, Task, Image, Profile
from Shelter.pet_view import handle_uploaded_image


def tasks(request):
    user = request.user
    if user.is_authenticated and user.profile.type == 'Owner':
        shelter = Shelter.objects.get(user=user.profile)
        apps = Task.objects.filter(shelter=shelter)
        images = [Image.objects.filter(task=app).first() for app in apps]
    else:
        apps = Task.objects.all()
        images = [Image.objects.filter(task=app).first() for app in apps]
    return render(request, 'tasks.html', {'apps': zip(apps, images)})

def task_detail(request, id):
    task = Task.objects.get(id=id)
    images = list(Image.objects.filter(task=task))
    comments = task.comments.filter()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if request.user.is_authenticated:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = Profile.objects.get(user=request.user)
                new_comment.task = task
                new_comment.save()
                return JsonResponse({'id': id})
        else:
            return JsonResponse({})
    else:
        comment_form = CommentForm()
        return render(request,
                      'task_detail_view.html',
                      {'task': task,
                       'images': images,
                       'comments': comments,
                       'new_comment': new_comment,
                       'comment_form': comment_form})

def edittask(request, id):
    try:
        task = Task.objects.get(id=id)
        images = list(Image.objects.filter(task=task))
        if request.method == "POST":
            images = request.FILES.getlist('images')
            task.title = request.POST.get("title")
            task.body = request.POST.get("body")
            task.dateExpiration = request.POST.get('dateExpiration')
            task.save()
            if images:
                for i in images:
                    file_path = handle_uploaded_image(i, task)
                    if file_path:
                        fl = Image(task=task, image=file_path)
                        fl.save()
            return HttpResponseRedirect("/tasks")
        else:
            return render(request, "task_edit.html", {"task": task, "images": images})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

def deletetask(request, id):
    try:
        remove = Task.objects.get(id=id)
        remove.delete()
        return HttpResponseRedirect("/tasks")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

def addtask(request):
    profile = Profile.objects.get(user=request.user)
    shelter = Shelter.objects.get(user=profile)
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        form_date = DateForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid() and form_date.is_valid():
            task = Task()
            task.title = form.cleaned_data['title']
            task.body = form.cleaned_data['body']
            task.dateExpiration = form_date.cleaned_data['dateExpiration']
            task.status = 'free'
            task.shelter = shelter
            task.save()
            if images:
                for i in images:
                    file_path = handle_uploaded_image(i, task)
                    if file_path:
                        fl = Image(task=task, image=file_path)
                        fl.save()
            return HttpResponseRedirect("/tasks")
        else:
            error = 'error'
    form = TaskForm()
    form_date = DateForm()
    data = {
        'form': form,
        'form_date': form_date,
        'error': error
    }
    return render(request, 'task_create.html', data)

# def deleteimages_task(request, id):
#     try:
#         remove = Image.objects.get(id=id)
#         id_task = remove.task.id
#         remove.delete()
#         return HttpResponseRedirect(f"/edittask/{id_task}")
#     except Task.DoesNotExist:
#         return HttpResponseNotFound("<h2>News not found</h2>")