from urllib import request
from django.shortcuts import render


def recognition_view(request):
    return render(request, "common/recognition.html")
