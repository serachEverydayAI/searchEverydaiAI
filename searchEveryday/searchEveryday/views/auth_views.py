import requests
import jwt, json
from ..config import URI, KAKAO_CONFIG, DB_PATH, DatabaseConnection
from django.shortcuts import render, redirect
from ..sql.insert import insertSeCustInfo
from ..sql.select import getSeCustInfo_WithCi


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

    if decoded_id_token:
        default_values = {}
        extracted_values = extract_values(decoded_id_token, default_values)
        addCustIfFirst(extracted_values)
        nickname = extracted_values['nickname']
        picture = extracted_values['picture']

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


def addCustIfFirst(data):
    user_ci = '' if data.get('cust_ci') == '' else data.get('aud')
    sign_up_way = 'KAKAO'

    with DatabaseConnection(DB_PATH) as conn:
        df_SeCustInfo = getSeCustInfo_WithCi(
            user_ci, conn
        )
        print(f"[DEBUG] Add_Customer: {data}, SIZE: {len(df_SeCustInfo)}, user_ci: {user_ci}")
        if len(df_SeCustInfo) == 0:
            insertSeCustInfo(
                conn, data.get('cust_nm'), data.get('cust_birth'), data.get('cust_telco'), data.get('cust_hp'),
                data.get('cust_email'), data.get('cust_gender'),data.get('cust_ssn'),user_ci,
                data.get('nickname'), data.get('picture'), data.get('cust_level'), sign_up_way
            )
        elif len(df_SeCustInfo) > 1:
            print('Error: Duplication Customer', df_SeCustInfo)


def extract_values(decoded_id_token, default_values=None):
    if not isinstance(decoded_id_token, dict):
        if default_values is None:
            return {}
        return {key: default for key, default in default_values.items()}
    if default_values is None:
        default_values = {}

    extracted_values = {}
    for key in decoded_id_token.keys():
        extracted_values[key] = decoded_id_token.get(key, default_values.get(key, None))

    return extracted_values
