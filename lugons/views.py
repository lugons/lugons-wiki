# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField()

def login_page(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.clean()['username'],
					    password=form.clean()['password'])
			print "Authenticated: ", user.is_authenticated()
			print "User: " + user.username
			login(request, user)
			
	else:
		form = LoginForm()
	return render_to_response('login.html', {'form':form}, RequestContext(request))

def logout_page(request):
	if request.user.is_authenticated():
		logout(request)
		return render_to_response('logout.html', {"msg":"You are now logged out."})
	else:
		return render_to_response('logout.html', {"msg":"You are not logged in."})

def index_page(request):
	return render_to_response('article.html', {'stuff':'The index page'})
