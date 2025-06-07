from django.urls import path
from . import views

urlpatterns = [
    path('discover/', views.discover_view, name='discover'),
    path('groups/', views.groups_view, name='groups'),
    path('whats-new/', views.tpc_whats_new, name='tpc_whats_new'),
    path('whats-new/release-notes/', views.tpc_whats_new_release_notes, name='tpc_whats_new_release_notes'),
]
