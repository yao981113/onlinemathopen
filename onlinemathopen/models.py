import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Contest(models.Model):
	name = models.CharField(max_length=80, default='', 
			help_text = "Name of test", unique=True)
	description = models.TextField(default='', 
			help_text = "Description of the test (shown on listing).")
	number_of_problems = models.IntegerField(default=30, 
			help_text = "Number of problems in the test")
	exam_window_start = models.DateTimeField(
			help_text = "Start of test window")
	exam_window_end = models.DateTimeField(
			help_text = "End of test window")
	active = models.BooleanField(default=False,
			help_text = "Is the contest currently active?")
	
	@property
	def window_has_past(self):
		return timezone.now() > self.exam_window_end
	@property
	def window_not_started(self):
		return timezone.now() < self.exam_window_start
	@property
	def accepting_submissions(self):
		return (not self.window_has_past) \
				and (not self.window_not_started) \
				and self.active
	
	def __str__(self):
		return self.name

# A problem belongs to a contest.
class Problem(models.Model):
	test = models.ForeignKey(Contest, on_delete=models.CASCADE,
			help_text = "The test that the problem is on")
	number = models.PositiveIntegerField(
			help_text = "The problem number on the test")
	answer = models.IntegerField(
			help_text = "The answer to the problem")
			
	def __str__(self):
		return self.test.name + " problem #" + str(self.number)

# A team is the entity where a given user submit answers for a given contest.
class Team(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=80, help_text = "Name of team")
	captain = models.ForeignKey(User, on_delete=models.CASCADE,
			help_text = "The user that registered the team")
	test = models.ForeignKey(Contest, on_delete=models.CASCADE,
			help_text = "The test that the team is for")
	real_names = models.CharField(max_length=320,
			help_text = "Comma separated list of the real student(s) taking the test.")
	
	def __str__(self):
		return self.name + " in " + self.test

# A submission is what students put on the form when they submit. 
# It contains multiple attempts, one for each problem.
class Submission(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE,
			help_text = "The team that made the submission")
	timestamp = models.DateTimeField(auto_now_add = True,
			help_text = "The time the submission was made")
	
	def __str__(self):
		return self.team + "'s submission at " + self.timestamp
	
# An attempt is the answer to a *single* problem.
class Attempt(models.Model):
	submission = models.ForeignKey(Submission, on_delete=models.CASCADE,
			help_text = "The submission that this answer attempt belongs to")
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE,
			help_text = "The problem that is being attempted")
	guess = models.IntegerField(
			help_text = "The submitted answer")
	
	@property
	def correct(self):
		return self.guess == self.problem.answer
		
	def __str__(self):
		return self.submission.team.name + "'s answer " + self.guess + " for problem " + self.problem.number
	

# A problem status corresponds to a team's status on a certain problem.
class ProblemStatus(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE,
			help_text = "The team that this status is linked to")
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE,
			help_text = "The problem that this status is linked to")
	current_answer = models.IntegerField(
			help_text = "The current answer")
	
	@property
	def correct(self):
		return self.current_answer == self.problem.answer
	
	# Update the problem status based on the attempt
	def update(self, attempt):
		current_answer = attempt.guess
		return True
	
	def __str__(self):
		return self.team + "'s problem " + self.problem.number