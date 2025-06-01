from urllib import request
from django.shortcuts import render


def registryop_view(request):
    return render(request, "common/registryop.html")
