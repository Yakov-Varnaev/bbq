from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CompanyModel(models.Model):

    # class Meta:
    #     verbose_name = 'Company'
    #     verbose_name_plural = 'Companies'

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='companies', on_delete=models.PROTECT)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
