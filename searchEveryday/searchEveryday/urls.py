from django.contrib import admin
from django.urls import include, path
from .views.page_views import index, home
from .views.auth_views import kakaoLoginLogic, kakaoLoginLogicRedirect, kakaoLogout, kakaoLogoutWithAcccount

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', index),
    path('home/', home),

    path('kakaoLoginLogic/', kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', kakaoLoginLogicRedirect),
    path('kakaoLogout/', kakaoLogout),
    path('kakaoLogoutWithAcccount/', kakaoLogoutWithAcccount),
]