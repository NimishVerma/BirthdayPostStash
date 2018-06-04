# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from forms import RegistrationForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from django.contrib.auth.models import User

from django.shortcuts import redirect 


def login_redirect(request):
	return redirect('/users/login')
	
def profile(request):
	#args = { 'user' : request.user.username }
	return render(request,'profile.html')

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data
			username = user['username']
			email =  user['email']
			password =  user['password1']
			first_name = user['first_name']
			second_name = user['last_name']
			if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				User.objects.create_user(username, email, password)
				user = authenticate(username = username, password = password)
				login(request, user)
				return redirect('/users/profile')
			else:
				raise forms.ValidationError('Looks like a username with that email or password already exists')

		else:
			args = {'form':form}

			return render(request,'reg_form.html',args)
	else:
		form = RegistrationForm()
		args = {'form':form}
		return render(request,'reg_form.html',args)