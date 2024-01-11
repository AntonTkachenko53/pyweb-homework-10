from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=100, null=False, unique=True)
    born_date = models.CharField(max_length=50, null=False)
    born_location = models.CharField(null=False)
    description = models.TextField()

    def __str__(self):
        return f"{self.fullname}"
