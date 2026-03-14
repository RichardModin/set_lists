from django.urls import path

from . import views

app_name = 'bands'

urlpatterns = [
    path('create/', views.create_band, name='create_band'),
    path('<int:band_id>/', views.band_detail, name='band_detail'),
    path('<int:band_id>/calendar/', views.band_calendar, name='band_calendar'),
    path('<int:band_id>/songs/', views.band_songs, name='band_songs'),
    path('<int:band_id>/setlists/', views.band_setlists, name='band_setlists'),
    path('<int:band_id>/notes/', views.band_notes, name='band_notes'),
    path('<int:band_id>/manage/', views.band_manage, name='band_manage'),
    path('<int:band_id>/members/<int:user_id>/remove/', views.remove_member, name='remove_member'),
    path('<int:band_id>/invites/<int:invite_id>/delete/', views.delete_invite, name='delete_invite'),
    path('<int:band_id>/edit/', views.edit_band, name='edit_band'),
    path('<int:band_id>/delete/', views.delete_band, name='delete_band'),
    path('bands/<int:band_id>/invite/', views.invite_member, name='invite_member'),
    path('invite/accept/<int:invite_id>/', views.accept_invite, name='accept_invite'),
]
