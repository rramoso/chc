
import pandas as pd
from django.http import HttpResponse,HttpResponseNotModified
from django.shortcuts import render
from django.http import HttpResponseRedirect, StreamingHttpResponse
from .forms import UploadFileForm
from . import templates
import re
import csv
from django.conf import settings
from .models import Account
from .scripts.Phone_standardization import *
from .scripts.Zipcode_Cleanse import *
from .scripts.Address import *
from .scripts.Name_decapitalization import *
from django_pandas.io import read_frame
from io import StringIO
from django.template import Context, loader

def index(request):
	
	if request.method == "POST":
		
		form = UploadFileForm(request.POST, request.FILES)
		radio = request.POST.get('optradio')

		csv_file = request.FILES['csv_file']
		file_data = csv_file.read().decode("utf-8")	
		file_name = csv_file.name

		lines = file_data.split("\n")
		fields = lines[0].replace('"','').split(",")
		n_fields = len(fields)

		df = pd.read_csv(StringIO(file_data))
		df.to_csv(settings.STATIC_ROOT+'/uploads/'+file_name,index = False, quoting = csv.QUOTE_ALL)
		if "_upload" in request.POST:
			response = HttpResponseNotModified()

			return response
		if "_qa" in request.POST:
			return QA(df,radio,file_name)

		elif "_load" in request.POST:
			return download_Load(df,radio,file_name)

			# heads = fields
			# print(fields[0].replace('"',''))
		# print(data_dict)
	return render(request, "import_csv.html")



def download_Load(df,radio,file_name):
	if radio == 'phone':

		df['PHONE'] = df.PHONE.apply(tidy_phone_ext)
		df[['ID','PHONE']].to_csv(settings.STATIC_ROOT+'/V2 DataTool - '+file_name+' - Phone Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		# print(request.POST.get('phone') == 'on')
		fp = open(settings.STATIC_ROOT+'/V2 DataTool - '+file_name+' - Phone Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(),content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - '+file_name+' - Phone Cleanse.csv"'
		fp.close() 
		return response 

	elif radio == 'zipcode':

		df['POSTALCODE'] = df.POSTALCODE.apply(clean4zipcodes)

		df[['ID','POSTALCODE']].to_csv(settings.STATIC_ROOT+'/V2 DataTool - '+file_name+' - Zipcode Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		fp = open(settings.STATIC_ROOT+'/V2 DataTool - '+file_name+' - Zipcode Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(), content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - '+file_name+' - Zipcode Cleanse.csv"'
		fp.close()
		return response

	elif radio == 'address':
		
		# Records with zipcode but without state
		df['STATECODE'] = np.nan
		# print(df[(df.STATE.isnull()) & (df.POSTALCODE.notnull())].POSTALCODE.apply(getStateCode))
		df['STATECODE'][df[(df.STATE.isnull()) & (df.POSTALCODE.notnull())].index] = df[(df.STATE.isnull()) & (df.POSTALCODE.notnull())].POSTALCODE.apply(getStateCode)
		# print(df[(df.STATE.isnull()) & (df.POSTALCODE.notnull())])
		df['STATE_CLEAN'] = df.STATECODE.apply(getState)

		# # Records with city but without zipcode 
		df['POSTALCODE_clean'] = np.nan
		df['POSTALCODE_clean'][df[(df.POSTALCODE.isnull()) & (df.CITY.notnull())].index] = df[(df.POSTALCODE.isnull()) & (df.CITY.notnull())].CITY.str.upper().apply(getZip)
		
		# Records with zipcode but without city
		df['CITY_clean'] = df.POSTALCODE.apply(getCity)

		df['POSTALCODE'] = df['POSTALCODE_clean']
		df['CITY'] = df['CITY_clean']
		df['STATE'] = df['STATE_CLEAN']

		df[['ID','POSTALCODE','STATE','CITY','STATECODE']].to_csv(settings.STATIC_ROOT+'/V2 DataTool - '+file_name+' - Address Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		
		fp = open(settings.STATIC_ROOT+'/V2 DataTool - '+file_name+' - Address Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(), content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - '+file_name+' - Address Cleanse.csv"'
		fp.close()
		return response

	elif radio == 'name':

		df['NAME'] = df.NAME.apply(decapitalize)
		df[['ID','NAME']].to_csv(settings.STATIC_ROOT+'/V2 DataTool - '+file_name+' - Name Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		fp = open(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Name Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(), content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - '+file_name+' - Name Cleanse.csv"'
		fp.close()
		return response

	elif radio == 'website':

		df['WEBSITE'] = df.WEBSITE.apply(cleanup_website)
		df[['ID','WEBSITE']].to_csv(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Website Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		fp = open(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Website Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(), content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - '+file_name+' - Website Cleanse.csv"'
		fp.close()
		return response




def QA(df,radio,file_name):
	print("QA")
	if radio == 'phone':

		df['Phone_clean'] = df.PHONE.apply(tidy_phone_ext)
		df[['ID','PHONE','Phone_clean']].to_csv(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Phone Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		# print(request.POST.get('phone') == 'on')
		fp = open(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Phone Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(),content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - '+file_name+' - Phone Cleanse.csv"'
		fp.close() 
		return response 

	elif radio == 'zipcode':

		df['Zipcode_clean'] = df.POSTALCODE.apply(clean4zipcodes)
		print(df.POSTALCODE.apply(clean4zipcodes))
		df[['ID','POSTALCODE','Zipcode_clean']].to_csv(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Zipcode Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		fp = open(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Zipcode Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(), content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - '+file_name+' - Zipcode Cleanse.csv"'
		fp.close()
		return response

	elif radio == 'address':
		
		# Records with zipcode but without state
		df['STATECODE'] = np.nan
		# print(df[(df.STATE.isnull()) & (df.POSTALCODE.notnull())].POSTALCODE.apply(getStateCode))
		df['STATECODE'][df[(df.STATE.isnull()) & (df.POSTALCODE.notnull())].index] = df[(df.STATE.isnull()) & (df.POSTALCODE.notnull())].POSTALCODE.apply(getStateCode)
		# print(df[(df.STATE.isnull()) & (df.POSTALCODE.notnull())])
		df['STATE_CLEAN'] = df.STATECODE.apply(getState)

		# # Records with city but without zipcode 
		df['POSTALCODE_clean'] = np.nan
		df['POSTALCODE_clean'][df[(df.POSTALCODE.isnull()) & (df.CITY.notnull())].index] = df[(df.POSTALCODE.isnull()) & (df.CITY.notnull())].CITY.str.upper().apply(getZip)
		
		# Records with zipcode but without city
		df['CITY_clean'] = df.POSTALCODE.apply(getCity)


		df[['ID','POSTALCODE','STATE','CITY','STATECODE','STATE_CLEAN','POSTALCODE_clean','CITY_clean']].to_csv(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Address Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		fp = open(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Address Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(), content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - '+file_name+' - Address Cleanse.csv"'
		fp.close()
		return response

	elif radio == 'name':

		df['NAME_clean'] = df.NAME.apply(decapitalize)
		df[['ID','NAME','NAME_clean']].to_csv(settings.STATIC_ROOT+'/V2 DataTool - '+file_name+' - Name Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		fp = open(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Name Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(), content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - '+file_name+' - Name Cleanse.csv"'
		fp.close()
		return response

	elif radio == 'website':

		df['WEBSITE_clean'] = df.WEBSITE.apply(cleanup_website)
		df[['ID','WEBSITE','WEBSITE_clean']].to_csv(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Website Cleanse.csv',index = False, quoting = csv.QUOTE_ALL)
		fp = open(settings.STATIC_ROOT+'/'+'V2 DataTool - '+file_name+' - Website Cleanse.csv', 'rb')
		response = HttpResponse(fp.read(), content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="V2 DataTool - '+file_name+' - Website Cleanse.csv"'
		fp.close()
		return response







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


