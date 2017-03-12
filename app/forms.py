from django import forms
from .models import Survey

class UploadFileForm(forms.Form):
	filename = forms.CharField(max_length=50)

class UserForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50)

class NewUserForm(forms.Form):
	nickname = forms.CharField(max_length=50)
	emailUser = forms.CharField(max_length=50)
	passUser = forms.CharField(max_length=50)

class UrlForm(forms.Form):
	urlProject = forms.CharField(max_length=80)

class UpdateForm(forms.Form):
	newPass = forms.CharField(max_length=50)
	newEmail = forms.CharField(max_length=50)

class SurveyForm(forms.Form):

	question1a = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('yes', 'Yes'), ('mol', 'More or less'), ('no','No')])
	question1b = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('yes', 'Yes'), ('mol', 'More or less'), ('no','No')])
	question2a = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('yes', 'Yes'), ('mol', 'More or less'), ('no','No')])
	question2b = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('yes', 'Yes'), ('mol', 'More or less'), ('no','No')])
	question2c = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('awesome', 'Awesome!'), ('good', 'Good'), ('mol','Neither good not bad'), ('bad','Bad')])
	question2d = forms.CharField(max_length=200)
	question3a = forms.CharField(max_length=100)
	question3b = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('yes', 'Yes'), ('mol', 'More or less'), ('no','No')])
	question3c = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('yes', 'Yes'), ('mol', 'More or less'), ('no','No')])
	question4 = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('yes', 'Yes'), ('mol', 'More or less'), ('no','No')])
	question5 = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('yes', 'Yes'), ('mol', 'More or less'), ('no','No')])
	question6 = forms.CharField(max_length=500)



