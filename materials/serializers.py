from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    model = Course
    field = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    model = Lesson
    field = '__all__'