from django.shortcuts import render, redirect
from ..config import URI

def login(request):
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