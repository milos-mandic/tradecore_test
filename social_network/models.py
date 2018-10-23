from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class User(models.Model):
    """
    Social network user.
    """
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)

    def __str__(self):
        return 'User: {} - {} {}'.format(self.id, self.first_name, self.last_name)


class Post(models.Model):
    """
    Post made by a user.
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=1023, blank=True, null=True)
    user_liked = ArrayField(models.IntegerField(), blank=True, null=True)

    def no_of_likes(self):
        return len(self.user_liked)

    def __str__(self):
        return 'Post with id: {} - total likes {}'.format(self.id, self.no_of_likes())
