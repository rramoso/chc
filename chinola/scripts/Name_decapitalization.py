
# coding: utf-8

# In[20]:


import pandas as pd
import numpy as np
import string
import csv
from unicodedata import category
import re
import datetime


# In[3]:


# Import data
# Query: Select Id, Name, RecordTypeId, ParentId, BillingState, BillingPostalCode, BillingCountry, ShippingState, ShippingPostalCode, ShippingCountry, Phone, Fax, Website, Market__c FROM Account 
# Assign the accounts from a csv file using dataloader to download

# values = pd.read_csv('./12-8 - FullDev - Account - BACKUP .csv', low_memory=False)


# In[4]:


EDGECASES = ['LLC', 'LLP', 'LLCP', 'GCIB', 'USA','NYC', 'CPA', 'CDC', 'BBD', 'BBDO', 'OMD', 'IPG',
                 'GSD&M','PHD','JWT','AKQA','VML','BVK','DML','DNA','EMC','MPG','TMP']
    


# In[10]:


DELETE_SENTECES = ['\(Parent - Local Markets\)', '\(Parent Account\)','\(Agency Parent\)','\(Parent\)','\(PARENT\)']


# In[13]:


SPEC_CHARS = ['^','*']


# In[8]:


name_field = 'NAME'


# In[5]:


# NOTE: exceptions to handle: (XXX), -XXX, /XXX, LLC, LLP, LLCP, GCIB 
# 2.1 Regularize Account name capitalization
def decapitalize(cap_str):
    edge_cases = EDGECASES
    result = []
    if len(cap_str) < 5 and cap_str.isupper():
        return cap_str.title()
    elif cap_str.isupper() or cap_str.islower():
        for cap in re.split('\/|\s',cap_str): 
            if cap.upper() in edge_cases or len(cap) <= 2:
                result.append(cap.upper().strip())
            else:
                result.append(cap.title().strip())
        return " ".join(result)
    else:
        return cap_str.title()
    

def cleanup_website(x):
    x = str(x)
    if x == 'nan':
        return np.nan

    if x[-1] == '/':
        x = x[:-1]
    if x[0] == '/':
        x = x[1:]
    x = x.replace('https://', '')
    x = x.replace('http://', '')
    if 'www.' not in x.lower():
        x = 'www.'+x
    return x.lower()

# In[9]:


# # Apply caps normalization, excluding Parent Accounts (based on custom Account_Type__c = 'Parent' until RT Mapping is completed for FullDev)
# values[name_field+'_decap'] = values[name_field].apply(decapitalize).dropna()


# # In[11]:



# # Delete the sentences declare in the list from the Account name
# for i in DELETE_SENTECES:
#     values[name_field+'_decap'] = values[name_field+'_decap'].str.replace(i,'')


# # In[12]:


# values[name_field+'_decap'] = values[name_field+'_decap'].apply(decapitalize).dropna()


# # In[14]:


# Delete the last character of the name if is in SPEC_CHARS
def delete_last_char(x):
    list_spec_chars = SPEC_CHARS
    if x[-1] in list_spec_chars and ('TEST' not in x or 'Test'not in x) :
        return x.replace(x[-1],'')
    return x


# In[15]:


# values[name_field+'_decap'] = values[name_field+'_decap'].apply(delete_last_char)


# # In[16]:


# values[name_field+'_decap'] = values[name_field+'_decap'].str.replace(' Of ',' of ')


# # In[18]:


# result = values[['ID',name_field, name_field + '_decap']].copy()


# # In[21]:


# result.to_csv(name_field+' -- cleaned '+ datetime.date.today().strftime("%Y%m%d") +'.csv', index = False)

