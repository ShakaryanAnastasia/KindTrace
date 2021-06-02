from datetime import date

from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render

from Shelter.models import Order, Profile, Shelter, Pet


def app(request, num):
    profile = Profile.objects.get(user=request.user)
    if profile.type == 'Owner':
        shelter = Shelter.objects.get(user=profile)
        pets = list(Pet.objects.filter(shelter=shelter))
        orders = Order.objects.all()
        orders_1 = [order for order in orders if order.pet in pets]
        if num == 1:
            apps = [order for order in orders_1 if order.status == 'sent']
            apps = apps.reverse()
        if num == 2:
            apps = [order for order in orders_1 if order.status == 'accepted']
            apps = apps.reverse()
    if profile.type == 'Client':
        apps = Order.objects.filter(user=profile).reverse()
    return render(request, 'pet_applications.html', {'apps': apps, 'num': num})


def rejectorder(request, id):
    try:
        order = Order.objects.get(id=id)
        order.status = "rejected"
        order.save()
        return HttpResponseRedirect("/pet/applications/1")
    except Order.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def applay(request, id):
    try:
        order = Order.objects.get(id=id)
        order.status = "accepted"
        order.save()
        return HttpResponseRedirect("/pet/applications/1")
    except Order.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def confirm(request, id):
    try:
        order = Order.objects.get(id=id)
        pet = Pet.objects.get(id=order.pet.id)
        pet.owner = order.user
        order.datePickUp = date.today().strftime("%Y-%m-%d")
        pet.save()
        order.status = "confirmed"
        order.save()
        orders_for_this_pet = Order.objects.filter(pet=pet)
        if orders_for_this_pet:
            for ord in orders_for_this_pet:
                if ord.status != "confirmed":
                    ord.status = "rejected"
                    ord.save()
        return HttpResponseRedirect("/pet/applications/2")
    except Order.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def create_application(request, id, response):
    try:
        pet = Pet.objects.get(id=id)
        user = Profile.objects.get(user=request.user)
        Order.objects.create(pet=pet, user=user, dateViewing=response, status='sent')
        return JsonResponse({})
    except Order.DoesNotExist:
        return JsonResponse({"<h2>Pet not found</h2>"})

def deletepetapplications(request, id):
    try:
        remove = Order.objects.get(id=id)
        remove.delete()
        return HttpResponseRedirect("/pet/applications/1")
    except Pet.DoesNotExist:
        return HttpResponseNotFound("<h2>Order not found</h2>")