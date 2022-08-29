from django.db.models import JSONField
from django.db import models


class Statements(models.Model):
    statement_title = models.CharField(null=True,max_length=300)
    statement_json = JSONField()

