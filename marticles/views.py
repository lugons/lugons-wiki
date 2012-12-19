# Create your views here.
from django.shortcuts import render_to_response
from django import forms
import os, subprocess
from django.http import HttpResponse
from django.template import RequestContext

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
	c = RequestContext(request)

	subprocess.call(['rm', '-rf', '/tmp/temp-repo'])
	subprocess.call(['git', 'clone', '/home/nikola/sajt/lugons-wiki', '/tmp/temp-repo'])
	f = open('/tmp/temp-repo/the_repo/lugons.md', 'w')
	f.write(c)
	f.close()

	args = ['git', 'commit', '-a', '-m', "Some commit"]
	git = subprocess.Popen(args, cwd='/tmp/temp-repo', 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE)
	(out, err) = git.communicate()

	args = ['git', 'format-patch', 'origin/master', '--stdout']
	git = subprocess.Popen(args, cwd='/tmp/temp-repo', 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE)
	(out, err) = git.communicate()
	subprocess.call(['rm', '-rf', '/tmp/temp-repo'])

	return HttpResponse("<html><body><pre>"+out+"</pre></body></html>")
