from django.http import Http404
from bands.models import Band
from songs.models import Song
from core.models import SetList  # Assuming Setlist is defined in core/models.py

def user_has_access_to_band_or_song(view_func):
    def _wrapped_view(request, *args, **kwargs):
        band_id = kwargs.get('band_id')
        song_id = kwargs.get('song_id')
        setlist_id = kwargs.get('setlist_id')

        # Infer band_id from song_id if not provided
        if not band_id and song_id:
            song = Song.objects.filter(id=song_id).select_related('band').first()
            if song:
                band_id = song.band.id

        # Infer band_id from setlist_id if not provided
        if not band_id and setlist_id:
            setlist = SetList.objects.filter(id=setlist_id).select_related('band').first()
            if setlist:
                band_id = setlist.band.id

        # Check if the user has access to the band
        if band_id:
            band = Band.objects.filter(id=band_id, members=request.user).first()
            if not band:
                raise Http404("You do not have permission to access this band.")

        return view_func(request, *args, **kwargs)
    return _wrapped_view