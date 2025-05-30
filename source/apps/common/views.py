from django.shortcuts import render

def home_view(request):
    return render(request,"common/home.html")

def about_view(request):
    return render(request,"common/about.html")

def bologna_view(request):
    return render(request,"common/bologna.html")
