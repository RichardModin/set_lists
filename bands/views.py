from datetime import date, timedelta
import calendar

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from bands.models import Band, BandInvite
from core.decorators import user_has_access_to_band_or_song
from core.models import Event
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
@user_has_access_to_band_or_song
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
@user_has_access_to_band_or_song
def band_detail(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    unique_artists = band.songs.values_list('artist', flat=True).distinct()
    user_notes = request.user.notes.filter(song__band_id=band_id)

    # Calendar context
    today = date.today()
    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
        if month < 1 or month > 12:
            raise ValueError
    except ValueError:
        year = today.year
        month = today.month

    first_of_month = date(year, month, 1)
    _, last_day_num = calendar.monthrange(year, month)
    last_of_month = date(year, month, last_day_num)

    month_events = (
        Event.objects.filter(band=band, date__gte=first_of_month, date__lte=last_of_month)
        .select_related("venue", "created_by")
        .order_by("date", "time")
    )
    events_by_date = {}
    for event in month_events:
        events_by_date.setdefault(event.date, []).append(event)

    cal = calendar.Calendar(firstweekday=6)  # Sunday
    calendar_weeks = []
    for week in cal.monthdatescalendar(year, month):
        week_days = []
        for day in week:
            week_days.append(
                {
                    "date": day,
                    "in_current_month": day.month == month,
                    "events": events_by_date.get(day, []),
                }
            )
        calendar_weeks.append(week_days)

    prev_month_date = first_of_month - timedelta(days=1)
    next_month_date = last_of_month + timedelta(days=1)

    context = {
        "band": band,
        "unique_artists": unique_artists,
        "user_notes": user_notes,
        "calendar_weeks": calendar_weeks,
        "current_year": year,
        "current_month": month,
        "current_month_name": calendar.month_name[month],
        "prev_year": prev_month_date.year,
        "prev_month": prev_month_date.month,
        "next_year": next_month_date.year,
        "next_month": next_month_date.month,
    }

    return render(request, "bands/band_detail.html", context)

@login_required
@user_has_access_to_band_or_song
def delete_band(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    if request.method == "POST":
        band.delete()
        messages.success(request, "Band deleted successfully.")
        return redirect('core:dashboard')

    return redirect('bands:band_detail', band_id=band.id)

@login_required
@user_has_access_to_band_or_song
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