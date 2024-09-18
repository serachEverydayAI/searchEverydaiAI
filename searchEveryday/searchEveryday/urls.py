from django.contrib import admin
from django.urls import include, path

from .views.page_views import login, index, home_tab, statistic_tab, myInfo_tab
from .views.auth_views import kakaoLoginLogic, kakaoLoginLogicRedirect, kakaoLogout, kakaoLogoutWithAcccount
from django.shortcuts import render
from django.conf.urls import handler404
from django.conf.urls import handler500

def custom_404(request, exception=None):
    return render(request, 'searchEveryday/error/error_404.html', status=404)
handler404 = custom_404

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', login),

    path('index/', index),
    path('home/', home_tab, name='home_tab'),
    path('statistic/', statistic_tab, name='statistic_tab'),
    path('my-info/', myInfo_tab, name='myInfo_tab'),

    path('kakaoLoginLogic/', kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', kakaoLoginLogicRedirect),
    path('kakaoLogout/', kakaoLogout),
    path('kakaoLogoutWithAcccount/', kakaoLogoutWithAcccount),
]