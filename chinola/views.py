
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect, StreamingHttpResponse
from .forms import UploadFileForm
from . import templates
import re
import csv
from .models import Account
from .scripts.Phone_standardization import *
from django_pandas.io import read_frame
from io import StringIO
from django.template import Context, loader

def index(request):
	print('tamo GET: ')
	if request.method == "POST":
		print('tamo POST')
		form = UploadFileForm(request.POST, request.FILES)

		phone  = request.POST.get('phone')

		csv_file = request.FILES['csv_file']
		file_data = csv_file.read().decode("utf-8")	
		lines = file_data.split("\n")
		fields = lines[0].replace('"','').split(",")
		n_fields = len(fields)


		df = pd.read_csv(StringIO(file_data))
		print(df.index)
		
		df['Phone_clean'] = df.PHONE.apply(tidy_phone_ext)
		df[['ID','PHONE','Phone_clean']].to_csv('V2 DataTool - Phone Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		# print(request.POST.get('phone') == 'on')
		fp = open('V2 DataTool - Phone Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(),content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - Phone Cleanse.csv"'
		fp.close()
		return response

		for line in lines:

			fields = line.split(",")
			# heads = fields
			# print(fields[0].replace('"',''))
		# print(data_dict)
	return render(request, "import_csv.html")

def phone(request):

	a = Account.objects.all()
	# print(a.to_dataframe())
	# tidy_phone_ext(Account.objects.get(pk=1).phone)
	df = read_frame(a)
	df['PHONE_clean'] = df.phone.apply(tidy_phone_ext)
	l_df = []
	d_d = read_frame(a).to_dict()
	# for i in d_d:
	# 	f = Account(phone = tidy_phone_ext(d_d[i].phone), name = d_d[i].name)
	# 	l_df.append(f)
	# print(d_d)
	return render(request, 'db.html', {'greetings': a,'fixed':'fixed'})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    with open('static/uploads/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


