import pytest

from django.conf import settings
from django.test import Client
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.app.models import ErModel


User = get_user_model()


def get_model_changelist_url(model):
    opts = model._meta
    return reverse(
        "admin:%s_%s_changelist"
        % (
            opts.app_label,
            opts.model_name,
        ),
        current_app=admin.AdminSite().name,
    )


@pytest.mark.django_db
def test_changelist(requests_mock):

    requests_mock.get(
        settings.TEST_EXTERNAL_SERVICE_URL,
        json={
            "total": 1000,
            "items": [
                {"id": 1, "key": "somekey", "value": "somevalue"},
            ],
        },
    )

    admin_user = User.objects.create(
        username="admin",
        is_superuser=True,
        is_staff=True,
    )

    c = Client()
    c.force_login(admin_user)

    response = c.get(get_model_changelist_url(ErModel))
    assert response.status_code == 200

    content = response.content.decode()
    assert "somekey" in content

    # check paginator
    assert "1000 {}".format(ErModel._meta.verbose_name) in content
