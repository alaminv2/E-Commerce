from django.db import models


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an EMAIL........!')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user():
        pass

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(_('Staff Status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address_1 = models.TextField(max_length=500, blank=True)
    city = models.CharField(max_length=30, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=14, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    def is_fully_filled(self):
        all_fields = [f.name for f in self._meta.get_fields()]
        for field in all_fields:
            value = getattr(self, field)
            if value is None or value == '':
                return False
        return True


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
