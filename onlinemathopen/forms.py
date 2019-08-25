from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SubmissionForm(forms.Form):
	def __init__(self, *args, **kwargs):
		problems = kwargs.pop('problems')
		team = kwargs.pop('team')
		super(NewSubmissionForm, self).__init__(*args, **kwargs)
		# Create a field for each problem
		for p in problems:
			self.fields[p] = forms.IntegerField(required = False, label = str(p.number))
		
	def save():
		data = self.cleaned_data
		sub = Submission(team = team)
		sub.save()
		for p in problems:
			if data[p] != None:
				att = Attempt(submission = sub, problem = p, guess = data[p])
				att.save()
				ps_set = ProblemStatus.objects.filter(team = team).filter(problem = p)
				if (ps_set.exists()):
					ps = ProblemStatus(team = team, problem = p, current_answer = data[p])
					ps.save()
				else:
					list(ps_set)[0].update(att)
		return sub
		
class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	email = forms.EmailField(max_length=254)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
		
class RegistrationForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['name', 'real_names']
		labels = {
			'name': 'Team Name', 
			'real_names': 'Full names of all team members (including yourself), seperated by commas'
		}

### NOT USED BELOW ###

class AttemptForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		problem = kwargs.pop('problem')
		super(AttemptForm, self).__init__(*args, **kwargs)
		self.fields['guess'].label = str(problem.number)

	class Meta:
		model = Attempt
		fields = ['guess']

class NewAttemptForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		test = kwargs.pop('test')
		super(NewAttemptForm, self).__init__(*args,**kwargs)
		self.fields['problem'].queryset = Problem.objects.filter(test=test)

	class Meta:
		model = Attempt
		fields = ('problem', 'guess',)
		

