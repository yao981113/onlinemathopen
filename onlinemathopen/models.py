import string
import uuid
import random
import os

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.template.defaulttags import register

# Create your models here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

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
        
  # The list of problem numbers ordered by difficulty (easiest first)
  def problems_by_difficulty(self):
    problem_diff = {}
    for prob in self.problem_set.all():
      problem_diff[prob.number] = prob.difficulty
    return sorted(problem_diff, key = lambda n: problem_diff[n])
    
  # The list of teams taking the test, by their current rank
  def teams_by_rank(self):
    pbd = self.problems_by_difficulty()
    return sorted(self.team_set.all(), 
                  key = lambda t: (t.score, tiebreaker_score(pbd, t.solve_set)))
  
  def __str__(self):
    return self.name

# Given a list of problems (in increasing difficulty) and a set of solves, 
# compute the tiebreaker score (i-th easiest problem gives 2^(i-1) points) 
def tiebreaker_score(problems, solves):
  score = 0
  for i in range(len(problems)):
    if problems[i] in solves:
      score += 2**i
  return score

def getFilePath(instance, filename):
  dir_name = ''.join([random.choice(string.ascii_letters+string.digits) for i in range(16)])
  return os.path.join(dir_name, filename)

class File(models.Model):
  name = models.CharField(max_length=80,
      help_text = "Name of the file")
  pdf_file = models.FileField(null=True, blank=True,
      upload_to = getFilePath,
      help_text = "The PDF file")
  test = models.ForeignKey(Contest, on_delete=models.CASCADE,
      help_text = "The test associated to the file")
      
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
  
  @property
  def num_solves(self):
    s = 0
    for ps in self.problemstatus_set.all():
      if ps.correct:
        s += 1
    return s
  
  @property
  def num_attempts(self):
    return self.problemstatus_set.all().count()
  
  @property
  def difficulty(self):
    return (-self.num_solves, self.number)
    
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
  
  @property
  def score(self):
    return len(self.solve_set)
  
  # A set of problem numbers that the team solved
  @property
  def solve_set(self):
    sset = set()
    for ps in self.problemstatus_set.all():
      if ps.correct:
        sset.add(ps.problem.number)
    return sset
  
  def __str__(self):
    return self.name + " in " + str(self.test)

# A submission is what students put on the form when they submit. 
# It contains multiple attempts, one for each problem.
class Submission(models.Model):
  team = models.ForeignKey(Team, on_delete=models.CASCADE,
      help_text = "The team that made the submission")
  timestamp = models.DateTimeField(auto_now_add = True,
      help_text = "The time the submission was made")
  
  def __str__(self):
    return self.team.name + "'s submission at " + str(self.timestamp)
  
# An attempt is the answer to a *single* problem.
class Attempt(models.Model):
  submission = models.ForeignKey(Submission, on_delete=models.CASCADE,
      help_text = "The submission that this answer attempt belongs to")
  problem = models.ForeignKey(Problem, on_delete=models.CASCADE,
      help_text = "The problem that is being attempted")
  guess = models.IntegerField(
      help_text = "The submitted answer")
    
  def __str__(self):
    return self.submission.team.name + "'s answer " + str(self.guess) + " for " + str(self.problem)
  

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
    self.current_answer = attempt.guess
    self.save()
    return True
  
  def __str__(self):
    return self.team.name + "'s problem " + str(self.problem.number)