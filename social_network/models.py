import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_extensions.db.models import TimeStampedModel

from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import enrich_user

# Create your models here.


class UserManager(BaseUserManager):
    """

    """

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """

    """
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """

        """
        return self.username

    def get_short_name(self):
        """

        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Profile(TimeStampedModel):
    # There is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=127, null=True)
    last_name = models.CharField(max_length=127, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    facebook_handle = models.CharField(max_length=127, null=True)
    github_handle = models.CharField(max_length=127, null=True)
    google_plus_handle = models.CharField(max_length=127, null=True)
    linkedin_handle = models.CharField(max_length=127, null=True)
    twitter_handle = models.CharField(max_length=127, null=True)
    location = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.username


class Post(TimeStampedModel):
    """
    Post made by a user.
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=1023, blank=True)
    users_liked = ArrayField(models.CharField(max_length=255), default=list)

    def no_of_likes(self):
        return len(self.users_liked)

    def __str__(self):
        return 'Post with id: {} - total likes {}'.format(self.id, self.no_of_likes())


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)
        enrich_user(instance)
