from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, "login.html")

def page_not_found(request, exception):
    return render(request, "404.html", status=404)
