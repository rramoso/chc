from django.http import HttpResponse
from django.shortcuts import render
from . import templates

def index(request):

	return render(request, 'import_csv.html', {})