from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *

def AnswerValidator(value):
	if value != None:
		if value >= 2**31 or value < 0:
			raise ValidationError("The answer must be an integer between 0 and 2^31-1 inclusive.")

class SubmissionForm(forms.Form):
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		problems = kwargs.pop('problems')
		team = kwargs.pop('team')
		super(SubmissionForm, self).__init__(*args, **kwargs)
		# Create a field for each problem
		for p in problems:
			self.fields[str(p)] = forms.IntegerField(required = False, validators = [AnswerValidator], label = str(p.number))
		
	def save(self, **kwargs):
		problems = kwargs.pop('problems')
		team = kwargs.pop('team')
		data = self.cleaned_data
		#print(data)
		sub = Submission(team = team)
		#Save the submission first.
		sub.save() 
		for p in problems:
			sp = str(p)
			#print(data[sp])
			if data[sp] != None:
				att = Attempt(submission = sub, problem = p, guess = data[sp])
				att.save()
				ps_set = ProblemStatus.objects.filter(team = team).filter(problem = p)
				if (not ps_set.exists()):
					ps = ProblemStatus(team = team, problem = p, current_answer = data[sp])
					ps.save()
				else:
					ps = list(ps_set)[0]
					ps.update(att)
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
			'real_names': 'Full names of all team members'
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
		

