from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['name', 'preview', 'description', 'lessons', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class CountLessonSerializer(serializers.ModelSerializer):
    number_of_lessons_per_course = SerializerMethodField()

    def get_number_of_lessons_per_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ['name', 'preview', 'number_of_lessons_per_course']
