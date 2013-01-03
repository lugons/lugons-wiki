import string, random
from django.conf import settings
import os, subprocess

def random_path():
	rs = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
	random_path='/tmp/temp-repo-'+rs+'/'
	return random_path
	
def clone_repo(repo1, repo2):
	subprocess.call(['git', 'clone', '-q', repo1, repo2])

def write_data(temp_repo, the_file, data):
	file_path = os.path.join(temp_repo, the_file+'.md')
	f = open(file_path, "w")
	data = data.replace('\r', '').encode('UTF-8')
	f.write(data)
	f.close()

def call_command(args, temp_repo):
	git = subprocess.Popen(args, cwd=temp_repo, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE)
	return git.communicate()

def add_file_to_repo(temp_repo, filename):
	args = ['git', 'add', temp_repo + filename + '.md']
	call_command(args, temp_repo)

def commit_change(temp_repo, user, mail, commit_msg):
	author = "--author=" + user + " <" + mail + ">"
	args = ['git', 'commit', author, '-a', '-m', commit_msg]
	call_command(args, temp_repo)

def remove_repo(temp_repo):
	subprocess.call(['rm', '-rf', temp_repo])

def push(temp_repo):
	args = ['git', 'push', 'origin', 'master']
	call_command(args, temp_repo)
	
def commit_edit(filename, data, user, mail, commit_msg):
	write_data(settings.REPO_ROOT, filename, data)
	add_file_to_repo(settings.REPO_ROOT, filename)
	commit_change(settings.REPO_ROOT, user, mail, commit_msg)

def make_patch(filename, data, user, mail, commit_msg):
	temp_repo = random_path()
	clone_repo(settings.REPO_ROOT, temp_repo)
	write_data(temp_repo, filename, data)
	add_file_to_repo(temp_repo, filename)
	commit_change(temp_repo, user, mail, commit_msg)

	args = ['git', 'format-patch', 'origin/master', '--stdout']
	(out, err) = call_command(args, temp_repo)

	remove_repo(temp_repo)
	return out
