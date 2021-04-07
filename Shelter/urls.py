from Shelter import application_owner_view, pet_view, new_view
from django.urls import path

urlpatterns = [
    path('owner/application', application_owner_view.create, name='create'),
    path('owner/applications', application_owner_view.app, name='application'),
    path('owner/read/<int:id>/', application_owner_view.read_application_owner),
    path('owner/delete/<int:id>/', application_owner_view.delete),
    path('owner/applay/<int:id>/', application_owner_view.applay),
    path('addpet', pet_view.addpet, name='addpet'),
    path('pets', pet_view.petapp, name='petapp'),
    path('<int:id>/', pet_view.post_detail, name='post_detail'),
    path('download/<int:id>/', application_owner_view.download_file),
    path('news', new_view.news, name='news'),
    path('news/<int:id>/', new_view.news_detail, name='news_detail'),
    path('editnews/<int:id>/', new_view.editnews, name='editnews'),
    path('editpet/<int:id>/', pet_view.editpet, name='editpet'),
    path('deletenews/<int:id>/', new_view.deletenews),
    path('deletepet/<int:id>/', pet_view.deletepet),
    path('addnews', new_view.addnews),
    path('news/deleteimages/<int:id>/', new_view.deleteimages_new),
    path('pet/deleteimages/<int:id>/', pet_view.deleteimages_pet),
]
