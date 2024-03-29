from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

import pytest

from credit_card.models import CreditCard
from creditcard import CreditCard as CreditCardValidator
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture()
def user():
    return get_user_model().objects.create_superuser("lucas", None, "123456")


@pytest.fixture()
def client(user):
    token = Token.objects.get(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return client


@pytest.fixture()
def url():
    return reverse("credit_card:credit_card-list")


@pytest.fixture()
def valid_data():
    return {
        "exp_date": "10/2222",
        "holder": "Fulano",
        "number": "0000000000000001",
        "cvv": 123,
    }


@pytest.fixture()
def data_return():
    return {
        "id": 1,
        "exp_date": "10/2222",
        "holder": "Fulano",
        "number": "0000000000000001",
        "cvv": 123,
        "brand": "BR",
    }


@pytest.fixture()
def credit_card(user, valid_data):
    valid_data["exp_date"] = "2222-10-10"
    return CreditCard.objects.create(client=user, brand="BR", **valid_data)


@pytest.fixture()
def url_detail(credit_card):
    return reverse("credit_card:credit_card-detail", kwargs={"pk": credit_card.id})


@pytest.mark.django_db()
class TestCreditCard:
    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=True))
    def test_create_credit_card(self, client, valid_data, data_return):
        url = reverse("credit_card:credit_card-list")
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 200
        assert response_data.json() == data_return

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=True))
    def test_exp_date_with_wrong_format(self, url, client, valid_data):
        valid_data["exp_date"] = "2025/10"
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {"detail": "date is formatted wrong"}

        valid_data["exp_date"] = "2025/13"
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {"detail": "date is formatted wrong"}

        valid_data["exp_date"] = "9999/10"
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {"detail": "date is formatted wrong"}

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=True))
    def test_exp_date_data_less_than_current(self, url, client, valid_data):
        valid_data["exp_date"] = "10/1990"
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {"exp_date": ["cannot be less than today's date"]}

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=True))
    def test_holder_with_wrong_format(self, url, client, valid_data):
        valid_data["holder"] = "a"
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {"holder": ["Ensure this field has at least 2 characters."]}

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=False))
    def test_invalid_card_number(self, url, client, valid_data):
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {"number": ["invalid number"]}

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=True))
    def test_invalid_cvv(self, url, client, valid_data):
        valid_data["cvv"] = 1
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {"cvv": ["must be between 3 and 4 characters"]}

        valid_data["cvv"] = 11111
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {"cvv": ["must be between 3 and 4 characters"]}

    @pytest.mark.usefixtures("credit_card")
    def test_datail_credit_card(self, url_detail, client, data_return):
        response_data = client.get(url_detail, format="json")
        assert response_data.status_code == 200
        assert response_data.json()["holder"] == data_return["holder"]

    @pytest.mark.usefixtures("credit_card")
    def test_get_list_credit_card(self, url, client, data_return):
        response_data = client.get(url, format="json")
        assert response_data.status_code == 200
        assert response_data.json()[0]["holder"] == data_return["holder"]

    def test_command(self):
        call_command("seed", "--create-superuser")
        assert len(get_user_model().objects.all()) == 1
