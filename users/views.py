from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, filters

from users.models import Payment
from users.serializers import PaymentSerializer

# Платежи
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['paid_at']
    ordering = ["paid_at"]
