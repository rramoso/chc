
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import string
import csv
from unicodedata import category
import re
import datetime


# In[2]:


# Import data
# Query: Select Id, Name, RecordTypeId, ParentId, BillingState, BillingPostalCode, BillingCountry, ShippingState, ShippingPostalCode, ShippingCountry, Phone, Fax, Website, Market__c FROM Account 
# Assign the accounts from a csv file using dataloader to download

# values = pd.read_csv('./12-8 - FullDev - Account - BACKUP .csv', low_memory=False)


# In[3]:


postalcode_field = 'SHIPPINGPOSTALCODE'


# In[10]:


def clean4zipcodes(zip_val):
    zip_val = str(zip_val)
    if "nan" == zip_val:
    	return np.nan
    if re.match(r'[A-Z]', zip_val) == None:
            if isinstance(zip_val, str):
                return zip_val.zfill(5)
            elif isinstance(zip_val, int): 
                return zip_clean1.map("{:05}".format)


# In[5]:



# values[postalcode_field + '_clean'] = values.dropna(subset = [postalcode_field])[values[postalcode_field].dropna().apply(len) == 4][postalcode_field].apply(clean4zipcodes)


# # In[6]:


# result = values[['ID',postalcode_field, postalcode_field + '_clean']].copy()


# # In[7]:


# result.to_csv(postalcode_field + ' -- cleaned ' + datetime.date.today().strftime("%Y%m%d") +'.csv', index = False)


# # In[9]:




