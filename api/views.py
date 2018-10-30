from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social_network.models import Profile, Post
from social_network.tasks import check_email_existence
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer, ProfileSerializer, PostSerializer,\
    PostLikeUnlikeSerializer
from .renderers import UserJSONRenderer, ProfileJSONRenderer, PostJSONRenderer
from .permissions import IsAuthorOfPost
from utils.exceptions import ProfileDoesNotExist, EmailDoesNotExist, PostAlreadyLiked, PostWasntLiked


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        if not check_email_existence(user.get('email')):
            raise EmailDoesNotExist
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):

        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})

        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),

            'profile': {
                'first_name': user_data.get('first_name', request.user.profile.first_name),
                'last_name': user_data.get('last_name', request.user.profile.last_name),
                'avatar': user_data.get('avatar', request.user.profile.avatar),
                'facebook_handle': user_data.get('facebook_handle', request.user.profile.facebook_handle),
                'github_handle': user_data.get('github_handle', request.user.profile.github_handle),
                'google_plus_handle': user_data.get('google_plus_handle', request.user.google_plus_handle),
                'linkedin_handle': user_data.get('linkedin_handle', request.user.profile.linkedin_handle),
                'twitter_handle': user_data.get('twitter_handle', request.user.profile.twitter_handle),
                'location': user_data.get('location', request.user.profile.location),

            }
        }

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):

        try:
            username = self.request.query_params.get('username', None)
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Post.objects.all()
    # permission_classes = (IsAuthenticated,)
    renderer_classes = (PostJSONRenderer,)
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (IsAuthenticated(),)
        return (IsAuthenticated(), IsAuthorOfPost(),)

    def perform_create(self, serializer):
        instance = serializer.save(creator=self.request.user)

        return super(PostViewSet, self).perform_create(serializer)


class PostLikeViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    renderer_classes = (PostJSONRenderer,)
    serializer_class = PostLikeUnlikeSerializer
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.username not in instance.users_liked:
            instance.users_liked.append(self.request.user.username)
        else:
            raise PostAlreadyLiked
        instance.save()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class PostUnlikeViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    renderer_classes = (PostJSONRenderer,)
    serializer_class = PostSerializer
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.username in instance.users_liked:
            instance.users_liked.remove(self.request.user.username)
        else:
            raise PostWasntLiked
        instance.save()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
