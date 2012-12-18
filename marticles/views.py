# Create your views here.
from django.shortcuts import render_to_response
from django import forms

repo = 'the_repo/'

class EditForm(forms.Form):
	contents = forms.CharField(widget=forms.Textarea)

def hello(request, filename):
	try:
		f = open(repo+filename+'.md')
	except IOError as e:
		return render_to_response('hello.html', {'stuff' : "#fajl ne posoji"})
	string = f.read()
	f.close()
	return render_to_response('hello.html', { 'stuff' : string})

def edit(request, filename):
	try:
		f = open(repo+filename+'.md')
	except IOError as e:
		return render_to_response('hello.html', {'stuff' : "#fajl ne posoji"})
	string = f.read()
	f.close()
	form = EditForm({'contents' : string})
	return render_to_response('editor.html', { 'form' : form })
