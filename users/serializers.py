from rest_framework import serializers

from materials.models import Course, Lesson
from users.models import User, Payments, Subscription


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False, allow_null=True)
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Payments
        fields = ['id','payment_date', 'user', 'course', 'lesson', 'payment_amount']

    def validate(self, data):
        if not data.get('course') and not data.get('lesson'):
            raise serializers.ValidationError('Требуется заполнить либо курс, либо урок')
        return data


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'avatar', 'city', 'payments']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Subscription
        fields = ['user', 'course']
