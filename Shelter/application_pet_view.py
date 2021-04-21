from datetime import date

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

from Shelter.models import Order, Profile, Shelter, Pet


def app(request):
    profile = Profile.objects.get(user=request.user)
    if profile.type == 'Owner':
        shelter = Shelter.objects.get(user=profile)
        pets = list(Pet.objects.filter(shelter=shelter))
        orders = Order.objects.all()
        apps = [order for order in orders if order.pet in pets]
    if profile.type == 'Client':
        apps = Order.objects.filter(user=profile)
    return render(request, 'pet_applications.html', {'apps': apps})


def rejectorder(request, id):
    try:
        order = Order.objects.get(id=id)
        # pet = Pet.objects.get(id=order.pet.id)
        # pet.owner = order.user
        # order.datePickUp = date.today().strftime("%Y-%m-%d")
        # pet.save()
        order.status = "rejected"
        order.save()
        return HttpResponseRedirect("/pet/applications")
    except Order.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def applay(request, id):
    try:
        order = Order.objects.get(id=id)
        # pet = Pet.objects.get(id=order.pet.id)
        # pet.owner = order.user
        # order.datePickUp = date.today().strftime("%Y-%m-%d")
        # pet.save()
        order.status = "accepted"
        order.save()
        return HttpResponseRedirect("/pet/applications")
    except Order.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
