from django.contrib.auth import authenticate
from rest_framework import serializers
from social_network.models import User, Profile, Post


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # The purpose of this flag is to tell us
        # whether the user has been banned or deactivated.
        # This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'avatar', 'facebook_handle', 'github_handle',
                  'google_plus_handle', 'linkedin_handle', 'twitter_handle', 'location')
        read_only_fields = ('username',)


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    profile = ProfileSerializer(write_only=True)

    first_name = serializers.CharField(source='profile.first_name', read_only=True)
    last_name = serializers.CharField(source='profile.last_name', read_only=True)
    avatar = serializers.CharField(source='profile.avatar', read_only=True)
    facebook_handle = serializers.CharField(source='profile.facebook_handle', read_only=True)
    github_handle = serializers.CharField(source='profile.github_handle', read_only=True)
    google_plus_handle = serializers.CharField(source='profile.google_plus_handle', read_only=True)
    linkedin_handle = serializers.CharField(source='profile.linkedin_handle', read_only=True)
    twitter_handle = serializers.CharField(source='profile.twitter_handle', read_only=True)
    location = serializers.CharField(source='profile.location', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token', 'profile', 'first_name', 'last_name', 'avatar',
                  'facebook_handle', 'github_handle', 'google_plus_handle', 'linkedin_handle', 'twitter_handle',
                  'location')
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)

        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)
            # Save the profile just like we saved the user.
            instance.profile.save()

        return instance


class PostSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Post
        fields = ('id','creator', 'text', 'users_liked')

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(PostSerializer, self).get_validation_exclusions()

        return exclusions + ['creator', 'users_liked']


class PostLikeUnlikeSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Post
        fields = ('creator', 'text', 'users_liked')
        read_only_fields = ('id', 'creator', 'text', 'users_liked')

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(PostLikeUnlikeSerializer, self).get_validation_exclusions()

        return exclusions + ['creator', 'text', 'users_liked']
