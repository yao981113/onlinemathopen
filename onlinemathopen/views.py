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
	
	# A list of past submissions that this team made
	past_submissions = list(models.Submission.objects.filter(team = team_id).order_by('timestamp'))
	
	problem_statuses = list(models.ProblemStatus.objects.filter(team = team_id).order_by('problem__number'))
	
	
	
	if request.method == "POST":
		form = NewAttemptForm(request.POST, test = test)
		pass
	
	
	score = 0
	
	
	return HttpResponse("This is the page where teams submit answers.")