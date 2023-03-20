from django.db import transaction
from django.shortcuts import get_object_or_404

from credit_card.models import CreditCard
from credit_card.serializers import CreditCardSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


class CreditcardViewSet(viewsets.ViewSet):
    serializer_class = CreditCardSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        creditcard = get_object_or_404(CreditCard, id=pk)
        data = CreditCardSerializer(creditcard).data
        return Response(data, status=status.HTTP_200_OK)

    def list(self, request):
        creditcard = CreditCard.objects.all()
        data = CreditCardSerializer(creditcard, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request):
        serializer = CreditCardSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
