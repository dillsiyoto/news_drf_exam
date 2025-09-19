from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import(
    TokenObtainPairView, 
    TokenRefreshView
)
from users.views import RegistrationViewSet, ActivateAccount

router = DefaultRouter()
router.register("register", RegistrationViewSet, basename="register")

urlpatterns = [
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/activate/", ActivateAccount.as_view(), name="activate"),
    path("", include(router.urls)),
]
