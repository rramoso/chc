from django.http import HttpResponse
from django.shortcuts import render
from . import templates
from .models import Account

def index(request):

	return render(request, 'import_csv.html', {})

def phone(request):
	a = Account.objects.all()

	return render(request, 'db.html', {'greetings': a})
