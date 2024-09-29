from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from ..common.confirm import login_yn, keyword_yn
from ..config import URI

def login(request):
    _context = {'check':False}
    print(f'Request : {request.session.get('access_token')}')
    if None != request.session.get('access_token'):
        return redirect(URI['DEFAULT'] + '/index')
    else:
        _context['check'] = True
        return render(request,URI['LOGIN'], _context)

def index(request):
    if login_yn(request):
        return render(request, URI['INDEX'])
    else:
        return redirect(URI['DEFAULT'])

def home_tab(request):
    request.session['keyword'] = keyword_yn(request)
    if login_yn(request):
        if request.session['keyword']:
            return render(request, URI['HOMETABY'])
        else:
            return render(request, URI['HOMETABN'])
    else:
        return redirect(URI['DEFAULT'])

def statistic_tab(request):
    if login_yn(request):
        return render(request, URI['STATISTICTAB'])
    else:
        return redirect(URI['DEFAULT'])

def myInfo_tab(request):
    if login_yn(request):
        return render(request, URI['MYINFOTAB'])
    else:
        return redirect(URI['DEFAULT'])

