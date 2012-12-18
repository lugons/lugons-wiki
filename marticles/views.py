# Create your views here.
from django.shortcuts import render_to_response
from django import forms
import os, subprocess
from django.http import HttpResponse

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
	return render_to_response('editor.html',{'stuff':string} )

def submit_edit(request):
	if 'q' in request.GET:
		subprocess.call(['rm', '-rf', '/tmp/temp-repo'])
		subprocess.call(['git', 'clone', '/home/nikola/sajt/lugons-wiki', '/tmp/temp-repo'])
		f = open('/tmp/temp-repo/the_repo/lugons.md', 'w')
		f.write(str(request.GET['q']))
		subprocess.call(['git', 'commit', '-a', '-m', "Some commit"])
	
		args = ['git', 'format-patch']
		git = subprocess.Popen(args, cwd='/tmp/temp-repo', 
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)
		(out, err) = git.communicate()
		
	else:
		message = 'Empty form.'

	return HttpResponse(out)
