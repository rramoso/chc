
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import string
import csv
from unicodedata import category
import re
import datetime


addresses = pd.read_csv('/Users/ricardoramos/Documents/Heroku:Python/chc/chinola/scripts/free-zipcode-database.csv',low_memory = False)
addresses = addresses[addresses.LocationType == 'PRIMARY']
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


def getZip(city):
    try:
        return addresses[addresses.City == city].Zipcode.tolist()[0]
    except:
        return np.nan

def getCity(zipp):
    try:
        return addresses[addresses.Zipcode == zipp].City.tolist()[0].title()

    except:
        return np.nan

def getStateCode(zip):
    try:
        return addresses[addresses.Zipcode == zip].State.tolist()[0]
    except:
        return np.nan

def getState(statecode):
    try:
        return states[statecode]
    except:
        return np.nan


# Import resource for State mapping
# WARNING: CONCERNS AROUND FOREING PROVINCE VALUE THAT DUPLICATE VALID US ONES
# SUCH AS MN -> Minnesota, MN -> Manipur
# SF_countryStates = pd.read_csv('/Users/ricardoramos/Desktop/FullDev Acc Cleanup 2/SF Country-State Codes [Update].csv')


# In[9]:


# Set Index to State for a correct map

# SF_countryStates.index = SF_countryStates['State']


# In[ ]:


# code: Is the two-letter state code that will transform into the Full name.
# 
# country: Is the already clean and correct Full name of the Country. 
#                       Please be sure that match with the SF_countryStates dataframe's country list.
# 
# city: Is the already clean and correct Full name of the City. 
#                       Please be sure that match with the SF_countryStates dataframe's city list.
# 
# 
# 
# Result: It will return the full name of the state based on the its two-letter code. 
#                       Please be sure that match with the SF_countryStates dataframe's state list.
# 


# In[10]:


cities = {}
def stateNameByCode(code,country=np.nan,city=np.nan):
    
    try:
        result = ''
        countries = SF_countryStates[SF_countryStates['State Code'] == code].Country.tolist()
        names = SF_countryStates[SF_countryStates['State Code'] == code].State.tolist()
        if country is not np.nan:
            if country in countries:
                n = countries.index(country)
                result = names[n]
                
                if city is not np.nan and city not in cities:
                    cities[city] = {code : result}
                elif city in cities:
                    cities[city][code] = result
                    
                return result
            
            if len(countries) > 1:
                for i in names:
                    cities[city] = {code:i}
            
            result = names[0]
            cities[city] = {code : result}
            return result
            
        elif city in cities.keys():
            if code is not np.nan:
                result = cities[city][code]
                return result
            return list(cities[city].values())[0]
        else:
            result = names[0]
            cities[city] = {code : result}
            return result
    except:
        return code


# In[11]:


# values[state_field+'_clean'] = np.vectorize(stateNameByCode)(values[state_field], values[state_field],values[clea])



# In[12]:


# result = values[['ID',state_field, state_field + '_clean']].copy()


# In[ ]:


# result.to_csv(state_field+' -- cleaned '+ datetime.date.today().strftime("%Y%m%d") +'.csv', index = False)

