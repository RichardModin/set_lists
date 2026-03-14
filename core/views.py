from datetime import date
from urllib.parse import urlencode

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

from songs.models import Notes
from .decorators import user_has_access_to_band_or_song
from .models import SetList, Event, EventNote
from bands.models import Band, BandInvite
from .forms import SetListForm, UserRegisterForm, DuplicateSetListForm, EventForm, EventNoteForm

SECRET_PASSCODE = "dwkjtvssgssfdhajk"


def _band_calendar_url(band_id, event_date):
    return f"{reverse('bands:band_calendar', kwargs={'band_id': band_id})}?{urlencode({'year': event_date.year, 'month': event_date.month})}"


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
    user_bands = request.user.bands.prefetch_related('members').all()
    invites = BandInvite.objects.filter(invited_user=request.user, accepted=False).select_related('band', 'invited_by')

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
            # Copy ordered song IDs from the original setlist
            new_setlist.song_ids = list(original_setlist.song_ids or [])
            new_setlist.save()
            messages.success(request, "Set list duplicated successfully.")
            return redirect("bands:band_setlists", band_id=band.id)
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
    if request.method == "POST":
        form = SetListForm(request.POST)
        if form.is_valid():
            setlist = form.save(commit=False)
            setlist.band = band

            # Process the songs for the setlist using ordered song IDs
            song_ids = request.POST.getlist("songs")
            if song_ids:
                setlist.song_ids = [int(song_id) for song_id in song_ids]
                setlist.save()
                return redirect("bands:band_setlists", band_id=band.id)
            else:
                # Handle the case where no songs are provided
                messages.error(request, "You must add at least one song to the setlist.")

    else:
        form = SetListForm()
    return render(request, "core/setlist_form.html", {"form": form, "band": band})


@login_required
@user_has_access_to_band_or_song
def edit_setlist(request, setlist_id):
    setlist = get_object_or_404(SetList, id=setlist_id)
    band = setlist.band

    if request.method == "POST":
        form = SetListForm(request.POST, instance=setlist)
        if form.is_valid():
            setlist = form.save(commit=False)

            # Process the songs for the setlist using ordered song IDs
            song_ids = request.POST.getlist("songs")
            if song_ids:
                setlist.song_ids = [int(song_id) for song_id in song_ids]
                setlist.save()
                messages.success(request, "Setlist updated successfully.")
            else:
                # Handle the case where no songs are provided
                messages.error(request, "You must add at least one song to the setlist.")
    else:
        form = SetListForm(instance=setlist)

    return render(
        request,
        "core/setlist_form.html",
        {
            "form": form,
            "band": band,
            "setlist": setlist,
            "edit_mode": True,
        },
    )


@login_required
@user_has_access_to_band_or_song
def delete_setlist(request, setlist_id):
    setlist = get_object_or_404(SetList, id=setlist_id)
    band = setlist.band

    if request.method == "POST":
        setlist.delete()
        messages.success(request, "Setlist deleted successfully.")
        return redirect('bands:band_setlists', band_id=band.id)

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


@login_required
@user_has_access_to_band_or_song
def create_event(request, band_id):
    band = get_object_or_404(Band, id=band_id)

    initial = {}
    year = request.GET.get("year")
    month = request.GET.get("month")
    day = request.GET.get("day")
    if year and month and day:
        try:
            initial["date"] = date(int(year), int(month), int(day))
        except ValueError:
            pass

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.band = band
            event.created_by = request.user
            event.save()
            return redirect(_band_calendar_url(band.id, event.date))
    else:
        form = EventForm(initial=initial)

    return render(request, "core/event_form.html", {"form": form, "band": band, "year": year, "month": month})


@login_required
@user_has_access_to_band_or_song
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    band = event.band

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect(_band_calendar_url(band.id, event.date))
    else:
        form = EventForm(instance=event)

    return render(request, "core/event_form.html", {"form": form, "band": band, "event": event, "year": event.date.year, "month": event.date.month})


@login_required
@user_has_access_to_band_or_song
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    band = event.band

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect(_band_calendar_url(band.id, event.date))

    return render(request, "core/event_confirm_delete.html", {"event": event, "band": band})


@login_required
@user_has_access_to_band_or_song
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    band = event.band
    user_note = EventNote.objects.filter(event=event, user=request.user).first()

    if request.method == "POST":
        form = EventNoteForm(request.POST, instance=user_note)
        if form.is_valid():
            note = form.save(commit=False)
            note.event = event
            note.user = request.user
            note.save()
            messages.success(request, "Your private note has been saved.")
            return redirect("core:event_detail", event_id=event.id)
    else:
        form = EventNoteForm(instance=user_note)

    return render(
        request,
        "core/event_detail.html",
        {
            "event": event,
            "band": band,
            "user_note": user_note,
            "form": form,
        },
    )


@require_POST
@login_required
@user_has_access_to_band_or_song
def delete_event_note(request):
    note_id = request.POST.get("note_id")
    try:
        note = EventNote.objects.get(id=note_id, user=request.user)
        note.delete()
        return JsonResponse({"success": True})
    except EventNote.DoesNotExist:
        return JsonResponse({"success": False, "error": "Note not found"}, status=404)