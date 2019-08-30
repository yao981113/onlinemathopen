from django.contrib import admin, auth

from .models import *
# Register your models here.

class FileInline(admin.TabularInline):
	model = File

class ProblemInline(admin.TabularInline):
	model = Problem
	fields = ['test', 'number', 'answer', 'num_solves', 'num_attempts']
	readonly_fields = ['num_solves', 'num_attempts']

class TeamInline(admin.TabularInline):
	model = Team
	fields = ['name', 'captain', 'test', 'real_names', 'score']
	readonly_fields = ['score']
	
class SubmissionInline(admin.TabularInline):
	model = Submission
	
class ProblemStatusInline(admin.TabularInline):
	model = ProblemStatus
	
class AttemptInline(admin.TabularInline):
	model = Attempt

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
	inlines = [FileInline, ProblemInline, TeamInline]
	list_display = ['name', 'number_of_problems', 'exam_window_start', 'exam_window_end', 'active']
	list_filter = ['active']
	
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	inlines = [SubmissionInline, ProblemStatusInline]
	list_display = ['name', 'captain', 'test', 'real_names', 'score']
	readonly_fields = ['score']
	list_filter = ['test']
	
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
	inlines = [AttemptInline]
	list_filter = ['team']


