# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.conf import settings
from mforms import EditForm
from patcher import make_patch

repo = 'the_repo/'

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

	if request.method == 'POST':
		form = EditForm(request.POST)
		if(form.is_valid()):
			out = make_patch(filename, form.clean()['text'],
					 mail=form.clean()['mail'],
					 user=form.clean()['user'],
					 commit_msg=form.clean()['commit_msg'])
			return render_to_response('patch.html', {'patch':out}) 
	else:
		if request.user.is_authenticated():
			form = EditForm(initial={'text':string, 
						 'user':request.user.username,
						 'mail':request.user.email})
		else:
			form = EditForm(initial={'text':string})

	return render_to_response('editor.html',{'form':form}, context_instance=RequestContext(request))

def new(request, filename):
	if request.method == 'POST':
		form = EditForm(request.POST)
		if(form.is_valid()):
			out = make_patch(filename, form.clean()['text'],
				mail=form.clean()['mail'],
				user=form.clean()['user'],
				commit_msg=form.clean()['commit_msg'])
			return render_to_response('patch.html', {'patch':out})
	else:
		form = EditForm()
	return render_to_response('editor.html', {'form':form}, RequestContext(request))
