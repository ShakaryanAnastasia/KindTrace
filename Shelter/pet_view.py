import os
from datetime import date, datetime

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from Shelter import models
from Shelter.forms import CommentForm, PetForm, ReportForm
from Shelter.models import Pet, Profile, Shelter, Image, Report, Order

from keras.applications import VGG19
from keras.engine import Model
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input

from sklearn.neighbors import NearestNeighbors

import numpy as np
import tensorflow as tf
import logging
import csv

FILENAME = "vecs.csv"

logger = tf.get_logger()
logger.setLevel(logging.ERROR)

model = VGG19(weights='imagenet', include_top=False)
bm = VGG19(weights='imagenet')
model = Model(inputs=bm.input, outputs=bm.get_layer('fc1').output)

knn = NearestNeighbors(metric='cosine', algorithm='brute')
length = 4096


# pets = Pet.objects.filter(owner=None)
# images = [Image.objects.filter(pet=pet).first() for pet in pets]

def write_in_csv(list_of_image):
    for imge in list_of_image:
        if imge.pet.vector == "":
            # path = os.path.join(train_catt_dir, name_img)
            path = imge.image.path
            img = image.load_img(path, target_size=(224, 224))  # чтение из файла
            x = image.img_to_array(img)  # сырое изображения в вектор
            x = np.expand_dims(x, axis=0)  # превращаем в вектор-строку (2-dims)
            x = preprocess_input(x)  # библиотечная подготовка изображения
            vec = model.predict(x).ravel()
            imge.pet.vector = ",".join(map(str, vec.tolist()))
            imge.pet.save()
            # with open(FILENAME, "a", newline="") as file:
            #     writer = csv.writer(file)
            #     writer.writerow(vec)


def load_images_vectors(count, length, list_images):
    vecs = np.ndarray(shape=(count, length), dtype=float, order='F')
    i = 0
    for image in list_images:
        vector = image.pet.vector.split(',')
        print(image.pet.vector)
        vecs[i] = vector
        i += 1
    # with open(FILENAME, "r", newline="") as file:
    #     reader = csv.reader(file, delimiter=",")
    #     i = 0
    #     for row in reader:
    #         vecs[i] = row
    #         i += 1
    return vecs


def petapp(request, num):
    user = request.user
    params = {}
    apps = []
    images = []
    sexes = Pet.SEX_CHOICES
    types = Pet.TYPE_CHOICES
    colors = Pet.COLOR_CHOICES
    wools = Pet.WOOL_CHOICES
    characters = Pet.CHARACTER_CHOICES
    days = []

    def reset():
        params = {'sex': [],
                  'petTypes': [], 'ageFrom': 0,
                  'ageTo': max([pet.age for pet in Pet.objects.all() if pet.owner == None])}

        pets = Pet.objects.all()
        apps = [pet for pet in pets if pet.owner == None]

        if user.is_authenticated and user.profile.type == 'Owner':
            shelter = Shelter.objects.get(user=user.profile)
            pets = Pet.objects.filter(shelter=shelter)
            if num == 1:
                apps = [pet for pet in pets if pet.owner == None]
            if num == 2:
                apps = [pet for pet in pets if pet.owner != None]

        images = [Image.objects.filter(pet=app).first() for app in apps]
        return params, apps, images

    if request.method == 'GET':
        params, apps, images = reset()

    elif request.method == 'POST':
        if 'reset' in request.POST:
            params, apps, images = reset()

        if 'apply' in request.POST:
            params = {}
            params['type'] = request.POST.get('type')
            if not params['type']:
                params['type'] = [type[0] for type in types]

            params['ageFrom'] = request.POST.get('ageFrom')
            params['ageTo'] = request.POST.get('ageTo')

            params['ageFrom'] = int(params['ageFrom']) if params['ageFrom'].isdigit() else 0
            params['ageTo'] = int(params['ageTo']) \
                if params['ageTo'].isdigit() and int(params['ageTo']) >= params['ageFrom'] else \
                max([pet.age for pet in Pet.objects.all() if pet.owner == None])

            params['sex'] = request.POST.get('sex')
            if not params['sex']:
                params['sex'] = [sex[0] for sex in sexes]
            params['color'] = request.POST.get('color')
            if not params['color']:
                params['color'] = [color[0] for color in colors]
            params['wool'] = request.POST.get('wool')
            if not params['wool']:
                params['wool'] = [wool[0] for wool in wools]
            params['character'] = request.POST.get('character')
            if not params['character']:
                params['character'] = [character[0] for character in characters]

            pets = Pet.objects.all()
            apps = [pet for pet in pets if pet.owner == None]

            if user.is_authenticated and user.profile.type == 'Owner':
                shelter = Shelter.objects.get(user=user.profile)
                pets = Pet.objects.filter(shelter=shelter)
                if num == 1:
                    apps = [pet for pet in pets if pet.owner_id == None]
                if num == 2:
                    apps = [pet for pet in pets if pet.owner_id != None]

            apps = [app for app in apps if app.type in params[
                'type'] and params['ageFrom'] <= app.age <= params['ageTo'] and app.sex in params[
                        'sex'] and app.color in params[
                        'color'] and app.wool in params[
                        'wool'] and app.character in params[
                        'character']]

            images = [Image.objects.filter(pet=app).first() for app in apps]

    if num == 2:
        orders = [Order.objects.filter(pet=app).exclude(datePickUp=None).first() for app in apps]
        reports = [Report.objects.filter(pet=app).last() for app in apps]
        for report, order in zip(reports, orders):
            if (order is not None):
                    if report is not None:
                        days.append(date.today() - report.dateCreate)
                    else:
                        days.append(date.today() - order.datePickUp)
            else:
                days.append(None)
    else:
        for app in apps: days.append(None)

    return render(request, 'pets.html',
                  {'apps': zip(apps, images, days), 'num': num, 'params': params, 'sexes': sexes, 'types': types,
                   'colors': colors, 'wools': wools, 'characters': characters})


def list_pet(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    pets = Pet.objects.filter(owner=profile)
    images = [Image.objects.filter(pet=pet).first() for pet in pets]
    return render(request, 'clients_pets.html', {'apps': zip(pets, images)})


def post_detail(request, id):
    pets = list(Pet.objects.filter(owner=None))
    list_images = [Image.objects.filter(pet=pet).first() for pet in pets]

    write_in_csv(list_images)
    vecs = load_images_vectors(len(list_images), length, list_images)
    knn.fit(vecs)
    vec = np.ndarray(shape=(1, length), dtype=float, order='F')

    vec[0] = vecs[pets.index(Pet.objects.get(id=id))]
    dist, indices = knn.kneighbors(vec, n_neighbors=3)
    indices_tolist = indices.tolist()
    similar_images = [
        list_images[indices_tolist[0][i]]
        for i in range(len(indices_tolist[0]))
    ]

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
                       'comment_form': comment_form,
                       'filenames': similar_images[1:]})


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
            imge = Image.objects.filter(pet=pet).first()
            if (imge):
                path = imge.image.path
                img = image.load_img(path, target_size=(224, 224))  # чтение из файла
                x = image.img_to_array(img)  # сырое изображения в вектор
                x = np.expand_dims(x, axis=0)  # превращаем в вектор-строку (2-dims)
                x = preprocess_input(x)  # библиотечная подготовка изображения
                vec = model.predict(x).ravel()
                imge.pet.vector = ",".join(map(str, vec.tolist()))
                imge.pet.save()
            return HttpResponseRedirect("/pets/1")
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
                orders_for_this_pet = Order.objects.filter(pet=pet)
                if orders_for_this_pet:
                    for ord in orders_for_this_pet:
                        ord.status = "rejected"
                        ord.save()
            pet.save()
            if images:
                for i in images:
                    file_path = handle_uploaded_image(i, pet)
                    if file_path:
                        fl = Image(pet=pet, image=file_path)
                        fl.save()
            imge = Image.objects.filter(pet=pet).first()
            if (imge):
                path = imge.image.path
                img = image.load_img(path, target_size=(224, 224))  # чтение из файла
                x = image.img_to_array(img)  # сырое изображения в вектор
                x = np.expand_dims(x, axis=0)  # превращаем в вектор-строку (2-dims)
                x = preprocess_input(x)  # библиотечная подготовка изображения
                vec = model.predict(x).ravel()
                imge.pet.vector = ",".join(map(str, vec.tolist()))
                imge.pet.save()
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
        return HttpResponseRedirect("/pets/1")
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
    reports = list(Report.objects.filter(pet=post))
    reports.reverse()
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
