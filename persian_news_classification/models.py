from django.db import models


class Category(models.Model):
    title = models.CharField(
        max_length=128,
    )


class News(models.Model):
    titr = models.CharField(
        max_length=512,
    )
    context = models.TextField(

    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    vector = models.JSONField(

    )
    refrence = models.CharField(
        max_length=128,
    )