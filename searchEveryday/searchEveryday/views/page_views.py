from django.shortcuts import render, redirect

from ..common.confirm import login_yn
from ..config import URI

def login(request):
    _context = {'check':False}
    print(f'Request : {request.session.get('access_token')}')
    if None != request.session.get('access_token'):
        return redirect(URI['DEFAULT'] + '/index')
    else:
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

def index(request):
    if login_yn(request):
        return render(request, URI['INDEX'])
    else:
        return redirect(URI['DEFAULT'])

def home_tab(request):
    if login_yn(request):
        return render(request, URI['HOMETAB'])
    else:
        return redirect(URI['DEFAULT'])

def statistic_tab(request):
    if login_yn(request):
        return render(request, URI['STATISTICTAB'])
    else:
        return redirect(URI['DEFAULT'])

def myInfo_tab(request):
    if login_yn(request):
        nickname = request.session.get('nickname', 'No nickname')
        picture = request.session.get('picture', 'No picture')
        return render(request, URI['MYINFOTAB'],{'nickname': nickname, 'picture': picture})
    else:
        return redirect(URI['DEFAULT'])
