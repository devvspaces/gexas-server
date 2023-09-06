from django.db import models
from uuid import uuid4
from django.utils.safestring import mark_safe
from django.urls import reverse


class Graph(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    tablanotas = models.TextField()
    tablaaudit = models.TextField()

    def __str__(self):
        return str("Graph " + str(self.id))

    @property
    def safe_tablanotas(self):
        return mark_safe(self.tablanotas)

    @property
    def safe_tablaaudit(self):
        return mark_safe(self.tablaaudit)

    def get_absolute_url(self):
        return reverse('main:view', kwargs={'graph_id': str(self.id)})
