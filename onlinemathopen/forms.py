from django import forms
from .models import *

class SubmissionForm(forms.Form):
	def __init__(self, *args, **kwargs):
		problems = kwargs.pop('problems')
		team = kwargs.pop('team')
		super(NewSubmissionForm, self).__init__(*args, **kwargs)
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
				ps_set = models.ProblemStatus.objects.filter(team = team).filter(problem = p)
				if (ps_set.exists()):
					ps = ProblemStatus(team = team, problem = p, current_answer = data[p])
					ps.save()
				else:
					list(ps_set)[0].update(att)
		return sub
		


### NOT USED BELOW ###

class AttemptForm(form.ModelForm):
	def __init__(self, *args, **kwargs):
		problem = kwargs.pop('problem')
		super(AttemptForm, self).__init__(*args, **kwargs)
		self.fields['guess'].label = str(problem.number)

	class Meta:
		model = models.Attempt
		fields = ['guess']

class NewAttemptForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		test = kwargs.pop('test')
		super(NewAttemptForm, self).__init__(*args,**kwargs)
		self.fields['problem'].queryset = models.Problem.objects.filter(test=test)

	class Meta:
		model = models.Attempt
		fields = ('problem', 'guess',)
		

