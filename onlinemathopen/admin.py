from django.contrib import admin, auth

from .models import *
# Register your models here.

admin.site.register(Contest)
admin.site.register(Problem)
admin.site.register(Team)
admin.site.register(Submission)
admin.site.register(ProblemStatus)