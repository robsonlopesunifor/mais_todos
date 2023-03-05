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
def client():
    user = get_user_model().objects.create_superuser("lucas", None, "123456")
    token = Token.objects.get(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return client

@pytest.fixture()
def valid_data():
    return {
            "exp_date": "10/2025",
            "holder": "Fulano",
            "number": "0000000000000001",
            "cvv": "123",
        }

@pytest.fixture()
def data_return():
    return {
            "exp_date": "10/2025",
            "holder": "Fulano",
            "number": "0000000000000001",
            "cvv": "123",
            "brand": "BR",
        }


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

        import pdb; pdb.set_trace()
        assert response_data.status_code == 200
        assert response_data.json() == data_return

    @patch.object(CreditCardValidator, "is_valid", Mock(return_value=True))
    def _test_create_credit_card_with_wrong_date(self):
        # vai passar dados errados para a data
        # deve receber uma mensagem de erro informando onde foi
        # parra yyyy-mm,
        # mes que nao existe
        # anos que nao existe
        # data a baixo da tata atual
        # sem data

        data = self.data.copy()
        data["exp_date"] = "2025/10"

        response_data = self.client.post(self.url, data=data, format="json")

        self.assertEqual(response_data.status_code, 400)
        self.assertEqual(response_data.json(), {"detail": "date is formatted wrong"})

        data = self.data.copy()
        data["exp_date"] = "2025/13"

        response_data = self.client.post(self.url, data=data, format="json")

        self.assertEqual(response_data.status_code, 400)
        self.assertEqual(response_data.json(), {"detail": "date is formatted wrong"})

        data = self.data.copy()
        data["exp_date"] = "9999/10"

        response_data = self.client.post(self.url, data=data, format="json")

        self.assertEqual(response_data.status_code, 400)
        self.assertEqual(response_data.json(), {"detail": "date is formatted wrong"})

        data = self.data.copy()
        data["exp_date"] = "10/1990"

        response_data = self.client.post(self.url, data=data, format="json")

        self.assertEqual(response_data.status_code, 400)
        self.assertEqual(
            response_data.json(), {"exp_date": ["cannot be less than today's date"]}
        )

        data = self.data.copy()
        data["exp_date"] = None

        response_data = self.client.post(self.url, data=data, format="json")

        self.assertEqual(response_data.status_code, 400)
        self.assertEqual(
            response_data.json(), {"exp_date": ["cannot be less than today's date"]}
        )

    def _test_create_credit_card_with_wrong_holder(self):
        # valor menor que 2 caracteris
        # passa valor nao instring
        # sem valor
        pass

    def _test_create_credit_card_with_wrong_number(self):
        # vai validar se o numero do cartao de credito e valido
        # se nao for valido deve retornar uma mensagem de erro
        # sem numero
        pass

    def _test_create_credit_card_with_wrong_cvv(self):
        # vai validar se o numero do cartao de credito e valido
        # se nao for valido deve retornar uma mensagem de erro
        # sem numero
        pass

    def _test_datail_credit_card(self):
        # deve retornar os dados no fomato pre defininido no setup
        # retornar 200
        # precisa passar o token do usuario
        data = {
            "exp_date": "2025-10-10",
            "holder": "Fulano",
            "number": "0000000000000001",
            "cvv": "123",
        }

        credit_card = CreditCard.objects.create(brand="BR", client=self.user, **data)
        url = reverse("credit_card:credit_card-detail", kwargs={"pk": credit_card.id})
        response_data = self.client.get(url, data=self.data, format="json")

        self.assertEqual(response_data.status_code, 200)
        self.assertEqual(response_data.json(), self.data_return)

    def _test_get_list_credit_card(self):
        # retorna a lista de cartoes de credito
        # voce precisa criar um factory para gerar os cartoes de credito
        # compara com as resposta predefinida no setup
        pass
