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

    // Right-align the built-in DataTables filter container.
    $('#songsTable_filter').addClass('text-end').removeClass('dataTables_filter');;
    // Make DataTables search input visually match Bootstrap inputs.
    $('#songsTable_filter input[type="search"]').addClass('form-control d-inline-block w-100').removeClass('form-control-sm');
    //add a placeholder to the search input
    $('#songsTable_filter input[type="search"]').attr('placeholder', 'Search songs...');
    //remove the default label for the search input
    $('#songsTable_filter label').addClass('w-100').contents().filter(function() {
      return this.nodeType === Node.TEXT_NODE;
    }).remove();

    $('#songsTable_wrapper > div:nth-child(1) > div:nth-child(1)').remove();
    $('#songsTable_wrapper > div:nth-child(1) > div').removeClass('col-md-6').addClass('col-md-12');

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
    const page = document.getElementById('band-songs-page');
    if (!page) {
      return;
    }

    initialiseSongsTable();
    initialiseNoteDeletion(page);
  });
})();
