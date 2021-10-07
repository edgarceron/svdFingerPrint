from django.shortcuts import render

# Create your views here.

def check_fingerprint(request):
    return render(request, 'users/check_fingerprint.html')
