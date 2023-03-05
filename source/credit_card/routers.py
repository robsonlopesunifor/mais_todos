from rest_framework.routers import DefaultRouter
from credit_card.views import CreditcardViewSet


router = DefaultRouter()
router.register("credit_card", CreditcardViewSet, basename="credit_card")
