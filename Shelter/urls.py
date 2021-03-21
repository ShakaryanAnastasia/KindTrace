from Shelter import application_owner_view, pet_view
from django.urls import path

urlpatterns = [
    path('owner/application', application_owner_view.create, name='create'),
    path('owner/applications', application_owner_view.app, name = 'application'),
    path('owner/read/<int:id>/', application_owner_view.read_application_owner),
    path('owner/delete/<int:id>/', application_owner_view.delete),
    path('owner/applay/<int:id>/', application_owner_view.applay),
    path('addpet', pet_view.addpet, name ='addpet'),
    path('pets', pet_view.petapp, name='petapp'),
    path('<int:id>/',pet_view.post_detail, name='post_detail')
]