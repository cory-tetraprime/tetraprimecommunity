from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_project, name='create_project'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('<int:project_id>/view/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/add-member/', views.add_member, name='add_member'),
    path('<int:membership_id>/<str:action>/', views.respond_to_invite, name='respond_to_invite'),
    path('membership/<int:membership_id>/edit/', views.edit_member, name='edit_member'),
]
