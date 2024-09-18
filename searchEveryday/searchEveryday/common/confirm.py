def login_yn(request):
    _context = {'check': False}
    print(f'Request : {request.session.get('access_token')}')
    if request.session.get('access_token'):
        return True
    else:
        return False