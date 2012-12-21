# Create your views here.
from django.shortcuts import render_to_response
from django import forms
import os, subprocess
from django.http import HttpResponse
from django.template import RequestContext
import string, random

repo = 'the_repo/'

class EditForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	CHOICES = [('commit', 'Commit change'),
		   ('make patch', 'Generate the patch')]

	radio = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={"onchange":"details()" }))
	mail = forms.CharField()
	user = forms.CharField()

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
			out = make_patch(filename, form.clean()['text'])
			return render_to_response('patch.html', {'patch':out}) 
	else:
		form = EditForm(initial={'text':string})

	return render_to_response('editor.html',{'form':form}, context_instance=RequestContext(request))

def make_patch(filename, data):
	#Generate random string
	rs = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))

	#Clean and clone repo
	subprocess.call(['git', 'clone', '/home/nikola/sajt/lugons-wiki', '/tmp/temp-repo-'+rs])

	#Write new data into file
	f = open('/tmp/temp-repo-'+rs+'/the_repo/'+filename+'.md', 'w')
	f.write(data.replace('\r', '').encode('UTF-8'))
	f.close()

	#Commit edit
	args = ['git', 'commit', '-a', '-m', "Some commit"]
	git = subprocess.Popen(args, cwd='/tmp/temp-repo-'+rs, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE)
	(out, err) = git.communicate()

	#Create format patch
	args = ['git', 'format-patch', 'origin/master', '--stdout']
	git = subprocess.Popen(args, cwd='/tmp/temp-repo-'+rs, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE)
	(out, err) = git.communicate()

	#Remove temp repo
	subprocess.call(['rm', '-rf', '/tmp/temp-repo-'+rs])

	return out

