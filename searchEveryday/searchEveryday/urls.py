from django.contrib import admin
from django.urls import include, path

from .views.myInfo_views import myInfo_details
from .views.page_views import login, index, home_tab, statistic_tab, myInfo_tab
from .views.auth_views import kakaoLoginLogic, kakaoLoginLogicRedirect, kakaoLogout, kakaoLogoutWithAcccount
from django.shortcuts import render
from django.conf.urls import handler404
from django.conf.urls import handler500

from .views.searchWord import addSearchWord, saveCustKeyword, addSearchWordView, getMyKeyword, getTodayNewsList


def custom_404(request, exception=None):
    return render(request, 'searchEveryday/error/error_404.html', status=404)
handler404 = custom_404

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', login),

    path('index/', index),
    path('home/', home_tab, name='home_tab'),
    path('statistic/', statistic_tab, name='statistic_tab'),
    path('myInfo/', myInfo_tab, name='myInfo_tab'),

    path('myInfo_details/', myInfo_details, name='myInfo_details'),
    path('addSearchWord/', addSearchWord, name='addSearchWord'),
    path('addSearchWordView/', addSearchWordView, name='addSearchWordView'),
    path('saveCustKeyword/', saveCustKeyword, name='addSearchWord_save'),

    path('getMyKeyword/', getMyKeyword, name='getMyKeyword'),
    path('getTodayNewsList/', getTodayNewsList, name='getTodayNewsList'),

    path('kakaoLoginLogic/', kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', kakaoLoginLogicRedirect),
    path('kakaoLogout/', kakaoLogout),
    path('kakaoLogoutWithAcccount/', kakaoLogoutWithAcccount),
]