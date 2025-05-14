from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bands/create/', views.create_band, name='create_band'),
    path('bands/<int:band_id>/', views.band_detail, name='band_detail'),
    path('bands/<int:band_id>/invite/', views.invite_member, name='invite_member'),
    path('bands/<int:band_id>/edit/', views.edit_band, name='edit_band'),
    path('bands/<int:band_id>/delete/', views.delete_band, name='delete_band'),
    path('setlists/<int:band_id>/create/', views.create_setlist, name='create_setlist'),
    path('setlists/<int:setlist_id>/edit/', views.edit_setlist, name='edit_setlist'),
    path('setlists/<int:setlist_id>/', views.view_setlist, name='view_setlist'),
    path('songs/<int:band_id>/create/', views.create_song, name='create_song'),
    path('songs/<int:song_id>/edit/', views.edit_song, name='edit_song'),
    path('songs/<int:song_id>/delete/', views.delete_song, name='delete_song'),
]
