from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Location


class TestViews(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        # this will let us bypass the login requirements
        self.client = Client()

        self.location1 = Location.objects.create(
            city="Santiago",
            country="Chile",
            latitude=-33.45,
            longitude=-70.67,
        )

        self.location2 = Location.objects.create(
            city="Buenos Aires",
            country="Argentina",
            latitude=-34.60,
            longitude=-58.38,
        )

    def login(self):
        self.client.force_login(self.user)

    def test_list_locations_view__success(self):
        """
        success test: Test that the location list view returns the correct locations in context,
        verifying that for each location a card with an hx-target containing its id is rendered.
        """
        self.login()
        url = reverse("list_locations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        for location in Location.objects.all():
            expected_target = f'hx-target="#weather-data-{location.id}"'
            self.assertIn(expected_target, content)

    def test_list_locations_view__not_logged_in(self):
        """
        failure test: Test that the location list view returns a 302 redirect when the user is not logged in
        """
        url = reverse("list_locations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
