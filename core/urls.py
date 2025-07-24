from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_note/', views.delete_note, name='delete_note'),
    path('setlists/<int:band_id>/create/', views.create_setlist, name='create_setlist'),
    path('setlists/<int:setlist_id>/edit/', views.edit_setlist, name='edit_setlist'),
    path('setlists/<int:setlist_id>/', views.view_setlist, name='view_setlist'),
    path('setlists/<int:setlist_id>/delete/', views.delete_setlist, name='delete_setlist'),
    path('setlists/<int:setlist_id>/duplicate/', views.duplicate_setlist, name='duplicate_setlist'),
]
