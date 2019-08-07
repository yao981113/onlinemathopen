from django import forms
from . import models

class NewSubmissionForm(forms.ModelForm):
	class Meta:
		model = models.Submission
		

class NewAttemptForm(forms.ModelForm):
	class Meta:
		model = models.Attempt
		fields = ('problem', 'guess',)