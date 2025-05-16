# core/context_processors.py
from urllib.parse import urlparse
from bands.models import Band
from songs.models import Song
from core.models import SetList

def breadcrumbs(request):
    breadcrumbs = [{'name': 'Home', 'url': '/dashboard/'}]

    if 'bands' in request.path:
        band_id = request.resolver_match.kwargs.get('band_id')
        if band_id:
            try:
                band = Band.objects.get(id=band_id)
                breadcrumbs.append({'name': band.name, 'url': f'/bands/{band_id}/'})
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
                breadcrumbs.append({'name': band_name, 'url': f'/bands/{band_id}/'})

                # Check if the previous URL is from a setlist
                referer = request.META.get('HTTP_REFERER', '')
                parsed_referer = urlparse(referer)
                if 'setlists' in parsed_referer.path:
                    setlist_id = parsed_referer.path.split('/')[-2]  # Extract setlist ID from URL
                    try:
                        setlist = SetList.objects.get(id=setlist_id)
                        breadcrumbs.append({'name': f'Setlist: {setlist.name}', 'url': f'/setlists/{setlist_id}/'})
                    except SetList.DoesNotExist:
                        pass

                breadcrumbs.append({'name': f'Song: {song.title}', 'url': None})
            except Song.DoesNotExist:
                pass

        if 'create' in request.path and band_id:
            try:
                band = Band.objects.get(id=band_id)
                breadcrumbs.append({'name': band.name, 'url': f'/bands/{band_id}/'})
                breadcrumbs.append({'name': 'Create Song', 'url': None})
            except Band.DoesNotExist:
                pass
        elif 'upload_csv' in request.path and band_id:
            try:
                band = Band.objects.get(id=band_id)
                breadcrumbs.append({'name': band.name, 'url': f'/bands/{band_id}/'})
                breadcrumbs.append({'name': 'Upload CSV', 'url': None})
            except Band.DoesNotExist:
                pass
        elif 'edit' in request.path:
            breadcrumbs.append({'name': f'Edit', 'url': None})
        elif 'view' in request.path:
            breadcrumbs.append({'name': f'Details', 'url': None})
        elif 'delete' in request.path:
            breadcrumbs.append({'name': f'Delete', 'url': None})

    if 'setlists' in request.path:
        setlist_id = request.resolver_match.kwargs.get('setlist_id')
        band_id = request.resolver_match.kwargs.get('band_id')
        if setlist_id:
            try:
                setlist = SetList.objects.select_related('band').get(id=setlist_id)
                band_id = setlist.band.id
                band_name = setlist.band.name
                breadcrumbs.append({'name': band_name, 'url': f'/bands/{band_id}/'})
                breadcrumbs.append({'name': f'Setlist {setlist.name}', 'url': None})
            except SetList.DoesNotExist:
                pass

        if 'create' in request.path and band_id:
            try:
                band = Band.objects.get(id=band_id)
                breadcrumbs.append({'name': band.name, 'url': f'/bands/{band_id}/'})
                breadcrumbs.append({'name': 'Create Setlist', 'url': None})
            except Band.DoesNotExist:
                pass
        elif 'edit' in request.path:
            breadcrumbs.append({'name': f'Edit', 'url': None})
        elif 'view' in request.path:
            breadcrumbs.append({'name': f'Details', 'url': None})
        elif 'delete' in request.path:
            breadcrumbs.append({'name': f'Delete', 'url': None})

    return {'breadcrumbs': breadcrumbs}