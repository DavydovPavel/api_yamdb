from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, CreateUserSet,
                    GenreViewSet, MyTokenObtainPairView, ReviewViewSet,
                    TitleViewSet, UsersViewSet, MeInfoUserSet)

router = DefaultRouter()

router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
# router.register('users/me', MeUserSet.as_view(), basename="me")
router.register('users', UsersViewSet)
router.register('auth/email', CreateUserSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('users/me/', MeInfoUserSet.as_view(), name="me"),
    path('', include(router.urls)),
    path(
        'auth/token/',
        MyTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
]
