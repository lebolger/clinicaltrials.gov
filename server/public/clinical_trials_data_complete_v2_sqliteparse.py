#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite:///my_database_test1.db')

# Optionally, save the DataFrame to a CSV file
#df.to_csv("clinical_trials_data_complete_v2.csv", index=False)

# Save the DataFrame to an SQLite database
df.to_sql(name='clinical_trials', con=engine,index=False, if_exists="replace")


# In[6]:


with engine.connect() as conn:
  print(pd.read_sql('SELECT "protocolSection.identificationModule.nctId" from clinical_trials', conn))


# In[ ]:




