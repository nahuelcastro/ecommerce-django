from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *


def loginPage(request):
    # indexPage = "index.html"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            redirect("store")
            # return render(request, indexPage)

    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")
