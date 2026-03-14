from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from bands.models import Band


class BandDetailCalendarTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="richard", password="testpass123")
        self.band = Band.objects.create(name="Sunday Set")
        self.band.members.add(self.user)
        self.client.login(username="richard", password="testpass123")

    def test_band_detail_calendar_starts_on_sunday_and_uses_partial_assets(self):
        response = self.client.get(reverse("bands:band_detail", args=[self.band.id]), {"year": 2025, "month": 10})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bands/band_detail.html")
        self.assertTemplateUsed(response, "bands/_calendar_tab.html")
        self.assertContains(response, 'src="/static/js/band_detail.js"')
        self.assertContains(response, "<th scope=\"col\">Sun</th>", html=True)

        context = response.context[-1] if hasattr(response.context, "__getitem__") and not isinstance(response.context, dict) else response.context
        first_week = context["calendar_weeks"][0]
        self.assertEqual(first_week[0]["date"], date(2025, 9, 28))
        self.assertEqual(first_week[0]["date"].weekday(), 6)
        self.assertEqual(first_week[-1]["date"], date(2025, 10, 4))
