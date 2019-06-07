from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
        AbstractBaseUser,
        BaseUserManager,
        PermissionsMixin,)


class UserManager(BaseUserManager):

    def create_user(self, email,
                    phone_number=None,
                    password=None,
                    name=None,
                    **kwargs):
        """Creates and saves a new custom user"""
        if not email:
            raise ValueError("User must have an email address.")

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Creates and saves a new super user"""
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

    def create_staff(self, email, password=None):
        """Creates and saves a new staff user"""

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = False

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports email as the username field"""

    validation_error_message = """
        Phone numbers must be in the format '9802051714' """

    phone_regex = RegexValidator(
        regex=r'(98|97|96)\d{8}',
        message=validation_error_message)

    gender_of_user = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')]

    email = models.EmailField(max_length=255, unique=True)

    name = models.CharField(max_length=255)

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=10,
        unique=True)

    gender = models.CharField(
        choices=gender_of_user,
        max_length=1, default='M')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
