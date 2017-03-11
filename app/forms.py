from django import forms

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

#	question1 = forms.ChoiceField(widget=forms.RadioSelect(), choices=[(1, 'yes'), (2, 'moreless'), (3,'no')])
#	question2 = forms.ChoiceField(widget=forms.RadioSelect(), choices=[(1, 'yes'), (2, 'moreless'), (3,'no')])
#	question3 = forms.ChoiceField(widget=forms.RadioSelect(), choices=[(1, 'yes'), (2, 'moreless'), (3,'no')])
    question1 = forms.CharField(max_length=50)

#CHOICES=[('select1','select 1'),
 #        ('select2','select 2')]



