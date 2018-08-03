
# coding: utf-8

# In[1]:


from datetime import datetime
from unicodedata import category
import operator
import pandas as pd
import numpy as np
import csv
import string
import re


# In[2]:


addresses = pd.read_csv('free-zipcode-database.csv')


# In[3]:





# In[238]:


old_IVR = pd.read_csv('IVR_without Sate or Zipcode - IVR_WO_zip.csv')


# In[37]:


states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


# In[5]:


def getZip(city):
    try:
        return addresses[addresses.City == city].Zipcode.tolist()[0]
    except:
        return np.nan


# In[120]:


def getCity(zipp):
    try:
        return addresses[addresses.Zipcode == zipp].City.tolist()[0].title()

    except:
        return np.nan


# In[28]:


def getStateCode(zip):
    try:
        return addresses[addresses.Zipcode == zip].State.tolist()[0]
    except:
        return np.nan


# In[45]:


def getState(statecode):
    try:
        return states[statecode]
    except:
        return np.nan


# In[30]:


IVR['Zip_Code__c'] = IVR.City__c.str.upper().apply(getZip)


# In[29]:


IVR['State_ISO_Code__c'] = IVR.Zip_Code__c.apply(getStateCode)


# In[47]:


IVR['State__c'][IVR[(IVR.State__c.isnull()) & (IVR.Zip_Code__c.notnull())].index] = IVR[(IVR.State__c.isnull()) & (IVR.Zip_Code__c.notnull())].State_ISO_Code__c.apply(getState)


# In[10]:


len(IVR[(IVR.City__c.isnull()) & (IVR.Zip_Code__c.isnull())])


# In[69]:


IVR.to_csv('IVR 20180704 - Address fixes.csv')


# In[75]:


# IVR[(IVR.Zip_Code__c.isnull()) & (IVR.Street_Address__c.notnull())][['Zip_Code__c', 'City__c', 'State__c', 'State_ISO_Code__c', 'Country__c','Status__c', 'Street_Address__c']].to_csv('IVR 20180706 - Address fixes with zipcode.csv')


# In[164]:


newIVR = IVR[(IVR.Zip_Code__c.isnull()) & (IVR.Street_Address__c.notnull())]


# In[165]:


l = newIVR.Street_Address__c.str.split(',').tolist()


# In[166]:


maybeZipCodes = []


# In[167]:


for i in l:
    try:
        maybeZipCodes.append(int(i[-1].split()[-1]))
    except:
        maybeZipCodes.append(None)


# In[168]:


newIVR['Zip_Code__c'] = maybeZipCodes


# In[169]:


newIVR['City__c'][newIVR[newIVR.Zip_Code__c.apply(str).apply(len) > 5].index] = newIVR[newIVR.index.isin(newIVR[newIVR.Zip_Code__c.apply(str).apply(len) > 5].index)].Zip_Code__c.apply(getCity)


# In[170]:


l2 = newIVR[(newIVR.City__c.notnull()) & (newIVR.City__c.str.contains(','))].City__c.str.split(',').tolist()


# In[171]:


maybeZipCodes2 = []


# In[172]:


for i in l2:
    try:
        maybeZipCodes2.append(int(i[-1].split()[-1]))
    except:
        maybeZipCodes2.append(None)


# In[173]:


newIVR['Zip_Code__c'][newIVR[(newIVR.City__c.notnull()) & (newIVR.City__c.str.contains(','))].index] = maybeZipCodes2


# In[174]:


newIVR['City__c'] = newIVR.Zip_Code__c.apply(getCity)


# In[175]:


len(newIVR[newIVR.Zip_Code__c.isnull()])  # [['Zip_Code__c', 'City__c', 'State__c', 'State_ISO_Code__c', 'Country__c','Status__c', 'Street_Address__c']]


# In[176]:


newIVR['State_ISO_Code__c'] = newIVR.Zip_Code__c.apply(getStateCode)


# In[178]:


newIVR['State__c'] = newIVR.State_ISO_Code__c.apply(getState)


# In[185]:


IVR[IVR.index.isin(newIVR.index)] = newIVR


# In[219]:


len(IVR[IVR.Zip_Code__c.isnull()])


# In[216]:


IVR[(IVR.Zip_Code__c.isnull()) & (IVR.Street_Address__c.str.contains(','))].Street_Address__c


# In[222]:


toExport = IVR[['sf_account_number__c','Account_Name__c','Zip_Code__c', 'City__c', 'State__c', 'State_ISO_Code__c', 'Country__c', 'Street_Address__c']]


# In[239]:


toExport['Old_ZipCode'] = old_IVR['Zip_Code__c']


# In[240]:


toExport['Old_City__c'] = old_IVR['City__c']


# In[241]:


toExport['Old_State__c'] = old_IVR['State__c']


# In[242]:


toExport['Old_State_ISO_Code__c'] = old_IVR['State_ISO_Code__c']


# In[243]:


toExport['Old_Country__c'] = old_IVR['Country__c']


# In[244]:


toExport['Old_Street_Address__c'] = old_IVR['Street_Address__c']


# In[246]:


toExport.to_csv('IVR 20180706 - Address fixes.csv')

