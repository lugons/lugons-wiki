import string, random
from django.conf import settings
import os, subprocess

def make_patch(filename, data, user, mail, commit_msg):
	#Generate random string
	rs = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
	random_name='/tmp/temp-repo-'+rs

	#Clean and clone repo
	subprocess.call(['git', 'clone', settings.SITE_ROOT+'/..', random_name])

	#Write new data into file
	f = open(random_name+'/the_repo/'+filename+'.md', 'w')
	f.write(data.replace('\r', '').encode('UTF-8'))
	f.close()
	author = "--author=" + user + " <" + mail + ">"

	#Commit edit
	args = ['git', 'commit', author, '-a', '-m', commit_msg]
	git = subprocess.Popen(args, cwd=random_name, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE)
	(out, err) = git.communicate()

	#Create format patch
	args = ['git', 'format-patch', 'origin/master', '--stdout']
	git = subprocess.Popen(args, cwd=random_name, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE)
	(out, err) = git.communicate()

	#Remove temp repo
	subprocess.call(['rm', '-rf', random_name])
	return out
