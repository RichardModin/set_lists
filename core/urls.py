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
    path('bands/<int:band_id>/events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/delete_note/', views.delete_event_note, name='delete_event_note'),
]
