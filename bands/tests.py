from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from bands.models import Band, BandInvite


class BandCalendarPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="richard", password="testpass123")
        self.band = Band.objects.create(name="Sunday Set")
        self.band.members.add(self.user)
        self.client.login(username="richard", password="testpass123")

    def test_band_calendar_starts_on_sunday(self):
        response = self.client.get(reverse("bands:band_calendar", args=[self.band.id]), {"year": 2025, "month": 10})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bands/band_calendar.html")
        self.assertTemplateUsed(response, "bands/_calendar_tab.html")
        self.assertContains(response, "<th scope=\"col\">Sun</th>", html=True)

        context = response.context[-1] if hasattr(response.context, "__getitem__") and not isinstance(response.context, dict) else response.context
        first_week = context["calendar_weeks"][0]
        self.assertEqual(first_week[0]["date"], date(2025, 9, 28))
        self.assertEqual(first_week[0]["date"].weekday(), 6)
        self.assertEqual(first_week[-1]["date"], date(2025, 10, 4))

    def test_navbar_shows_selected_band_and_band_page_links(self):
        response = self.client.get(reverse("bands:band_calendar", args=[self.band.id]))

        self.assertContains(response, self.band.name)
        self.assertContains(response, reverse("bands:band_songs", args=[self.band.id]))
        self.assertContains(response, reverse("bands:band_setlists", args=[self.band.id]))
        self.assertContains(response, reverse("bands:band_notes", args=[self.band.id]))

    def test_band_subpages_have_expected_breadcrumb_label(self):
        cases = [
            ("bands:band_calendar", "Calendar"),
            ("bands:band_songs", "Songs"),
            ("bands:band_setlists", "Set Lists"),
            ("bands:band_notes", "Notes"),
        ]

        for route_name, expected_label in cases:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name, args=[self.band.id]))
                self.assertEqual(response.status_code, 200)

                context = response.context[-1] if hasattr(response.context, "__getitem__") and not isinstance(response.context, dict) else response.context
                breadcrumb_names = [crumb["name"] for crumb in context["breadcrumbs"]]

                self.assertEqual(breadcrumb_names[0], "Home")
                self.assertIn(self.band.name, breadcrumb_names)
                self.assertEqual(breadcrumb_names[-1], expected_label)


class BandManageActionsTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="testpass123")
        self.member = User.objects.create_user(username="member", password="testpass123")
        self.invited = User.objects.create_user(username="invited", password="testpass123")
        self.band = Band.objects.create(name="Action Band")
        self.band.members.add(self.owner, self.member)
        self.invite = BandInvite.objects.create(
            band=self.band,
            invited_user=self.invited,
            invited_by=self.owner,
            accepted=False,
        )
        self.client.force_login(self.owner)

    def test_remove_member_post_removes_member(self):
        response = self.client.post(
            reverse("bands:remove_member", kwargs={"band_id": self.band.id, "user_id": self.member.id})
        )

        self.assertRedirects(response, reverse("bands:band_manage", kwargs={"band_id": self.band.id}))
        self.assertFalse(self.band.members.filter(id=self.member.id).exists())

    def test_delete_invite_post_removes_pending_invite(self):
        response = self.client.post(
            reverse("bands:delete_invite", kwargs={"band_id": self.band.id, "invite_id": self.invite.id})
        )

        self.assertRedirects(response, reverse("bands:band_manage", kwargs={"band_id": self.band.id}))
        self.assertFalse(BandInvite.objects.filter(id=self.invite.id).exists())
