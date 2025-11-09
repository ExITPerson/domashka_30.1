from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
# from materials.validators import URLValidator
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        # validators = [URLValidator(field=['link_video'])]

        def validate_link_video(self, value):
            if 'youtube.com' not in value:
                raise serializers.ValidationError('URL is not OK')
            return value

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    is_subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['name', 'preview', 'description', 'lessons', 'lessons_count', 'is_subscription', 'last_notified']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscription(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()


class CountLessonSerializer(serializers.ModelSerializer):
    number_of_lessons_per_course = SerializerMethodField()

    def get_number_of_lessons_per_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ['name', 'preview', 'number_of_lessons_per_course']
