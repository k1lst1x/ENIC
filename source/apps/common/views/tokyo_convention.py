from urllib import request
from django.shortcuts import render


def tokyo_convention_view(request):
    return render(request, "common/tokyo_convention.html")
