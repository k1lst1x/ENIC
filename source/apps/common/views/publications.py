from urllib import request
from django.shortcuts import render


def publications_view(request):
    return render(request, "common/publications.html")
