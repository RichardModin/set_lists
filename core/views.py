from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import Band, SetList, BandInvite, Song, SetListSong
from .forms import BandForm, SetListForm, UserRegisterForm, SongForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # optionally log them in after registration
            messages.success(request, 'Account created successfully!')
            return redirect('core:dashboard')
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
def edit_band(request, band_id):
    band = get_object_or_404(Band, id=band_id)

    if request.method == 'POST':
        form = BandForm(request.POST, instance=band)
        if form.is_valid():
            form.save()
            return redirect('core:band_detail', band_id=band.id)
    else:
        form = BandForm(instance=band)

    return render(request, 'core/band_form.html', {'form': form, 'editing': True, 'band': band})


@login_required
def band_detail(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    unique_artists = band.songs.values_list('artist', flat=True).distinct()
    return render(request, 'core/band_detail.html', {'band': band, 'unique_artists': unique_artists})

@login_required
def create_setlist(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    if request.method == 'POST':
        form = SetListForm(request.POST)
        if form.is_valid():
            setlist = form.save(commit=False)
            setlist.band = band
            setlist.save()

            # Process the songs for the setlist
            song_ids = request.POST.getlist('songs')  # Get the list of song IDs
            if song_ids:  # Ensure there are songs to process
                for order, song_id in enumerate(song_ids, start=1):
                    song = get_object_or_404(Song, id=song_id)
                    SetListSong.objects.create(setlist=setlist, song=song, order=order)
                return redirect('core:band_detail', band_id=band.id)
            else:
                # Handle the case where no songs are provided
                messages.error(request, "You must add at least one song to the setlist.")
                setlist.delete()  # Remove the empty setlist

    else:
        form = SetListForm()
    return render(request, 'core/setlist_form.html', {'form': form, 'band': band})

@login_required
def view_setlist(request, setlist_id):
    setlist = get_object_or_404(SetList, id=setlist_id)
    return render(request, 'core/setlist_detail.html', {'setlist': setlist})

@login_required
def edit_setlist(request, setlist_id):
    setlist = get_object_or_404(SetList, id=setlist_id)
    band = setlist.band

    if request.method == 'POST':
        form = SetListForm(request.POST, instance=setlist)
        if form.is_valid():
            setlist = form.save()

            # Clear existing songs from the setlist
            setlist.setlistsong_set.all().delete()

            # Process the songs for the setlist
            song_ids = request.POST.getlist('songs')  # Get the list of song IDs
            if song_ids:  # Ensure there are songs to process
                for order, song_id in enumerate(song_ids, start=1):
                    song = get_object_or_404(Song, id=song_id)
                    SetListSong.objects.create(setlist=setlist, song=song, order=order)
            else:
                # Handle the case where no songs are provided
                messages.error(request, "You must add at least one song to the setlist.")
                return render(request, 'core/setlist_form.html', {
                    'form': form,
                    'band': band,
                    'setlist': setlist,
                    'edit_mode': True,
                })

            return redirect('core:band_detail', band_id=band.id)
    else:
        form = SetListForm(instance=setlist)

    return render(request, 'core/setlist_form.html', {
        'form': form,
        'band': band,
        'setlist': setlist,
        'edit_mode': True,
    })

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
def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    if request.method == "POST":
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('core:band_detail', band_id=song.band.id)
    else:
        form = SongForm(instance=song)

    return render(request, 'core/song_form.html', {'form': form, 'band': song.band, 'editing': True})

@login_required
def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    band = song.band
    if request.method == "POST":
        song.delete()
        return redirect('core:band_detail', band_id=band.id)  # Update with your actual song list URL name

    return render(request, 'core/song_confirm_delete.html', {'song': song, 'band': band})


@login_required
def delete_band(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    if request.method == "POST":
        band.delete()
        messages.success(request, "Band deleted successfully.")
        return redirect('core:dashboard')

    return redirect('core:band_detail', band_id=band.id)
