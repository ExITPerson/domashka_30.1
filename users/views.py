import stripe
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone

from materials.models import Course
from users.models import User, Payments, Subscription
from users.serializers import UserSerializer, PaymentSerializer, SubscriptionSerializer
from users.services import CreatePayment


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


class SubscriptionAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *arg, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'

        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({'message': message})


class SubscriptionManageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, request, course_id, *arg, **kwargs):
        user = request.user
        course_item = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course_item)

        if created:
            return Response({'detail': 'Подписка успешно оформлена'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'detail': 'Подписка уже оформлена'}, status=status.HTTP_200_OK)

    def delete(self, request, course_id,  *arg, **kwargs):
        user = request.user
        course_item = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course_item)

        if subscription.exists():
            subscription.delete()
            return Response({'detail': 'Вы успешно отписались от курса'}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({'detail': 'Вы не подписаны на этот курс'}, status=status.HTTP_400_BAD_REQUEST)


class CreatePymentView(APIView):

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            course = validated_data.get('course')
            lesson = validated_data.get('lesson')

            if course:
                name = course.name
                description = course.description
            elif lesson:
                name = lesson.name
                description = lesson.description
            else:
                return Response({'error': 'Требуется курс или урок'}, status=status.HTTP_400_BAD_REQUEST)

            payment_amount = int(validated_data['payment_amount'] * 100)

            try:
                payment_session = CreatePayment().get_payment_link(name, description, payment_amount)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            payment_instance = serializer.save()

            return Response({
                'id_payment_session': payment_session['id'],
                'payment_url': payment_session['url'],
                'local_payment_id': payment_instance.id,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusPymentView(APIView):

    def post(self, request):
        session_id = request.data.get('id_payment_session')

        if not session_id:
            return Response({'error': 'session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.retrieve(session_id)

        except stripe._error.StripeError as e:
            return Response({'error': f'Stripe error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        payment_status = session.payment_status

        return Response({
            'payment_status': payment_status,
            'session': session
        })


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            email = request.data.get('email', None)

            if email:
                user = User.objects.get(email=email)
                user.last_login = timezone.now()
                user.save()

        return response
