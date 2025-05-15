from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bands.models import Band, BandInvite
from .forms import BandForm, BandInviteForm


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
        form = BandInviteForm(request.POST)
        if form.is_valid():
            invited_user = form.cleaned_data['invited_user']

            # Check if an invite already exists for this user and band
            if BandInvite.objects.filter(band=band, invited_user=invited_user).exists():
                messages.error(request, "This user has already been invited to the band.")
                return redirect('bands:invite_member', band_id=band.id)

            # Create a BandInvite
            BandInvite.objects.create(
                band=band,
                invited_user=invited_user,
                invited_by=request.user
            )

            messages.success(request, "Invitation sent successfully.")
            return redirect('bands:band_detail', band_id=band.id)
    else:
        form = BandInviteForm()

    return render(request, 'bands/invite_user.html', {'form': form, 'band': band})

@login_required
def accept_invite(request, invite_id):
    invite = get_object_or_404(BandInvite, id=invite_id)

    # Only allow the invited user to accept the invite
    if invite.invited_user != request.user:
        return redirect('bands:band_detail', band_id=invite.band.id)

    # Mark the invite as accepted
    invite.accepted = True
    invite.save()

    # Add the user to the band
    invite.band.members.add(request.user)

    messages.success(request, "You have successfully joined the band.")
    return redirect('bands:band_detail', band_id=invite.band.id)