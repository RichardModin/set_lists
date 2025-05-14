from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import Band, SetList, BandInvite
from .forms import BandForm, SetListForm, UserRegisterForm, SongForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # optionally log them in after registration
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')  # or whatever your homepage is
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    user_bands = request.user.bands.all()
    invites = BandInvite.objects.filter(invited_user=request.user, accepted=False)
    return render(request, 'core/dashboard.html', {'bands': user_bands, 'invites': invites})

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
    return render(request, 'core/band_form.html', {'form': form})

@login_required
def band_detail(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    return render(request, 'core/band_detail.html', {'band': band})

@login_required
def create_setlist(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    if request.method == 'POST':
        form = SetListForm(request.POST)
        if form.is_valid():
            setlist = form.save(commit=False)
            setlist.band = band
            setlist.save()
            form.save_m2m()
            return redirect('core:band_detail', band_id=band.id)
    else:
        form = SetListForm()
    return render(request, 'core/setlist_form.html', {'form': form, 'band': band})

@login_required
def view_setlist(request, setlist_id):
    setlist = get_object_or_404(SetList, id=setlist_id)
    return render(request, 'core/setlist_detail.html', {'setlist': setlist})

@login_required
def invite_member(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            invite = BandInvite.objects.create(band=band, invited_user=email)
            # Send email logic here
            return redirect('core:band_detail', band_id=band.id)
    return render(request, 'core/invite_member.html', {'band': band})

@login_required
def create_song(request, band_id):
    band = get_object_or_404(Band, id=band_id)  # Get the band
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.band = band  # Associate the song with the band
            song.created_by = request.user  # Set the created_by field to the current user
            song.save()
            return redirect('core:band_detail', band_id=band.id)  # Redirect to the band detail page
    else:
        form = SongForm()

    return render(request, 'core/song_form.html', {'form': form, 'band': band})

@login_required
def delete_band(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    if request.method == "POST":
        band.delete()
        messages.success(request, "Band deleted successfully.")
        return redirect('core:dashboard')

    return redirect('core:band_detail', band_id=band.id)
