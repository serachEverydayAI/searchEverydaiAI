from django.shortcuts import render, redirect
import requests
import jwt, json
from django.shortcuts import render


KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY": "393ca1ee74d48f3859abc66c9f40b86a",
    "KAKAO_REDIRECT_URI": "http://localhost:8000/oauth/kakao/login/callback/",
    "KAKAO_CLIENT_SECRET_KEY": "0AYrHw7x9XtIXARQAN4olB8mPJqrL6wm",
}

kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

URI = {
    "DEFAULT": "http://127.0.0.1:8000",
    "LOGIN" : 'searchEveryday/main/index.html',
    "HOME" : 'searchEveryday/main/home.html',
}

def index(request):
    _context = {'check':False}
    print(f'Request : {request.session.get('access_token')}')
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request,URI['LOGIN'], _context)

def home(request):
    _context = {'check':False}
    print(f'Request : {request.session.get('access_token')}')
    if request.session.get('access_token'):
        _context['check'] = True
        nickname = request.session.get('nickname', 'No nickname')
        picture = request.session.get('picture', 'No picture')
        return render(request, URI['HOME'],{'nickname': nickname,'picture':picture})
    else:
        return redirect(URI['DEFAULT'])

def kakaoLoginLogic(request):
    _redirectUrl = URI['DEFAULT'] + '/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CONFIG['KAKAO_REST_API_KEY']}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _redirect_uri = URI['DEFAULT'] + '/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_CONFIG['KAKAO_REST_API_KEY']}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()

    print("API Response JSON:", _result)

    request.session['access_token'] = _result['access_token']

    id_token = _result.get('id_token')
    decoded_id_token = None

    if id_token:
        try:
            # JWT를 디코딩하여 사용자 정보 추출
            decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})  # 서명 검증을 하지 않음
            print("Decoded ID Token:", decoded_id_token)
        except jwt.ExpiredSignatureError:
            print("The token has expired.")
        except jwt.InvalidTokenError:
            print("Invalid token.")

    # 모든 값을 json 형태로 넘기는 경우 사용
    # decoded_id_token_str = json.dumps(decoded_id_token, indent=4) if isinstance(decoded_id_token,dict) else decoded_id_token
    # request.session['decoded_id_token'] = decoded_id_token_str

    nickname = decoded_id_token.get('nickname', 'No nickname') if isinstance(decoded_id_token, dict) else 'No nickname'
    picture = decoded_id_token.get('picture', 'No picture') if isinstance(decoded_id_token, dict) else 'No picture'
    request.session['nickname'] = nickname
    request.session['picture'] = picture
    request.session.modified = True

    return redirect(URI['DEFAULT'] + '/home')

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
    return redirect(URI['DEFAULT'])

def kakaoLogoutWithAcccount(request):
    _redirect_uri = URI['DEFAULT']
    _url = f"https://kauth.kakao.com/oauth/logout?client_id={KAKAO_CONFIG['KAKAO_REST_API_KEY']}&logout_redirect_uri={_redirect_uri}"
    _res = requests.post(_url)
    del request.session['access_token']
    return redirect(_url)