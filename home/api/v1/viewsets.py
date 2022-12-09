import logging

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from home.models import App, Subscription, Plan
from rest_framework import permissions

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
    AppSerializer,
    SubscriptionSerializer,
    SubscriptionPostSerializer,
    AppPostSerializer,
    PlanSerializer
)


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})


class AppViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["post", "get", "put", "delete"]

    response = {
        'message': 'ok'
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return AppPostSerializer
        elif self.action == 'update':
            return AppPostSerializer
        return AppSerializer

    def get_queryset(self):
        self.queryset = App.objects.all()
        return self.queryset

    def get(self, request, pk=None):
        app = get_object_or_404(App, pk=pk)
        return Response(self.serializer_class(data=app).data)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.create()
        return Response(serializer)

    def update(self, request, pk=None, *args, **kwargs):
        app = get_object_or_404(App, pk=pk)

        serializer = AppSerializer(
            instance=app, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk=None):
        app = get_object_or_404(App, pk=pk)
        app.delete()
        return Response(self.response)


class SubscriptionViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["post", "get", "put", "patch"]

    def get_queryset(self):
        self.queryset = Subscription.objects.all()
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return SubscriptionPostSerializer
        elif self.action == 'update':
            return SubscriptionPostSerializer
        return SubscriptionSerializer

    def get(self, request, pk=None):
        app = get_object_or_404(Subscription, app_id=pk)
        return Response(self.serializer_class(data=app).data)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.create()
        return Response(serializer)

    def update(self, request, pk=None, *args, **kwargs):
        subscription = get_object_or_404(Subscription, id=pk)

        serializer = SubscriptionSerializer(
            instance=subscription, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk=None, *args, **kwargs):
        subscription = get_object_or_404(Subscription, id=pk)

        serializer = SubscriptionSerializer(
            instance=subscription, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        self.queryset = Plan.objects.all()
        return self.queryset
