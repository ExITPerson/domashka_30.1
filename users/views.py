from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from users.models import User, Payments
from users.serializers import UserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentsLitsAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_filter = ['course', 'lesson', 'payment_method']
    ordering_filter = ['payment_date']
    permission_classes = [IsAuthenticated]
