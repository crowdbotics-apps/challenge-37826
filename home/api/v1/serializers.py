from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer

from home.models import App, Subscription, Plan

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            username=generate_unique_username([
                validated_data.get('name'),
                validated_data.get('email'),
                'user'
            ])
        )
        user.set_password(validated_data.get('password'))
        user.save()
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class PasswordSerializer(PasswordResetSerializer):
    """Custom serializer for rest_auth to solve reset password error"""
    password_reset_form_class = ResetPasswordForm


class AppSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50,
        min_length=1
    )

    type = serializers.ChoiceField(
        choices=App.TYPE_CHOICES,
        initial=App.WEB,
        required=True
    )

    framework = serializers.ChoiceField(
        choices=App.FRAMEWORK_CHOICES,
        initial=App.DJANGO,
        required=True
    )

    subscription = serializers.SerializerMethodField(
        required=False
    )

    def get_subscription(self, obj):
        return None

    class Meta:
        model = App
        fields = (
            'id',
            'name',
            'description',
            'type',
            'framework',
            'domain_name',
            'screenshot',
            'user',
            'subscription',
            'created_at',
            'updated_at'
        )

        extra_kwargs = {}

    def create(self, validated_data):
        validated_data['user_id'] = self.context.get('request').user.id
        app = App.objects.create(**validated_data)
        return app

    def update(self, instance, validated_data):
        app = App.objects.filter(id=instance.id)
        app.update(**validated_data)
        return app.last()


class AppPostSerializer(AppSerializer):
    class Meta:
        model = App
        fields = (
            'id',
            'name',
            'description',
            'type',
            'framework',
            'domain_name',
        )

        extra_kwargs = {}


class SubscriptionSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(
        required=True
    )

    def create(self, validated_data):
        validated_data['user_id'] = self.context.get('request').user.id
        subscription = Subscription.objects.create(**validated_data)
        return subscription

    def update(self, instance, validated_data):
        subscription = Subscription.objects.filter(id=instance.id)
        subscription.update(**validated_data)
        return subscription.last()

    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionPostSerializer(SubscriptionSerializer):
    class Meta:
        model = Subscription
        fields = ('plan', 'app', 'active')


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
