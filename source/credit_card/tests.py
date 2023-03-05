import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from credit_card.models import CreditCard
from unittest.mock import patch
from creditcard import CreditCard as CreditCardValidator
from unittest.mock import Mock


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
            "exp_date": "10/2222",
            "holder": "Fulano",
            "number": "0000000000000001",
            "cvv": 123,
            "brand": "BR",
        }

@pytest.fixture()
def credit_card(user, valid_data):
    valid_data["exp_date"] = "2222-10-10"
    return CreditCard.objects.create(client=user,brand="BR",**valid_data)

@pytest.fixture()
def url_detail(credit_card):
    return reverse("credit_card:credit_card-detail", kwargs={"pk": credit_card.id})

@pytest.mark.django_db()
class TestCreditCard:

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=True))
    @patch.object(CreditCardValidator, "get_brand", Mock(return_value="BR"))
    def test_create_credit_card(self, client, valid_data, data_return):
        # validar a data
        # temque verificar se a data do cartao e maior que a data atual
        # temque armasenar no bando como yyyy-mm-(utimo dia do mes)
        # ele vai receber os dados no formato mm-yyyy

        # holder e um compo string, maios de 2 caracteris e obrigatorio
        # number

        # cvv e um campo nao obrigatorio
        # mais se tiver quem que ser numerico
        # e com o valor entre 3 a 4

        # brand
        # e o valor que o validador do munero passa
        # nao e necessario colocar na request
        # so vemos no retorno (get)
        url = reverse("credit_card:credit_card-list")
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 200
        assert response_data.json() == data_return

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=True))
    @patch.object(CreditCardValidator, "get_brand", Mock(return_value="BR"))
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
    @patch.object(CreditCardValidator, "get_brand", Mock(return_value="BR"))
    def test_exp_date_data_less_than_current(self, url, client, valid_data):
        valid_data["exp_date"] = "10/1990"
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {"exp_date": ["cannot be less than today's date"]}

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=True))
    @patch.object(CreditCardValidator, "get_brand", Mock(return_value="BR"))
    def test_holder_with_wrong_format(self, url, client, valid_data):
        # valor menor que 2 caracteris
        # passa valor nao instring
        # sem valor
        valid_data["holder"] = "a"
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {'holder': ['Ensure this field has at least 2 characters.']}

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=False))
    @patch.object(CreditCardValidator, "get_brand", Mock(return_value="BR"))
    def test_invalid_card_number(self, url, client, valid_data):
        # vai validar se o numero do cartao de credito e valido
        # se nao for valido deve retornar uma mensagem de erro
        # sem numero
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {'number': ['invalid number']}

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=True))
    @patch.object(CreditCardValidator, "get_brand", Mock(return_value="BR"))
    def test_invalid_cvv(self, url, client, valid_data):
        # vai validar se o numero do cartao de credito e valido
        # se nao for valido deve retornar uma mensagem de erro
        # sem numero
        valid_data["cvv"] = 1
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {'cvv': ['must be between 3 and 4 characters']}

        valid_data["cvv"] = 11111
        response_data = client.post(url, data=valid_data, format="json")
        assert response_data.status_code == 400
        assert response_data.json() == {'cvv': ['must be between 3 and 4 characters']}

    @pytest.mark.usefixtures("credit_card")
    def test_datail_credit_card(self, url_detail, client, data_return):
        response_data = client.get(url_detail, format="json")
        assert response_data.status_code == 200
        assert response_data.json() == data_return

    @pytest.mark.usefixtures("credit_card")
    def test_get_list_credit_card(self, url, client, data_return):
        response_data = client.get(url, format="json")
        assert response_data.status_code == 200
        assert response_data.json() == [data_return]
