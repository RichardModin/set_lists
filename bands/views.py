from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bands.models import Band, BandInvite
from .forms import BandForm

# Create your views here.
@login_required
def create_band(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            band = form.save()
            band.members.add(request.user)
            return redirect('core:dashboard')
    else:
        form = BandForm()
    return render(request, 'bands/band_form.html', {'form': form})

@login_required
def edit_band(request, band_id):
    band = get_object_or_404(Band, id=band_id)

    if request.method == 'POST':
        form = BandForm(request.POST, instance=band)
        if form.is_valid():
            form.save()
            return redirect('bands:band_detail', band_id=band.id)
    else:
        form = BandForm(instance=band)

    return render(request, 'bands/band_form.html', {'form': form, 'editing': True, 'band': band})


@login_required
def band_detail(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    unique_artists = band.songs.values_list('artist', flat=True).distinct()
    return render(request, 'bands/band_detail.html', {'band': band, 'unique_artists': unique_artists})

@login_required
def delete_band(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    if request.method == "POST":
        band.delete()
        messages.success(request, "Band deleted successfully.")
        return redirect('core:dashboard')

    return redirect('bands:band_detail', band_id=band.id)

@login_required
def invite_member(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            invite = BandInvite.objects.create(band=band, invited_user=email)
            # Send email logic here
            return redirect('bands:band_detail', band_id=band.id)
    return render(request, 'bands/invite_member.html', {'band': band})