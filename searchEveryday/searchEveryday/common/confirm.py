def login_yn(request):
    print(f'Request : {request.session.get('access_token')}')
    if request.session.get('access_token'):
        return True
    else:
        return False


def keyword_yn(request):
    from ..views.searchWord import getCustKeyword
    cust_id = request.session.get('cust_id')
    print(f'Login cust_id : {cust_id}')
    df = getCustKeyword(cust_id)
    if not df.empty:
        return True
    else:
        return False