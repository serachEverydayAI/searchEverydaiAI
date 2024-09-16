from django.shortcuts import render

def index(request):
    return render(request, 'searchEveryday/index.html')
