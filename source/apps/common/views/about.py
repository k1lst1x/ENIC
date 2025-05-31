from urllib import request
from django.shortcuts import render

def about_view(request):
    return render(request,"common/about.html")