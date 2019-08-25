from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.forms import formset_factory, modelformset_factory
from .forms import *
from .models import *

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def index(request):
    #return HttpResponse("Hello, world.")
	return render(request, 'onlinemathopen/index.html', {})

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = SignUpForm()
	return render(request, 'onlinemathopen/signup.html', {'form': form})

def active_tests(request):
	tests = Contest.objects.filter(active = True).order_by('exam_window_start')
	return render(request, 'onlinemathopen/active_tests.html', {'tests': tests})
	
def past_tests(request):
	tests = Contest.objects.filter(active = False).order_by('exam_window_start')
	return render(request, 'onlinemathopen/past_tests.html', {'tests': tests})

@login_required
def register(request, test_id):
	test = get_object_or_404(Contest, pk = test_id)
	user = request.user
	if test.window_has_past:
		messages.warning(request, "The test has already ended.")
		form = None
	elif request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			team = form.save(commit = False)
			team.captain = user
			team.test = test
			team.save()
			return redirect('/') #TODO maybe redirect to test page?
	else:
		form = RegistrationForm()
	return render(request, 'onlinemathopen/register.html', {'form': form})

### Find the team that the user is in when they compete
def get_team(test, user):
	team_set = Team.objects.filter(captain = user).filter(test = test)
	if (team_set.exists()):
		return list(team_set)[0]
	return None

@login_required
def contest(request, test_id):
	
	test = get_object_or_404(Contest, pk = test_id)
	# Find the team that the user is on
	team = get_team(test, request.user)
	if (team == None):
		raise Http404("Team not found")
		pass #TODO make them register a team
	if test.window_not_started:
		messages.warning(request, "The test has not started.")
		pass #TODO
	elif test.window_has_past:
		messages.warning(request, "The test has already ended.")
		pass #TODO
	elif not test.active:
		messages.warning(request, "The test is not currently accepting submissions.")
		pass #TODO
	
	# A list of past submissions that this team made (NOT USED)
	past_submissions = list(Submission.objects.filter(team = team).order_by('timestamp'))
	
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
	
	#return HttpResponse("This is the page where teams submit answers.") 
	return render(request, "onlinemathopen/compete.html", context)
	#TODO actual rendering
	
