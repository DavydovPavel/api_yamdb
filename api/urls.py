from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (TokenObtainPairView,
# TokenRefreshView)

from .views import (CategoryViewSet, GenreViewSet,
                    TitleViewSet, UsersViewSet, CreateUserSet,
                    MyTokenObtainPairView)

router = DefaultRouter()

router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register('users', UsersViewSet)
router.register('auth/email', CreateUserSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'auth/token/',
        MyTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
]
