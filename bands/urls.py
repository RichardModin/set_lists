from django.urls import path

from . import views

app_name = 'bands'

urlpatterns = [
    path('create/', views.create_band, name='create_band'),
    path('<int:band_id>/', views.band_detail, name='band_detail'),
    path('<int:band_id>/edit/', views.edit_band, name='edit_band'),
    path('<int:band_id>/delete/', views.delete_band, name='delete_band'),
    path('bands/<int:band_id>/invite/', views.invite_member, name='invite_member'),
    path('invite/accept/<int:invite_id>/', views.accept_invite, name='accept_invite'),
]
