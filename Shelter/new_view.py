from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect

from Shelter.forms import CommentForm, NewsForm
from Shelter.models import News, Profile, Shelter, Image
from Shelter.pet_view import handle_uploaded_image


def news(request):
    user = request.user
    if user.is_authenticated and user.profile.type == 'Owner':
        shelter = Shelter.objects.get(user=user.profile)
        apps = News.objects.filter(shelter=shelter)
        images = [Image.objects.filter(news=app).first() for app in apps]
    else:
        apps = News.objects.all()
        images = [Image.objects.filter(news=app).first() for app in apps]
    return render(request, 'news.html', {'apps': zip(apps, images)})


def news_detail(request, id):
    new = News.objects.get(id=id)
    images = list(Image.objects.filter(news=new))
    comments = new.comments.filter()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if request.user.is_authenticated:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = Profile.objects.get(user=request.user)
                new_comment.news = new
                new_comment.save()
                return JsonResponse({'id': id})
        else:
            return JsonResponse({})
    else:
        comment_form = CommentForm()
        return render(request,
                      'news_detail_view.html',
                      {'new': new,
                       'images': images,
                       'comments': comments,
                       'new_comment': new_comment,
                       'comment_form': comment_form})


def editnews(request, id):
    try:
        news = News.objects.get(id=id)
        images = list(Image.objects.filter(news=news))
        if request.method == "POST":
            images = request.FILES.getlist('images')
            news.title = request.POST.get("title")
            news.anons = request.POST.get("anons")
            news.body = request.POST.get("body")
            news.save()
            if images:
                for i in images:
                    file_path = handle_uploaded_image(i, news)
                    if file_path:
                        fl = Image(news=news, image=file_path)
                        fl.save()
            return HttpResponseRedirect("/news")
        else:
            return render(request, "news_edit.html", {"news": news, "images": images})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")


def deletenews(request, id):
    try:
        remove = News.objects.get(id=id)
        remove.delete()
        return HttpResponseRedirect("/news")
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")


def addnews(request):
    profile = Profile.objects.get(user=request.user)
    shelter = Shelter.objects.get(user=profile)
    error = ''
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            news = News()
            news.title = form.cleaned_data['title']
            news.anons = form.cleaned_data['anons']
            news.body = form.cleaned_data['body']
            news.shelter = shelter
            news.save()
            if images:
                for i in images:
                    file_path = handle_uploaded_image(i, news)
                    if file_path:
                        fl = Image(news=news, image=file_path)
                        fl.save()
            return HttpResponseRedirect("/news")
        else:
            error = 'error'
    form = NewsForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'news_create.html', data)

def deleteimages_new(request, id):
    try:
        remove = Image.objects.get(id=id)
        id_news = remove.news.id
        remove.delete()
        return HttpResponseRedirect(f"/editnews/{id_news}")
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")