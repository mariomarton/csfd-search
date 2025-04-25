from django.db import models


class Actor(models.Model):
    id = models.AutoField(primary_key=True)  # auto-generated if omitted, made explicit here for readability
    csfd_id = models.IntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Film(models.Model):
    id = models.AutoField(primary_key=True)  # auto-generated if omitted, made explicit here for readability
    csfd_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255)
    actors = models.ManyToManyField(Actor, related_name='films')

    def __str__(self):
        return self.title
