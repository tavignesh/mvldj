from django.shortcuts import render

# Create your views here.

def err404(request, stt):
    return render(request, 'misc/err404.html')

def unknown_error(request):
    return render(request, 'misc/unknownerror.html')
