from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.permissions import AuthorOrStaff
from materials.serializers import CourseSerializer, LessonSerializer, CountLessonSerializer
from users.permissions import ModeratorsPermissions


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CountLessonSerializer

        return CourseSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, AuthorOrStaff]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'list':
            self.permission_classes = [IsAuthenticated, ModeratorsPermissions | AuthorOrStaff]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.author = self.request.user
        new_lesson.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.author = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorsPermissions | AuthorOrStaff]
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorsPermissions | AuthorOrStaff]
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorsPermissions | AuthorOrStaff]
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, AuthorOrStaff]
    queryset = Lesson.objects.all()