from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [

    path('', views.index, name='index'),
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('signup/', views.signup, name='signup'),
	path('active_tests/', views.active_tests, name='active_tests'),
	path('past_tests/', views.past_tests, name='past_tests'),
	path('register/<int:test_id>/', views.register, name='register'),
	path('compete/<int:test_id>/', views.compete, name='compete')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)