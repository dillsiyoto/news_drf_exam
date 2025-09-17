from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Client
from users.serializers import( 
    UserRegistrationSerializer, 
    ActivateSerializer, 
    CustomTokenObtainPairSerializer,
    LoginSerializer
)


class RegistrationViewSet(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Client.objects.all()
    serializer_class = UserRegistrationSerializer


class ActivateAccount(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ActivateSerializer)
    def post(self, request):
        serializer = ActivateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        user = get_object_or_404(Client, email=email, activation_code=code)

        user.is_active = True
        user.save(update_fields=["is_active"])

        return Response(
            {"message": "Аккаунт успешно активирован"}, 
            status=status.HTTP_200_OK
        )
    

class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)