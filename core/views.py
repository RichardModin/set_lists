from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from songs.models import Notes
from .decorators import user_has_access_to_band_or_song
from .models import SetList, Song, SetListSong
from bands.models import Band, BandInvite
from .forms import SetListForm, UserRegisterForm, DuplicateSetListForm

SECRET_PASSCODE = "dwkjtvssgssfdhajk"

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        passcode = request.POST.get("passcode")
        if passcode != SECRET_PASSCODE:
            messages.error(request, "Invalid passcode.")
        elif form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in
            messages.success(request, "Account created successfully!")
            return redirect("core:dashboard")  # Redirect to the dashboard
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def dashboard(request):
    user_bands = request.user.bands.all()
    invites = BandInvite.objects.filter(invited_user=request.user, accepted=False)
    return render(request, 'core/dashboard.html', {'bands': user_bands, 'invites': invites})

@login_required
@user_has_access_to_band_or_song
def view_setlist(request, setlist_id):
    setlist = get_object_or_404(SetList, id=setlist_id)
    return render(request, 'core/setlist_detail.html', {'setlist': setlist})

@login_required
@user_has_access_to_band_or_song
def duplicate_setlist(request, setlist_id):
    original_setlist = get_object_or_404(SetList, id=setlist_id)
    band = original_setlist.band

    if request.method == "POST":
        form = DuplicateSetListForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data["name"]
            new_setlist = SetList.objects.create(name=new_name, band=band)
            for sl_song in original_setlist.setlistsong_set.all():
                SetListSong.objects.create(
                    setlist=new_setlist,
                    song=sl_song.song,
                    order=sl_song.order
                )
            messages.success(request, "Set list duplicated successfully.")
            return redirect("bands:band_detail", band_id=band.id)
    else:
        form = DuplicateSetListForm(initial={"name": f"{original_setlist.name} (Copy)"})

    return render(request, "core/duplicate_setlist.html", {
        "form": form,
        "original_setlist": original_setlist,
        "band": band,
    })

@login_required
@user_has_access_to_band_or_song
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
                return redirect('bands:band_detail', band_id=band.id)
            else:
                # Handle the case where no songs are provided
                messages.error(request, "You must add at least one song to the setlist.")
                setlist.delete()  # Remove the empty setlist

    else:
        form = SetListForm()
    return render(request, 'core/setlist_form.html', {'form': form, 'band': band})

@login_required
@user_has_access_to_band_or_song
def edit_setlist(request, setlist_id):
    setlist = get_object_or_404(SetList, id=setlist_id)
    band = setlist.band

    if request.method == 'POST':
        form = SetListForm(request.POST, instance=setlist)
        if form.is_valid():
            setlist = form.save(commit=False)

            # Clear existing songs from the setlist
            setlist.setlistsong_set.all().delete()

            # Process the songs for the setlist
            song_ids = request.POST.getlist('songs')  # Get the list of song IDs
            if song_ids:  # Ensure there are songs to process
                for order, song_id in enumerate(song_ids, start=1):
                    song = get_object_or_404(Song, id=song_id)
                    SetListSong.objects.create(setlist=setlist, song=song, order=order)
                messages.success(request, "Setlist updated successfully.")
            else:
                # Handle the case where no songs are provided
                messages.error(request, "You must add at least one song to the setlist.")
                setlist.delete()  # Remove the empty setlist
    else:
        form = SetListForm(instance=setlist)

    return render(request, 'core/setlist_form.html', {
        'form': form,
        'band': band,
        'setlist': setlist,
        'edit_mode': True,
    })

@login_required
@user_has_access_to_band_or_song
def delete_setlist(request, setlist_id):
    setlist = get_object_or_404(SetList, id=setlist_id)
    band = setlist.band

    if request.method == "POST":
        setlist.delete()
        messages.success(request, "Setlist deleted successfully.")
        return redirect('bands:band_detail', band_id=band.id)

    return render(request, 'core/setlist_confirm_delete.html', {'setlist': setlist})

@require_POST
@login_required
@user_has_access_to_band_or_song
def delete_note(request):
    note_id = request.POST.get('note_id')
    try:
        note = Notes.objects.get(id=note_id, user=request.user)
        note.delete()
        return JsonResponse({'success': True})
    except Notes.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Note not found'}, status=404)