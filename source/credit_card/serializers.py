from datetime import date
from calendar import monthrange
from rest_framework.serializers import ModelSerializer
from django.core.exceptions import ValidationError
from credit_card.models import CreditCard
from creditcard import CreditCard as CreditCardValidator
from credit_card.exceptions import DateFormatException


class CreditCardSerializer(ModelSerializer):
    class Meta:
        model = CreditCard
        read_only_fields = ("id", "brand")
        fields = ("id", "exp_date", "holder", "number", "cvv", "brand")

    def validate_number(self, value):
        if not CreditCardValidator(value).is_valid():
            raise ValidationError("invalid number")
        return value

    def validate_cvv(self, value):
        if value and len(str(value)) not in (3, 4):
            raise ValidationError("must be between 3 and 4 characters")
        return value

    def validate_exp_date(self, value):
        if value < date.today():
            raise ValidationError("cannot be less than today's date")
        return value

    def create(self, validated_data):
        brand = self._get_brand(validated_data["number"])
        credit_card = CreditCard.objects.create(
            brand=brand, client=self.context["user"], **validated_data
        )
        return credit_card

    def to_internal_value(self, data):
        data["exp_date"] = self._format_exp_date_to_date(data["exp_date"])
        return super(CreditCardSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["exp_date"] = self._format_date_to_exp_date(data["exp_date"])
        return data

    def _get_brand(self, number):
        return CreditCardValidator(number).get_brand()

    def _format_exp_date_to_date(self, exp_date):
        try:
            month, year = exp_date.split("/")
            last_day = monthrange(int(year), int(month))[1]
            date = "-".join([year, month, str(last_day)])
            return date
        except ValueError:
            raise DateFormatException

    def _format_date_to_exp_date(self, exp_date):
        try:
            year, month, _ = exp_date.split("-")
            date = "/".join([month, year])
            return date
        except ValueError:
            raise DateFormatException
