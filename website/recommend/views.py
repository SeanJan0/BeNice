from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    return render(request, 'recommend/index.html')
    ##template = loader.get_template('recommend/index.html')
    ##return HttpResponse(template.render(request))

def startRecord(request):
    return HttpResponse("placehold1")

def displayRecommend(request):
    return HttpResponse("placehold2")