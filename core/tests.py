from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from bands.models import Band
from core.models import Event, SetList
from songs.models import Song


class DashboardRoutingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dashboard_user", password="testpass123")
        self.band = Band.objects.create(name="Dashboard Band")
        self.band.members.add(self.user)
        self.client.force_login(self.user)

    def test_dashboard_renders_for_authenticated_user(self):
        response = self.client.get(reverse("core:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/dashboard.html")
        self.assertContains(response, "Dashboard Band")


class BreadcrumbDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="crumbs", password="testpass123")
        self.band = Band.objects.create(name="Breadcrumb Band")
        self.band.members.add(self.user)
        self.song = Song.objects.create(
            title="Ocean Avenue",
            artist="Yellowcard",
            created_by=self.user,
            band=self.band,
        )
        self.setlist = SetList.objects.create(name="Friday Night", band=self.band)
        self.client.force_login(self.user)

    def _crumb_names(self, response):
        if isinstance(response.context, dict):
            return [crumb["name"] for crumb in response.context["breadcrumbs"]]

        for ctx in reversed(response.context):
            if "breadcrumbs" in ctx:
                return [crumb["name"] for crumb in ctx["breadcrumbs"]]

        self.fail("Breadcrumbs not found in response context")

    def test_song_view_breadcrumbs_include_songs_section(self):
        response = self.client.get(reverse("songs:song_detail", kwargs={"song_id": self.song.id}))
        names = self._crumb_names(response)
        self.assertEqual(names, ["Home", self.band.name, "Songs", f"Song: {self.song.title}"])

    def test_song_edit_breadcrumbs_include_edit_suffix(self):
        response = self.client.get(reverse("songs:edit_song", kwargs={"song_id": self.song.id}))
        names = self._crumb_names(response)
        self.assertEqual(names, ["Home", self.band.name, "Songs", f"Song: {self.song.title}", "Edit"])

    def test_setlist_view_breadcrumbs_include_setlists_section(self):
        response = self.client.get(reverse("core:view_setlist", kwargs={"setlist_id": self.setlist.id}))
        names = self._crumb_names(response)
        self.assertEqual(names, ["Home", self.band.name, "Set Lists", f"Set List: {self.setlist.name}"])

    def test_setlist_edit_breadcrumbs_include_edit_suffix(self):
        response = self.client.get(reverse("core:edit_setlist", kwargs={"setlist_id": self.setlist.id}))
        names = self._crumb_names(response)
        self.assertEqual(names, ["Home", self.band.name, "Set Lists", f"Set List: {self.setlist.name}", "Edit"])


class EventCalendarRedirectTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="richard", password="testpass123")
        self.band = Band.objects.create(name="Test Band")
        self.band.members.add(self.user)
        self.client.force_login(self.user)

    def test_create_event_redirects_to_band_calendar_month(self):
        response = self.client.post(
            reverse("core:create_event", kwargs={"band_id": self.band.id}),
            {
                "title": "Album Release Show",
                "type": Event.EVENT_TYPE_CONCERT,
                "date": "2026-04-05",
                "time": "20:30",
                "venue": "",
                "location": "Main Street Club",
                "door_price": "15.00",
                "notes": "Bring merch.",
            },
        )

        event = Event.objects.get(title="Album Release Show")
        self.assertRedirects(
            response,
            f"{reverse('bands:band_calendar', kwargs={'band_id': self.band.id})}?year=2026&month=4",
            fetch_redirect_response=False,
        )
        self.assertEqual(event.band, self.band)
        self.assertEqual(event.created_by, self.user)

    def test_edit_event_redirects_to_updated_calendar_month(self):
        event = Event.objects.create(
            band=self.band,
            title="Rehearsal",
            type=Event.EVENT_TYPE_GENERIC,
            date="2026-04-05",
            time="19:00",
            location="Practice Space",
            created_by=self.user,
        )

        response = self.client.post(
            reverse("core:edit_event", kwargs={"event_id": event.id}),
            {
                "title": "Rescheduled Rehearsal",
                "type": Event.EVENT_TYPE_GENERIC,
                "date": "2026-06-12",
                "time": "18:00",
                "venue": "",
                "location": "Practice Space",
                "door_price": "",
                "notes": "",
            },
        )

        event.refresh_from_db()
        self.assertRedirects(
            response,
            f"{reverse('bands:band_calendar', kwargs={'band_id': self.band.id})}?year=2026&month=6",
            fetch_redirect_response=False,
        )
        self.assertEqual(event.title, "Rescheduled Rehearsal")

    def test_delete_event_redirects_to_band_calendar_month(self):
        event = Event.objects.create(
            band=self.band,
            title="Festival",
            type=Event.EVENT_TYPE_CONCERT,
            date="2026-07-20",
            time="21:00",
            location="Downtown Stage",
            created_by=self.user,
        )

        response = self.client.post(reverse("core:delete_event", kwargs={"event_id": event.id}))

        self.assertRedirects(
            response,
            f"{reverse('bands:band_calendar', kwargs={'band_id': self.band.id})}?year=2026&month=7",
            fetch_redirect_response=False,
        )
        self.assertFalse(Event.objects.filter(id=event.id).exists())
