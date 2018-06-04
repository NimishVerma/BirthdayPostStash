from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
			)

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		cleaned_form = self.cleaned_data
		user.first_name = cleaned_form['first_name']
		user.last = cleaned_form['last_name']
		user.email = cleaned_form['email']
	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		name = cleaned_data.get('name')
		email = cleaned_data.get('email')
		message = cleaned_data.get('message')
		if not name and not email and not message:
			raise forms.ValidationError('You have to write something!')