import requests

from django.conf import settings
from django.db import models
from django.contrib import admin

from dadfes.admin import DfesAdminModelMixin


class ErModel(models.Model):
    id = models.IntegerField("Id", primary_key=True)
    key = models.TextField("Key")
    value = models.TextField("Value")

    class Meta:
        managed = False
        verbose_name = "External Resource Model"


class ErModelAdmin(DfesAdminModelMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "key",
        "value",
    )

    def get_list(self, request, offset, limit):

        response = requests.get(settings.TEST_EXTERNAL_SERVICE_URL)

        data = response.json()

        items = list(map(lambda i: ErModel(**i), data.get("items") or []))

        return {
            "total": data.get("total") or 0,
            "items": items,
        }


admin.site.register(ErModel, ErModelAdmin)
