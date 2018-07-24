
# coding: utf-8

# In[2]:


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

values = pd.read_csv('./ACBJ_Prod_Contact_20180208.csv', low_memory = False)


# In[6]:


phone_field = 'PHONE'


# In[7]:



EXTCODES = [', ext.', 'Ext:', 'Ext.', 'ext.', 'EXT.', 'Ext', 'ext', 'EXT', 'ex.', 'Ex.', 'EX.', 'Ex', 'ex', 'EX', 'x', 'X'] 


# In[8]:


phone_cleanup_re = r'^[P\: ]?[\: ]?[t ]?[\+]?[1]?[\.]?[\ ]?[\-]?\(?([0-9]{3})\)?[-.● ]?([0-9]{3})[-.● ]?([0-9]{4})[\-\.]?$'

def tidy_phone(bad_num):
    try:
        return re.sub(phone_cleanup_re, r'(\1) \2-\3', bad_num)
    except TypeError:
        return np.nan

def tidy_phone_ext(bad_num):
    if bad_num != bad_num:
        return bad_num
    ext_codes = EXTCODES
    try:
        bad_num = str(bad_num)
    except:
        return bad_num
    for ext_code in ext_codes:
        if ext_code in bad_num:
            try:
                phone_num, phone_ext = bad_num.split(ext_code)
                clean_num = tidy_phone(phone_num)
                clean_num = clean_num.replace(',','')
                phone_ext = phone_ext.replace(')','')
                return tidy_phone(clean_num.strip()) + ' ' + 'x' + phone_ext.strip()
            except:
                return bad_num
    try:
        return re.sub(phone_cleanup_re, r'(\1) \2-\3', bad_num)
    except TypeError:
        return np.bad_num


# In[9]:


# Clean up phone number

values[phone_field+ '__clean'] = values[phone_field].apply(tidy_phone_ext)


# In[13]:


result = values[['ID',phone_field, phone_field + '__clean']].copy()


# In[14]:


result.to_csv(phone_field+' -- cleaned '+ datetime.date.today().strftime("%Y%m%d") +'.csv', index = False, quoting = csv.QUOTE_ALL)

