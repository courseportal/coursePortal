from django.http import HttpResponse

def index(request):
    return HttpResponse("google-site-verification: google3da26e317e8e8cda.html")
