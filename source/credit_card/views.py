from calendar import monthrange
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from credit_card.serializers import CreditCardSerializer
from credit_card.exceptions import DateFormatException
from credit_card.models import CreditCard
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404


class CreditcardViewSet(viewsets.ViewSet):
    serializer_class = CreditCardSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        creditcard = get_object_or_404(CreditCard, id=pk)
        data = CreditCardSerializer(creditcard).data
        data["exp_date"] = self._format_date_to_exp_date(data["exp_date"])
        return Response(data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request):
        serializer = CreditCardSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)