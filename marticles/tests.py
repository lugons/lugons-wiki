from django.test import Client
import nose.tools as nt
from django.conf import settings
import os

from patcher import make_patch

class TestMarticles(object):
	
	def setup(self):
		self.repo = settings.REPO_ROOT
		self.client = Client()
		self.write_files()

	def test_old_article_page(self):
		response = self.client.get("/lugons/")
		nt.assert_in('lugons site', response.content)

	def test_new_article(self):
		sent_data = { 'text':'#Some test',
			 'mail':'foo@mail.org',
			 'user':'the user',
			 'commit_msg':'some commit msg',
			}

		response = self.client.post("/new/a/", sent_data)
		nt.assert_in('PATCH', response.content)

	def test_no_such_page(self):
		response = self.client.get("/no-page/")
		nt.assert_in("no such file", response.content)

	def test_index_page(self):
		response = self.client.get("/")
		nt.assert_in("index page", response.content)

	def write_files(self):
		f = open(self.repo+'lugons.md', "w")
		f.write("#lugons site\n- jedan\n- dva\n- tri\n")
		f.close()

class TestPatcher(object):
	def setup(self):
		self.repo = settings.REPO_ROOT
		self.empty_repo()

	def test_new_file_patch(self):
		response = make_patch(
				'new file',
				'no text 2',
				'atlantic777',
				'atlantic777@lugons.org',
				'some commit msg')
		nt.assert_in("no text 2", response)
		nt.assert_in('PATCH', response)

	def empty_repo(self):
		for the_file in os.listdir(self.repo):
			file_path = os.path.join(self.repo, the_file)
			if os.path.isfile(file_path):
				os.unlink(file_path)

