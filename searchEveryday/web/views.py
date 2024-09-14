from django.shortcuts import render, redirect

# def index(request):
#     _context = {'check':False}
#     print(f'Request : {request}')
#     if request.session.get('access_token'):
#         _context['check'] = True
#     return render(request,'web/index.html', _context)