from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.forms import formset_factory, modelformset_factory
from .forms import *

from .models import *

# Create your views here.

def index(request):
    return HttpResponse("Hello, world.")

def contest(request, team_id):
	team = get_object_or_404(models.Team, pk = team_id)
	test = team.test
	
	# TODO something about checking if the current user can access the page?
	
	# A list of past submissions that this team made (NOT USED)
	past_submissions = list(Submission.objects.filter(team = team_id).order_by('timestamp'))
	
	# The list of problems associated with the test
	problems = list(Problem.objects.filter(test = test).order_by('number'))
	
	reset_form = True
	
	if request.method == "POST":
		form = SubmissionForm(request.POST, team = team, problems = problems)
		
		if form.is_valid():
			if test.accepting_submissions:
				submission = form.save()
			else:
				pass #Do something about test not accepting submissions
		else: 
			reset_form = False
			pass #Do something about form not being valid
	
	else:
		pass
		
	if reset_form:
		form = SubmissionForm(team = team, problems = problems)
		
	# The list of problem statuses associated with the test
	problem_statuses = list(ProblemStatus.objects.filter(team = team_id).order_by('problem__number'))
	
	context = {
			'team': team,
			'test': test,
			'form': form,
			'files': None, #TODO
			}
	
	return HttpResponse("This is the page where teams submit answers.") #TODO actual rendering
	
