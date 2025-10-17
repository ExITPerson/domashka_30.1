from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentsLitsAPIView, SubscriptionAPIView, SubscriptionManageAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('payments/', PaymentsLitsAPIView.as_view(), name='payments'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscription'),
    path('subscriptions/<int:course_id>/', SubscriptionManageAPIView.as_view(), name='subscription-manage')
] + router.urls