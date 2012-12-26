from django import forms

class EditForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	mail = forms.CharField()
	user = forms.CharField()
	commit_msg = forms.CharField()

