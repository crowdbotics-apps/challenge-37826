from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.viewsets import (
    SignupViewSet,
    LoginViewSet,
    AppViewSet,
    SubscriptionViewSet,
    PlanViewSet
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("app", AppViewSet, basename="app-user")
router.register("subscriptions", SubscriptionViewSet, basename="subscriptions-user")
router.register("plans", PlanViewSet, basename="plans-user")

urlpatterns = [
    path("", include(router.urls)),
    # path("app/", AppViewSet.as_view({'get': 'retrieve', 'post': 'create'})),
]
