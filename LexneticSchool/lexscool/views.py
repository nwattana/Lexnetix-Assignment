from django.shortcuts import render, redirect

# Create your views here.
def redirect_docs(request):
	response = redirect('/api/docs')
	return response
