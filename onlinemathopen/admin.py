from django.contrib import admin, auth

from .models import *
# Register your models here.

class FileInline(admin.TabularInline):
	model = File

class ProblemInline(admin.TabularInline):
	model = Problem

class TeamInline(admin.TabularInline):
	model = Team
	
class SubmissionInline(admin.TabularInline):
	model = Submission
	
class ProblemStatusInline(admin.TabularInline):
	model = ProblemStatus
	
class AttemptInline(admin.TabularInline):
	model = Attempt

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
	inlines = [FileInline, ProblemInline, TeamInline]
	list_filter = ['active']
	
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
	list_filter = ['test']
	
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	inlines = [SubmissionInline, ProblemStatusInline]
	list_filter = ['test']
	
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
	inlines = [AttemptInline]
	list_filter = ['team']

@admin.register(ProblemStatus)
class ProblemStatusAdmin(admin.ModelAdmin):
	list_filter = ['team', 'problem']


