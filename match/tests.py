import uuid
import datetime
import io
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.html import strip_tags
from .models import Player, Competition, Match
from .forms import PlayerForm, CompetitionForm, MatchForm


def get_test_image_file(name='test_logo.png', size=(10, 10), color='blue'):
    f = io.BytesIO()
    image = Image.new('RGB', size, color)
    image.save(f, 'PNG')
    f.seek(0)
    return SimpleUploadedFile(name, f.getvalue(), content_type='image/png')


class ModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.competition = Competition.objects.create(
            name="Test League",
            begin_date=datetime.date(2025, 1, 1),
            end_date=datetime.date(2025, 12, 31)
        )

        cls.player = Player.objects.create(
            name="Test Player",
            established_date=datetime.date(2000, 1, 1)
        )

    def test_create_player(self):
        player = Player.objects.get(id=self.player.id)
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(Player.objects.count(), 1)

    def test_create_competition(self):
        comp = Competition.objects.get(id=self.competition.id)
        self.assertEqual(comp.name, "Test League")
        self.assertEqual(Competition.objects.count(), 1)

    def test_create_match(self):
        match = Match.objects.create(
            competition=self.competition,
            begin_datetime=datetime.datetime(
                2025, 1, 15, 12, 0, tzinfo=datetime.timezone.utc),
            end_datetime=datetime.datetime(
                2025, 1, 15, 14, 0, tzinfo=datetime.timezone.utc)
        )
        match.players.add(self.player)

        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(match.competition.name, "Test League")
        self.assertEqual(match.players.count(), 1)
        self.assertEqual(match.players.first().name, "Test Player")


class FormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.competition = Competition.objects.create(
            name="Test League",
            begin_date=datetime.date(2025, 1, 1),
            end_date=datetime.date(2025, 12, 31)
        )
        cls.player = Player.objects.create(
            name="Test Player",
            established_date=datetime.date(2000, 1, 1)
        )

    def test_player_form_valid(self):
        data = {
            "name": "Valid Player",
            "established_date": "2010-01-01",
            "is_defunct": False
        }
        form = PlayerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_player_form_clean_name(self):
        data = {
            "name": "<b>Bold Player</b>",
            "established_date": "2010-01-01",
        }
        form = PlayerForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], "Bold Player")

    def test_competition_form_valid(self):
        data = {
            "name": "Valid Comp",
            "begin_date": "2025-01-01",
            "end_date": "2025-01-02",
        }
        form = CompetitionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_competition_form_invalid_dates(self):
        data = {
            "name": "Invalid Comp",
            "begin_date": "2025-01-05",
            "end_date": "2025-01-01",
        }
        form = CompetitionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("End date must be greater", form.errors["__all__"][0])

    def test_match_form_valid(self):
        data = {
            "competition": self.competition.id,
            "players": [self.player.id],
            "begin_datetime": "2025-01-15 12:00:00",
            "end_datetime": "2025-01-15 14:00:00",
        }
        form = MatchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_match_form_invalid_datetimes(self):
        data = {
            "competition": self.competition.id,
            "players": [self.player.id],
            "begin_datetime": "2025-01-15 14:00:00",
            "end_datetime": "2025-01-15 12:00:00",
        }
        form = MatchForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn(
            "End match time must be greater",
            form.errors["__all__"][0])


class BasicMatchAPIViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.normal_user = User.objects.create_user(
            username="user", password="password")

        cls.admin_user = User.objects.create_user(
            username="admin", password="password")
        admin_perm, _ = Permission.objects.get_or_create(
            codename='admin',
            content_type=ContentType.objects.filter(app_label='main').first()
        )
        cls.admin_user.user_permissions.add(admin_perm)

        cls.player1 = Player.objects.create(
            name="Player to Update",
            established_date=datetime.date(2000, 1, 1)
        )
        cls.comp1 = Competition.objects.create(
            name="Comp to Update",
            begin_date=datetime.date(2025, 1, 1),
            end_date=datetime.date(2025, 12, 31)
        )
        cls.match1 = Match.objects.create(
            competition=cls.comp1,
            begin_datetime=datetime.datetime(
                2025, 2, 1, 12, 0, tzinfo=datetime.timezone.utc),
            end_datetime=datetime.datetime(
                2025, 2, 1, 14, 0, tzinfo=datetime.timezone.utc)
        )
        cls.match1.players.add(cls.player1)

        cls.create_player_url = reverse("api_create_player")
        cls.update_comp_url = reverse(
            "api_update_competition", args=[
                cls.comp1.id])
        cls.delete_match_url = reverse(
            "api_delete_match", args=[cls.match1.id])

    def setUp(self):
        self.client = Client()

    def test_api_permission_denied_not_logged_in(self):
        response = self.client.post(self.create_player_url, data={})
        self.assertEqual(response.status_code, 302)
        self.assertIn('', response.url)

    def test_api_permission_denied_not_admin(self):
        self.client.login(username="user", password="password")
        response = self.client.post(self.create_player_url, data={})
        self.assertEqual(response.status_code, 302)

    def test_api_method_not_allowed_get_on_post_endpoint(self):
        self.client.login(username="admin", password="password")
        response = self.client.get(self.create_player_url)
        self.assertEqual(response.status_code, 405)

    def test_api_create_player_success(self):
        self.client.login(username="admin", password="password")

        logo_file = get_test_image_file()

        data = {
            "name": "New Player",
            "established_date": "2020-01-01",
            "is_defunct": False,
            "logo": logo_file
        }
        response = self.client.post(self.create_player_url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Player.objects.filter(name="New Player").exists())
        new_player = Player.objects.get(name="New Player")
        self.assertIn(str(new_player.id), new_player.logo.name)

    def test_api_create_player_invalid_data(self):
        self.client.login(username="admin", password="password")

        data = {"is_defunct": False}

        response = self.client.post(self.create_player_url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Player.objects.count(), 1)

    def test_api_update_competition_success(self):
        self.client.login(username="admin", password="password")

        data = {
            "name": "Updated Competition Name",
            "begin_date": self.comp1.begin_date,
            "end_date": self.comp1.end_date,
        }

        print(self.update_comp_url)
        response = self.client.post(self.update_comp_url, data=data)

        self.assertEqual(response.status_code, 201)
        self.comp1.refresh_from_db()
        self.assertEqual(self.comp1.name, "Updated Competition Name")

    def test_api_update_competition_invalid_dates(self):
        self.client.login(username="admin", password="password")

        data = {
            "name": "Updated Name",
            "begin_date": "2025-01-10",
            "end_date": "2025-01-01",
        }

        response = self.client.post(self.update_comp_url, data=data)

        self.assertEqual(response.status_code, 400)
        self.comp1.refresh_from_db()
        self.assertEqual(
            self.comp1.name,
            "Comp to Update")

    def test_api_update_competition_not_found(self):
        self.client.login(username="admin", password="password")

        bad_uuid = uuid.uuid4()
        bad_url = reverse("api_update_competition", args=[bad_uuid])
        data = {
            "name": "Name",
            "begin_date": "2025-01-01",
            "end_date": "2025-01-10",
        }

        response = self.client.post(bad_url, data=data)
        self.assertEqual(response.status_code, 404)

    def test_api_delete_match_success(self):
        self.client.login(username="admin", password="password")

        self.assertTrue(Match.objects.filter(id=self.match1.id).exists())

        response = self.client.post(self.delete_match_url)

        self.assertEqual(response.status_code, 202)
        self.assertFalse(Match.objects.filter(id=self.match1.id).exists())

    def test_api_delete_match_not_found(self):
        self.client.login(username="admin", password="password")

        bad_uuid = uuid.uuid4()
        bad_url = reverse("api_delete_match", args=[bad_uuid])

        response = self.client.post(bad_url)
        self.assertEqual(response.status_code, 404)
