# core/context_processors.py

from bands.models import Band, BandInvite
from songs.models import Song
from core.models import SetList, Event


def _resolve_selected_band(request):
    if not request.user.is_authenticated:
        return None

    resolver_match = getattr(request, "resolver_match", None)
    kwargs = resolver_match.kwargs if resolver_match else {}

    band = None
    band_id = kwargs.get("band_id")
    song_id = kwargs.get("song_id")
    setlist_id = kwargs.get("setlist_id")
    event_id = kwargs.get("event_id")
    invite_id = kwargs.get("invite_id")

    if band_id:
        band = Band.objects.filter(id=band_id, members=request.user).first()
    elif song_id:
        song = Song.objects.filter(id=song_id, band__members=request.user).select_related("band").first()
        band = song.band if song else None
    elif setlist_id:
        setlist = SetList.objects.filter(id=setlist_id, band__members=request.user).select_related("band").first()
        band = setlist.band if setlist else None
    elif event_id:
        event = Event.objects.filter(id=event_id, band__members=request.user).select_related("band").first()
        band = event.band if event else None
    elif invite_id:
        invite = BandInvite.objects.filter(id=invite_id, invited_user=request.user).select_related("band").first()
        band = invite.band if invite else None

    if band:
        request.session["selected_band_id"] = band.id
        return band

    selected_band_id = request.session.get("selected_band_id")
    if selected_band_id:
        band = Band.objects.filter(id=selected_band_id, members=request.user).first()
        if band:
            return band

    band = request.user.bands.order_by("name").first()
    if band:
        request.session["selected_band_id"] = band.id
    return band


def breadcrumbs(request):
    breadcrumbs = [{'name': 'Home', 'url': '/dashboard/'}]

    resolver_match = getattr(request, 'resolver_match', None)
    url_name = resolver_match.url_name if resolver_match else None

    if 'bands' in request.path:
        band_id = request.resolver_match.kwargs.get('band_id')
        if band_id:
            try:
                band = Band.objects.get(id=band_id)
                breadcrumbs.append({'name': band.name, 'url': f'/bands/{band_id}/manage/'})

                page_labels = {
                    'band_calendar': 'Calendar',
                    'band_songs': 'Songs',
                    'band_setlists': 'Set Lists',
                    'band_notes': 'Notes',
                }
                if url_name in page_labels:
                    breadcrumbs.append({'name': page_labels[url_name], 'url': None})
            except Band.DoesNotExist:
                pass

    if 'songs' in request.path:
        song_id = request.resolver_match.kwargs.get('song_id')
        band_id = request.resolver_match.kwargs.get('band_id')
        if song_id:
            try:
                song = Song.objects.select_related('band').get(id=song_id)
                band_id = song.band.id
                band_name = song.band.name
                breadcrumbs.append({'name': band_name, 'url': f'/bands/{band_id}/manage/'})
                breadcrumbs.append({'name': 'Songs', 'url': f'/bands/{band_id}/songs/'})
                breadcrumbs.append({'name': f'Song: {song.title}', 'url': None})

                if 'edit' in request.path:
                    breadcrumbs.append({'name': 'Edit', 'url': None})
                elif 'delete' in request.path:
                    breadcrumbs.append({'name': 'Delete', 'url': None})
            except Song.DoesNotExist:
                pass

        if 'create' in request.path and band_id:
            try:
                band = Band.objects.get(id=band_id)
                breadcrumbs.append({'name': band.name, 'url': f'/bands/{band_id}/manage/'})
                breadcrumbs.append({'name': 'Songs', 'url': f'/bands/{band_id}/songs/'})
                breadcrumbs.append({'name': 'Create Song', 'url': None})
            except Band.DoesNotExist:
                pass
        elif 'upload_csv' in request.path and band_id:
            try:
                band = Band.objects.get(id=band_id)
                breadcrumbs.append({'name': band.name, 'url': f'/bands/{band_id}/manage/'})
                breadcrumbs.append({'name': 'Songs', 'url': f'/bands/{band_id}/songs/'})
                breadcrumbs.append({'name': 'Upload CSV', 'url': None})
            except Band.DoesNotExist:
                pass

    if 'setlists' in request.path:
        setlist_id = request.resolver_match.kwargs.get('setlist_id')
        band_id = request.resolver_match.kwargs.get('band_id')
        if setlist_id:
            try:
                setlist = SetList.objects.select_related('band').get(id=setlist_id)
                band_id = setlist.band.id
                band_name = setlist.band.name
                breadcrumbs.append({'name': band_name, 'url': f'/bands/{band_id}/manage/'})
                breadcrumbs.append({'name': 'Set Lists', 'url': f'/bands/{band_id}/setlists/'})
                breadcrumbs.append({'name': f'Set List: {setlist.name}', 'url': None})

                if 'edit' in request.path:
                    breadcrumbs.append({'name': 'Edit', 'url': None})
                elif 'delete' in request.path:
                    breadcrumbs.append({'name': 'Delete', 'url': None})
            except SetList.DoesNotExist:
                pass

        if 'create' in request.path and band_id:
            try:
                band = Band.objects.get(id=band_id)
                breadcrumbs.append({'name': band.name, 'url': f'/bands/{band_id}/manage/'})
                breadcrumbs.append({'name': 'Set Lists', 'url': f'/bands/{band_id}/setlists/'})
                breadcrumbs.append({'name': 'Create Set List', 'url': None})
            except Band.DoesNotExist:
                pass

    return {'breadcrumbs': breadcrumbs, 'selected_band': _resolve_selected_band(request)}
