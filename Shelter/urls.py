from Shelter import application_owner_view, pet_view, new_view, task_view, views, application_pet_view
from django.urls import path

urlpatterns = [
    path('owner/application', application_owner_view.create, name='create'),
    path('owner/applications', application_owner_view.app, name='application'),
    path('owner/read/<int:id>/', application_owner_view.read_application_owner),
    path('owner/delete/<int:id>/<str:response>', application_owner_view.delete),
    path('owner/applay/<int:id>/', application_owner_view.applay),
    path('addpet', pet_view.addpet, name='addpet'),
    path('pets/<int:num>/', pet_view.petapp, name='petapp'),
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
    path('tasks', task_view.tasks, name='tasks'),
    path('addtask', task_view.addtask),
    path('task/<int:id>/', task_view.task_detail, name='task_detail'),
    path('edittask/<int:id>/', task_view.edittask, name='edittask'),
    path('deletetask/<int:id>/', task_view.deletetask),
    path('task/deleteimages/<int:id>/', task_view.deleteimages_task),
    path('owner/editprofile', views.editprofileowner, name='editprofileowner'),
    path('pet/applications/<int:num>/', application_pet_view.app),
    path('pet/applications/reject/<int:id>/', application_pet_view.rejectorder),
    path('pet/applications/applay/<int:id>/', application_pet_view.applay),
    path('pet/applications/confirm/<int:id>/', application_pet_view.confirm),
    path('client/editprofile', views.editprofileclient, name='editprofileclient'),
    path('admin/editprofile', views.changepassword, name='editprofileadmin'),
    path('client/pets', pet_view.list_pet, name='client_pets'),
    path('client/changepassword/', views.changepassword),
    path('owner/changepassword/', views.changepassword),
    path('create_application/<int:id>/<str:response>', application_pet_view.create_application),
    path('delete_application_pet/<int:id>/', application_pet_view.deletepetapplications),
    path('report/<int:id>/', pet_view.report_detail, name='post_report'),
]
