(function () {
  function getCookie(name) {
    const cookieValue = document.cookie
      .split(';')
      .map((cookie) => cookie.trim())
      .find((cookie) => cookie.startsWith(`${name}=`));

    return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : null;
  }

  function initialiseSongsTable() {
    const songsTable = $('#songsTable');
    const artistFilter = $('#artistFilter');

    if (!songsTable.length || !$.fn.DataTable) {
      return;
    }

    const table = songsTable.DataTable({
      paging: false,
      info: false,
      order: [[0, 'asc']],
    });

    if (artistFilter.length) {
      artistFilter.on('change', function () {
        table.column(1).search(this.value).draw();
      });
    }
  }

  function initialiseNoteDeletion(page) {
    const deleteNoteUrl = page.dataset.deleteNoteUrl;
    if (!deleteNoteUrl) {
      return;
    }

    document.addEventListener('click', function (event) {
      const button = event.target.closest('.delete-note-btn');
      if (!button) {
        return;
      }

      if (!window.confirm('Delete this note?')) {
        return;
      }

      const noteItem = button.closest('.list-group-item');
      const formData = new URLSearchParams({ note_id: button.dataset.noteId });

      fetch(deleteNoteUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
          'X-CSRFToken': getCookie('csrftoken') || '',
        },
        body: formData.toString(),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Failed to delete note.');
          }
          return response.json();
        })
        .then((data) => {
          if (!data.success) {
            throw new Error(data.error || 'Failed to delete note.');
          }

          if (noteItem) {
            noteItem.remove();
          }
        })
        .catch((error) => {
          window.alert(error.message);
        });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    const page = document.getElementById('band-detail-page');
    if (!page) {
      return;
    }

    initialiseSongsTable();
    initialiseNoteDeletion(page);
  });
})();
