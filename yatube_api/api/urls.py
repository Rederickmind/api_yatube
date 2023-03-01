from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import CommentViewSet, GroupViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r'v1/posts/', PostViewSet)
router.register(r'v1/groups/', GroupViewSet)
router.register(r'v1/posts/(?P<post_id>\d+)/comments/', CommentViewSet)


urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
