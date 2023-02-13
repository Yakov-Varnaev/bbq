from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='companies', on_delete=models.PROTECT)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)


class CompanyPoint(models.Model):
    """
    This model represents one object of a company.
    E.g. one barber shop from the whole network.
    """

    address = models.CharField(max_length=255)
    company = models.ForeignKey(Company, related_name='points', on_delete=models.CASCADE,)
