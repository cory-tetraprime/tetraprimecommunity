from django.urls import path
from . import views

urlpatterns = [
    path('people/', views.people_view, name='people'),
    path('groups/', views.groups_view, name='groups'),
]
