from django.http import HttpResponse
from django.shortcuts import render
from . import templates
# from scripts import *

def index(request):

	return render(request, 'import_csv.html', {})

def phone(request):

	return render(request, 'import_csv.html', {})
