from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import csv
from io import TextIOWrapper

from .forms import SongForm
from .models import Song
from bands.models import Band

# Create your views here.
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
            return redirect('bands:band_detail', band_id=band.id)  # Redirect to the band detail page
    else:
        form = SongForm()

    return render(request, 'songs/song_form.html', {'form': form, 'band': band})

@login_required
def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    if request.method == "POST":
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('bands:band_detail', band_id=song.band.id)
    else:
        form = SongForm(instance=song)

    return render(request, 'songs/song_form.html', {'form': form, 'band': song.band, 'editing': True})

@login_required
def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    band = song.band
    if request.method == "POST":
        song.delete()
        return redirect('bands:band_detail', band_id=band.id)  # Update with your actual song list URL name

    return render(request, 'songs/song_confirm_delete.html', {'song': song, 'band': band})

@login_required
def upload_csv(request, band_id):
    band = get_object_or_404(Band, id=band_id)

    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return redirect('songs:upload_csv', band_id=band.id)

        try:
            csv_data = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.DictReader(csv_data)
            for row in reader:
                tempo = row.get('tempo', '').strip()
                Song.objects.create(
                    band=band,
                    title=row.get('title', '').strip(),
                    artist=row.get('artist', '').strip(),
                    key=row.get('key', '').strip() if 'key' in row else None,
                    tempo=float(tempo) if tempo.isdigit() else None,
                    created_by=request.user
                )
            messages.success(request, 'Songs imported successfully!')
            return redirect('bands:band_detail', band_id=band.id)
        except Exception as e:
            messages.error(request, f'Error processing file: {e}')
            return redirect('songs:upload_csv', band_id=band.id)

    return render(request, 'songs/upload_csv.html', {'band': band})