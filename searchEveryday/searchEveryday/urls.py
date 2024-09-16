from django.contrib import admin
from django.urls import include, path

from .views.index import index
from .views.page_views import login, home
from .views.auth_views import kakaoLoginLogic, kakaoLoginLogicRedirect, kakaoLogout, kakaoLogoutWithAcccount
from django.shortcuts import render
from django.conf.urls import handler404
from django.conf.urls import handler500

def custom_404(request, exception=None):
    return render(request, 'searchEveryday/error/error_404.html', status=404)
handler404 = custom_404

urlpatterns = [
    path("admin/", admin.site.urls),
    path('index', index),

    path('', login),
    path('home/', home),

    path('kakaoLoginLogic/', kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', kakaoLoginLogicRedirect),
    path('kakaoLogout/', kakaoLogout),
    path('kakaoLogoutWithAcccount/', kakaoLogoutWithAcccount),
]