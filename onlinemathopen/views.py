from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import *

# Create your views here.

def index(request):
    return HttpResponse("Hello, world.")

def contest(request, team_id):
	team = get_object_or_404(models.Team, pk = team_id)
	test = team.test
	
	if request.method == "POST":
		pass
	
	
	score = 0
	
	
	return HttpResponse("This is the page where teams submit answers.")