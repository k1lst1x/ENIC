from urllib import request
from django.shortcuts import render


def reference_view(request):
    return render(request, "common/reference.html")
