# Core Python

# Core Django
from django.conf.urls import url, include

# Third-Party
from rest_framework import routers

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, ProfileRetrieveAPIView, PostViewSet,\
    PostLikeViewSet, PostUnlikeViewSet, OthersPostsViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('others_posts', OthersPostsViewSet)
router.register('post_like', PostLikeViewSet)
router.register('post_unlike', PostUnlikeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^users/?$', RegistrationAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^profiles/?$', ProfileRetrieveAPIView.as_view()),
]
