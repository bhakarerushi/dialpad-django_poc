from rest_framework.routers import DefaultRouter
from users.views import PlatFormUserViewSet, PostViewSet, OauthGitHubView, LoginUserViewSet,TokenRefreshViewSet, TestView
from django.urls import path


router = DefaultRouter()

router.register(r'users', PlatFormUserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')


urlpatterns = router.urls

urlpatterns += [

    path("callback", OauthGitHubView.as_view()),
    path("login", LoginUserViewSet.as_view({'post':'login',})),
    path("signup", LoginUserViewSet.as_view( {'post':'signup'})),
    path("refresh", TokenRefreshViewSet.as_view( {'get':'token_refresh'})),
    path("test_view", TestView.as_view( )),
]


