from urllib import request
from django.shortcuts import render


def bologna_view(request):
    return render(request, "common/bologna.html")
