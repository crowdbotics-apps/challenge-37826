from django.db import models
from commons.models import BaseTimeModel
from users.models import User


class App(BaseTimeModel):
    MOBILE = 'MOBILE'
    WEB = 'WEB'
    DJANGO = 'DJANGO'
    REACT_NATIVE = 'REACT NATIVE'

    TYPE_CHOICES = (
        (MOBILE, 'Mobile'),
        (WEB, 'Web'),
    )

    FRAMEWORK_CHOICES = (
        (DJANGO, 'Django'),
        (REACT_NATIVE, 'React Native'),
    )

    name = models.CharField(
        max_length=50,
    )

    description = models.TextField(
        blank=True
    )

    type = models.CharField(
        choices=TYPE_CHOICES,
        default=WEB,
        max_length=6
    )

    framework = models.CharField(
        choices=FRAMEWORK_CHOICES,
        default=DJANGO,
        max_length=6
    )

    domain_name = models.CharField(
        max_length=50,
        blank=True
    )

    screenshot = models.URLField(
        blank=True,
        max_length=50
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True
    )

    def __str__(self):
        return self.name


class Plan(BaseTimeModel):
    name = models.CharField(
        max_length=20
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    def __str__(self):
        return self.name


class Subscription(BaseTimeModel):
    user = models.ForeignKey(
        User,
        blank=True,
        on_delete=models.CASCADE
    )

    plan = models.ForeignKey(
        'home.Plan',
        on_delete=models.CASCADE,
    )

    app = models.ForeignKey(
        'home.App',
        on_delete=models.CASCADE,
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f'{self.id}'
