from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CompaniesModel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.PROTECT)
