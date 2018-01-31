from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# utils imports
from .utils import shared_file

# model imports
from .models import File

# python imports
import dropbox


# view for rendering and processing login page
# receives `username` and `password` in POST method
def login_view(request):

	# To check if the login credentials were correct
	error = False 

	if (request.method=='POST') :	# if the user submit's login form via POST method
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)
		if user is not None: # chech if the user is valid
			login(request, user)
			return redirect('/files') # show the files shared to the user
		else: # show error message if user is invalid
			error = True

	context = {
		'error' : error,
	}

	return render(request, 'login.html', context)

# logout the user and render login page
def logout_view(request):
	logout(request)
	return render(request, 'login.html')

# view for showing the files shared to the user
def files_view(request):
	# if user is not authenticated redirect him to the login page
	if not request.user.is_authenticated:
		return render(request, 'login.html')


	entries = File.objects.filter(users=request.user)

	context = {
		'entries' : entries,
	}

	return render(request, 'files.html', context)




# download the requested file if shared to the user
# file_name -> name of the file user is trying to download
def download_view(request, file_name):

	if( shared_file(file_name, request.user) ):
		dbx = dropbox.Dropbox('mi4aIRbk-MAAAAAAAAAAmQQkf1WZbyiRI3bBvFWJwM6atGiQvHNLmNGxsC2tvT16') # My dropbox api auth code
		path = "/" + str(file_name) # path of the file stored in drive
		try:
			md, res = dbx.files_download(path) 
		except dropbox.exceptions.HttpError as err:
			return HttpResponse('*** HTTP error', err)
		data = res.content
		print(len(data), 'bytes; md:', md)
		return HttpResponse(data)
	else :
		return HttpResponse("You cannot access this file :)")

