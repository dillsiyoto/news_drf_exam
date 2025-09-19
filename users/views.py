from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from users.models import Client
from users.serializers import( 
    UserRegistrationSerializer, 
    ActivateSerializer, 
)


class RegistrationViewSet(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Client.objects.all()
    serializer_class = UserRegistrationSerializer
    
    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            201: "пользователь зарегистрирован",
            400: "ошибка валидации данных"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ActivateAccount(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ActivateSerializer,
        responses={
            200: "аккаунт активирован",
            400: "ошибка валидации данных",
            404: "пользователь не найден"
        }
    )

    def post(self, request):
        serializer = ActivateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        user = get_object_or_404(Client, activation_code=code)

        user.is_active = True
        user.save(update_fields=["is_active"])

        return Response(
            {"message": "аккаунт успешно активирован"}, 
            status=status.HTTP_200_OK
        )
    
    