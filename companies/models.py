from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CompaniesModel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.PROTECT)
