from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_email_verified = models.BooleanField(default=False)

    # Fields for password reset
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)

    # Fields for social login integration
    social_provider = models.CharField(max_length=30, blank=True, null=True)
    social_uid = models.CharField(max_length=255, blank=True, null=True)
    social_access_token = models.CharField(max_length=255, blank=True, null=True)

    # Set username to None
    username = None
    # Add any additional fields you need
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

     # Add related_name to avoid clashes
    groups = models.ManyToManyField(Group, related_name='auth_app_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='auth_app_user_permissions')

    def __str__(self):
        return self.email
