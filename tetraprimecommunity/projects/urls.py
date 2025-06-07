from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_project, name='create_project'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('<int:project_id>/view/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/add-member/', views.add_member, name='add_member'),
    path('<int:project_id>/planner/', views.project_planner, name='project_planner'),
    path('<int:project_id>/notes/', views.project_notes, name='project_notes'),
    path('membership/<int:membership_id>/edit/', views.edit_member, name='edit_member'),
    path('<int:membership_id>/<str:action>/', views.respond_to_invite, name='respond_to_invite'),
    path('planner/next-action/<int:next_action_id>/view/', views.view_next_action, name='view_next_action'),
    # path('planner/next-action/<int:next_action_id>/delete/', views.delete_next_action, name='delete_next_action'),
    path('planner/notes/<int:note_id>/view/', views.view_project_note, name='view_project_note'),
    path('planner/notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('<int:project_id>/planner/notes/create/', views.create_project_note, name='create_project_note'),
]
