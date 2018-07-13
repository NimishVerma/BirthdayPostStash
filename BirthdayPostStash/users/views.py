# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# from forms import RegistrationForm,UploadFileForm
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth import login, authenticate

# from django.contrib.auth.models import User

# from django.shortcuts import redirect 
# from django import forms
# from django.contrib.auth.decorators import login_required
# from .forms import UploadFileForm
# from albums.models import *

# # from imagekit import ImageSpec, register
# # from imagekit.processors import ResizeToFill
# #
# # class Thumbnail(ImageSpec):
# #     processors = [ResizeToFill(100, 50)]
# #     format = 'JPEG'
# #     options = {'quality': 60}
# # register.generator('users:thumbnail', Thumbnail)

# #TODO API implementation of authentication. 
# # Authentication will be done only once and following requests 
# # will be made through a token generated upon authentication

# def login_redirect(request):
# 	return redirect('/users/login')


# @login_required	
# def profile(request):
# 	user = request.user
# 	user_id = User.objects.get(username=user).id
# 	albumimages = AlbumImage.objects.filter(user=user)
# 	people = People.objects.filter(created_by= user_id)
# 	args = { 'user' : request.user,'images':albumimages,'people':people}
# 	print args
# 	print user_id
# 	print People.objects.filter(created_by=1)
# 	return render(request,'profile.html',args)


# def register(request):
# 	if not request.user.is_authenticated:
# 		if request.method == 'POST':
# 			form = RegistrationForm(request.POST)
# 			if form.is_valid():
# 				user = form.cleaned_data
# 				username = user['username']
# 				email =  user['email']
# 				password =  user['password1']
# 				first_name = user['first_name']
# 				last_name = user['last_name']
# 				if not (User.objects.filter(username=username).exists()):
# 					new_user=User.objects.create_user(username, email, password)
# 					new_user.first_name=first_name
# 					new_user.last_name=last_name
# 					new_user.save()
# 					user = authenticate(username = username, password = password)
# 					login(request, user)
# 					return redirect('/users/profile')
# 				else:
# 					raise forms.ValidationError('Looks like a username with that email or password already exists')
# 					#return render(request,'reg_form.html',args)

# 			else:
# 				args = {'form':form}

# 				return render(request,'reg_form.html',args)
# 		else:
# 			form = RegistrationForm()
# 			args = {'form':form}
# 			return render(request,'reg_form.html',args)
# 	else:
# 		return redirect('/users/profile')

# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})


