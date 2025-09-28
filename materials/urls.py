from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonCreateAPIView, LessonUpdateAPIView, LessonListAPIView, \
    LessonRetrieveAPIView, LessonDestroyAPIView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='create'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_details'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete'),
] + router.urls