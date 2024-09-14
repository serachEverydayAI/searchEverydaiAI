from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json
from django.template import loader
from django.http import HttpResponse, JsonResponse


KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY": "393ca1ee74d48f3859abc66c9f40b86a",
    "KAKAO_REDIRECT_URI": "http://localhost:8000/oauth/kakao/login/callback/",
    "KAKAO_CLIENT_SECRET_KEY": "0AYrHw7x9XtIXARQAN4olB8mPJqrL6wm",
}

kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

URI = {
    "LOGIN" : 'web/index.html',
    "HOME" : 'web/home.html',
}

def index(request):
    _context = {'check':False}
    print(f'Request : {request.session.get('access_token')}')
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request,URI['LOGIN'], _context)

def kakaoLoginLogic(request):
    _redirectUrl = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CONFIG['KAKAO_REST_API_KEY']}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _redirect_uri = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_CONFIG['KAKAO_REST_API_KEY']}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True
    return render(request, URI['HOME'])

def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
      'Authorization': f'bearer {_token}'
    }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        print(f"Success Logout: {_result}")
    else:
        print(f"Error Logout")
    del request.session['access_token']
    return render(request, URI['LOGIN'])

def kakaoLogoutWithAcccount(request):
    _redirect_uri = 'http://127.0.0.1:8000'
    _url = f"https://kauth.kakao.com/oauth/logout?client_id={KAKAO_CONFIG['KAKAO_REST_API_KEY']}&logout_redirect_uri={_redirect_uri}"
    _res = requests.post(_url)
    # _result = _res.json()
    # print(f'kakaoLogoutWithAcccount: {_result}')
    return redirect(_url)