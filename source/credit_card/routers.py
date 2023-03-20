from credit_card.views import CreditcardViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("credit_card", CreditcardViewSet, basename="credit_card")
