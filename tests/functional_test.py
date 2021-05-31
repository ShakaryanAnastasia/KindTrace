from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from Shelter import models
from Shelter.application_pet_view import create_application
from Shelter.pet_view import petapp

import time


class Test(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.home = reverse('home')
        self.owner_app = reverse('create')

    def test_registration_positive(self):
        response = self.client.post(self.signup_url, {
            "first_name": "test",
            "last_name": "test",
            "phoneNum": "88888888888",
            "sex": "male",
            "username": "test@test.ru",
            "password1": "тест1234",
            "password2": "тест1234",
        })

        user = User.objects.get(username="test@test.ru")

        self.assertEqual(response.url, self.home)
        self.assertEqual(True, check_password("тест1234", user.password))

    def test_create_application_owner_positive(self):
        applications_before = list(models.OwnerApplication.objects.all())
        response_owner_app = self.client.post(self.owner_app, {
            "name": "test",
            "surname": "surname",
            "email": "test@test.ru",
            "phoneNum": "88888888888",
            "sex": "male",
            "title_shelter": "test",
            "address_shelter": "test",
            "description_shelter": "test",
        })
        applications_after = list(models.OwnerApplication.objects.all())
        self.assertEqual(response_owner_app.url, self.home)
        self.assertNotEqual(len(applications_before), len(applications_after))

    def test_applay_application_owner_positive(self):
        application_created = models.OwnerApplication.objects.create(
            name="test",
            surname="test",
            email="test@test.ru",
            phoneNum="88888888888",
            sex="male",
            title_shelter="test",
            address_shelter="test",
            description_shelter="",
            status="sent"
        )

        self.owner_app_applay = reverse('applay_applications', args=[application_created.id])
        response = self.client.post(self.owner_app_applay)
        application_changed = models.OwnerApplication.objects.get(id=application_created.id)
        self.assertEqual(application_changed.status, "accepted")

    def test_delete_application_owner_positive(self):
        application_created = models.OwnerApplication.objects.create(
            name="test",
            surname="test",
            email="test@test.ru",
            phoneNum="88888888888",
            sex="male",
            title_shelter="test",
            address_shelter="test",
            description_shelter="",
            status="sent"
        )
        applications_before = list(models.OwnerApplication.objects.all())
        self.owner_app_delete = reverse('delete_applications', args=[application_created.id, "test"])
        response = self.client.post(self.owner_app_delete)
        application_after = list(models.OwnerApplication.objects.all())
        self.assertNotEqual(len(applications_before), len(application_after))


class Pet_App_Test(TestCase):
    def setUp(self):
        self.user_owner = User.objects.create(
            username="test@test.ru",
            password="тест1234"
        )
        self.profile = models.Profile.objects.get(user=self.user_owner)
        self.profile.first_name = "test",
        self.profile.last_name = "test",
        self.profile.phoneNum = "88888888888",
        self.profile.type = 'Owner',
        self.profile.sex = 'male'

        self.user_client = User.objects.create(
            username="test_client@test.ru",
            password="тестиктестик"
        )

        self.shelter = models.Shelter.objects.create(
            title="test",
            address="test",
            description="",
            user=self.profile
        )
        self.pet = models.Pet.objects.create(
            name="test",
            age=3,
            sex='male',
            type='cat',
            color='black',
            wool='bald',
            character='Sanguine',
            description="",
            shelter=self.shelter
        )

    def test_create_pet_application_positive(self):
        factory = RequestFactory()
        pet_app_before = list(models.Order.objects.all())
        self.pet_app_create = reverse('create_pet_app', args=[self.pet.id, "test"])
        request = factory.post(self.pet_app_create)
        request.user = self.user_client
        response = create_application(request, self.pet.id, "2020-10-12 12:25")
        pet_app_after = list(models.Order.objects.all())
        self.assertNotEqual(pet_app_before, pet_app_after)

    def test_applay_pet_application_positive(self):
        profile_client = models.Profile.objects.get(user=self.user_client)
        order = models.Order.objects.create(
            pet=self.pet,
            user=profile_client,
            dateViewing="2020-10-12 12:25",
            status='sent'
        )
        self.pet_app_applay = reverse('pet_app_applay', args=[order.id])
        response = self.client.post(self.pet_app_applay)
        order_applayed = models.Order.objects.get(id=order.id)
        self.assertEqual(order_applayed.status, "accepted")

    def test_reject_pet_application_positive(self):
        profile_client = models.Profile.objects.get(user=self.user_client)
        order = models.Order.objects.create(
            pet=self.pet,
            user=profile_client,
            dateViewing="2020-10-12 12:25",
            status='sent'
        )
        self.pet_app_reject = reverse('pet_app_reject', args=[order.id])
        response = self.client.post(self.pet_app_reject)
        order_rejected = models.Order.objects.get(id=order.id)
        self.assertEqual(order_rejected.status, "rejected")

    def test_confirm_pet_application_positive(self):
        profile_client = models.Profile.objects.get(user=self.user_client)
        order = models.Order.objects.create(
            pet=self.pet,
            user=profile_client,
            dateViewing="2020-10-12 12:25",
            status='sent'
        )
        self.pet_app_confirm = reverse('pet_app_confirm', args=[order.id])
        response = self.client.post(self.pet_app_confirm)
        order_confirmed = models.Order.objects.get(id=order.id)
        self.assertEqual(order_confirmed.status, "confirmed")

    # def test(self):
    #     for i in range(0, 10):
    #         pet = models.Pet.objects.create(
    #             name="test",
    #             age=3,
    #             sex='male',
    #             type='cat',
    #             color='black',
    #             wool='bald',
    #             character='Sanguine',
    #             description="",
    #             shelter=self.shelter
    #         )
    #         models.Image.objects.create(
    #             image='static/images/1_russkaya-belaya.webp',
    #             pet=pet
    #         )
    #     start_time = time.time()
    #     factory = RequestFactory()
    #     self.pets = reverse('pets', args=[1])
    #     request = factory.post(self.pets)
    #     request.user = self.user_client
    #     response = petapp(request, 1)
    #     print("--- %s seconds ---" % (time.time() - start_time))
