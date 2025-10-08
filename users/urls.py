from rest_framework.routers import DefaultRouter
from django.urls import path
from users.apps import UsersConfig
from users.views import UserViewSet, PaymentsLitsAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('payments/', PaymentsLitsAPIView.as_view(), name='payments')
] + router.urls