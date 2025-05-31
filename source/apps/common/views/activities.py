from urllib import request
from django.shortcuts import render


def activities_view(request):
    return render(request, "common/activities.html")
