from django.http import HttpResponse
from django.shortcuts import render
def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'rango/index.html', context = context_dict)
    #return HttpResponse("Rango says hey there partner!<br/> <a href='/rango/about/'>About</a>")

def about(request):
    context_dict = {'boldmessage': "Casian"}
    return render(request, 'rango/about.html', context = context_dict)
    #return HttpResponse("Rango says here is the about page.<br/> <a href='/rango/'>Index</a>")