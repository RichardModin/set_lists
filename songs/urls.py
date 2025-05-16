from django.urls import path

from . import views

app_name = 'songs'

urlpatterns = [
    path('<int:song_id>/view/', views.view_song, name='song_detail'),
    path('<int:band_id>/create/', views.create_song, name='create_song'),
    path('<int:song_id>/edit/', views.edit_song, name='edit_song'),
    path('<int:song_id>/delete/', views.delete_song, name='delete_song'),
    path('<int:band_id>/upload_csv/', views.upload_csv, name='upload_csv'),
]
