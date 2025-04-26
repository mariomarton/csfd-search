from django.db import IntegrityError
from django.test import TestCase
from core.models import Actor, Film


class ActorModelTest(TestCase):
    def test_create_and_str(self):
        actor = Actor.objects.create(csfd_id=123, name="Janko Mrkvicka")
        self.assertEqual(str(actor), "Janko Mrkvicka")

    def test_unique_csfd_id(self):
        Actor.objects.create(csfd_id=123, name="Janko Mrkvicka")
        with self.assertRaises(IntegrityError):
            Actor.objects.create(csfd_id=123, name="Ferko Mrkvicka")


class FilmModelTest(TestCase):
    def setUp(self):
        self.actor1 = Actor.objects.create(csfd_id=1, name="actor1")
        self.actor2 = Actor.objects.create(csfd_id=2, name="actor2")

    def test_create_and_str(self):
        film = Film.objects.create(csfd_id=10, title="Gone in 60 seconds")
        self.assertEqual(str(film), "Gone in 60 seconds")

    def test_m2m_relationship(self):
        film = Film.objects.create(csfd_id=11, title="Interstellar")

        # link actors
        film.actors.add(self.actor1, self.actor2)
        self.assertCountEqual(film.actors.all(), [self.actor1, self.actor2])

        # reverse lookup
        self.assertIn(film, self.actor1.films.all())
        self.assertIn(film, self.actor2.films.all())

        # remove an actor
        film.actors.remove(self.actor1)
        self.assertEqual(film.actors.count(), 1)
        self.assertEqual(film.actors.first(), self.actor2)

        # reverse lookup after removal
        self.assertNotIn(film, self.actor1.films.all())
        self.assertIn(film, self.actor2.films.all())
