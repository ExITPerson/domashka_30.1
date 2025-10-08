from rest_framework import serializers

from materials.models import Course, Lesson
from users.models import User, Payments

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())

    class Meta:
        model = Payments
        fields = ['id','payment_date', 'user', 'course', 'lesson', 'payment_amount']


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'avatar', 'city', 'payments']
