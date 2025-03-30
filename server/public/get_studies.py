#!/usr/bin/env python
# coding: utf-8

# In[2]:


# API Request


# In[ ]:


import requests
import json
import pandas as pd
import numpy as np
import datetime
from fastapi import FastAPI
import uvicorn


# In[ ]:


app = FastAPI()

# Initial URL for the first API call
base_url = "https://clinicaltrials.gov/api/v2/studies"

params = {
    'fields': 'protocolSection.identificationModule.nctId,'
              'protocolSection.identificationModule.briefTitle,'
              'protocolSection.conditionsModule.conditions,'
              'protocolSection.statusModule.overallStatus,'
              'protocolSection.statusModule.startDateStruct,'
              'protocolSection.statusModule.primaryCompletionDateStruct,'
              'protocolSection.armsInterventionsModule.interventions,'
              'protocolSection.designModule.studyType,'
              'protocolSection.sponsorCollaboratorsModule.leadSponsor,'
              'protocolSection.sponsorCollaboratorsModule.collaborators,'
              'protocolSection.designModule.phases',
    'filter.overallStatus': 'NOT_YET_RECRUITING,RECRUITING',
    'filter.advanced': 'AREA[StartDate]RANGE[01/01/2024,MAX]',
    'pageSize': 1000,
    'format': 'json',
}

@app.get("/studies")
def get_studies():

    # Initialize an empty list to store the data
    data_list = []

    # Loop until there is no nextPageToken
    while True:

        # Print the current URL (for debugging purposes)
        print("Fetching data from:", base_url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()]))

        # Send a GET request to the API
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            studies = data.get('studies', [])  # Extract the list of studies

            # Loop through each study and extract specific information
            for study in studies:
                # Safely access nested keys
                nctId = study.get('protocolSection', {}).get('identificationModule', {}).get('nctId', 'Unknown')
                overallStatus = study.get('protocolSection', {}).get('statusModule', {}).get('overallStatus', 'Unknown')
                startDate = study.get('protocolSection', {}).get('statusModule', {}).get('startDateStruct', {}).get('date', 'Unknown Date')
                conditions = ', '.join(study.get('protocolSection', {}).get('conditionsModule', {}).get('conditions', ['No conditions listed']))
                acronym = study.get('protocolSection', {}).get('identificationModule', {}).get('acronym', 'Unknown')
                leadSponsor = study.get('protocolSection', {}).get('sponsorCollaboratorsModule', {}).get('leadSponsor', {}).get('name', 'Unknown')
                collaborators_list = study.get('protocolSection', {}).get('sponsorCollaboratorsModule', {}).get('collaborators', [])
                collaborators = ', '.join([collab.get('name', 'No collaborator listed') for collab in collaborators_list])

                # Extract interventions safely
                interventions_list = study.get('protocolSection', {}).get('armsInterventionsModule', {}).get('interventions', [])
                interventions = ', '.join([intervention.get('name', 'No intervention name listed') for intervention in interventions_list]) if interventions_list else "No interventions listed"

                # Extract locations safely
                locations_list = study.get('protocolSection', {}).get('contactsLocationsModule', {}).get('locations', [])
                locations = ', '.join([f"{location.get('city', 'No City')} - {location.get('country', 'No Country')}" for location in locations_list]) if locations_list else "No locations listed"

                # Extract dates and phases safely
                primaryCompletionDate = study.get('protocolSection', {}).get('statusModule', {}).get('primaryCompletionDateStruct', {}).get('date', 'Unknown Date')
                studyFirstPostDate = study.get('protocolSection', {}).get('statusModule', {}).get('studyFirstPostDateStruct', {}).get('date', 'Unknown Date')
                lastUpdatePostDate = study.get('protocolSection', {}).get('statusModule', {}).get('lastUpdatePostDateStruct', {}).get('date', 'Unknown Date')
                studyType = study.get('protocolSection', {}).get('designModule', {}).get('studyType', 'Unknown')
                phases = ', '.join(study.get('protocolSection', {}).get('designModule', {}).get('phases', ['Not Available']))

                # Append the data to the list as a dictionary
                data_list.append({
                    "NCT ID": nctId,
                    "Acronym": acronym,
                    "Overall Status": overallStatus,
                    "Start Date": startDate,
                    "Conditions": conditions,
                    "Interventions": interventions,
                    "Locations": locations,
                    "Primary Completion Date": primaryCompletionDate,
                    "Study First Post Date": studyFirstPostDate,
                    "Last Update Post Date": lastUpdatePostDate,
                    "Study Type": studyType,
                    "Phases": phases
                })

            # Check for nextPageToken and update the params or break the loop
            nextPageToken = data.get('nextPageToken')
            if nextPageToken:
                params['pageToken'] = nextPageToken  # Set the pageToken for the next request
            else:
                break  # Exit the loop if no nextPageToken is present
        else:
            print("Failed to fetch data. Status code:", response.status_code)
        break

    return data_list

def run():
     uvicorn.run(app, host="127.0.0.1", port=8000)

# # Create a DataFrame from the list of dictionaries
# studies = get_studies()
# df = pd.DataFrame()

# # Optionally, save the DataFrame to a CSV file
# df.to_csv("clinical_trials_data_complete.csv", index=False)


# # In[18]:


# # Inspect the raw studies data
# for i, study in enumerate(studies[:5]):  # Check the first 5 studies
#     print(f"Study {i+1}: {study}")
#     print("\n")  # Add a blank line between studies for clarity


# # In[4]:


# # Print the DataFrame
# print(df)


# # In[5]:


# print(df.columns)


# # In[6]:


# # Ensure dates are in datetime format
# df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
# df['Primary Completion Date'] = pd.to_datetime(df['Primary Completion Date'], errors='coerce')

# # Calculate duration
# df['Duration (days)'] = (df['Primary Completion Date'] - df['Start Date']).dt.days


# # In[7]:


# # Ensure dates are in datetime format
# df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
# df['Primary Completion Date'] = pd.to_datetime(df['Primary Completion Date'], errors='coerce')

# # Calculate duration
# df['Duration (days)'] = (df['Primary Completion Date'] - df['Start Date']).dt.days


# # In[8]:


# df_filtered = df.dropna(subset=['Duration (days)'])


# # In[9]:


# avg_duration = df_filtered['Duration (days)'].mean()
# print(f"Average Duration (Days): {avg_duration:.2f}")


# # In[10]:


# import pandas as pd
# import matplotlib.pyplot as plt

# # Load data
# df = pd.read_csv("clinical_trials_data_complete.csv")

# # Ensure dates are parsed correctly
# df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
# df['Primary Completion Date'] = pd.to_datetime(df['Primary Completion Date'], errors='coerce')

# # Calculate Duration
# df['Duration (days)'] = (df['Primary Completion Date'] - df['Start Date']).dt.days

# # Filter valid entries
# df_filtered = df.dropna(subset=['Duration (days)'])
# # Optionally, save the DataFrame to a CSV file
# df_filtered.to_csv("clinical_trials_data_filtered_complete.csv", index=False)
# # Summary Data
# summary = {
#     "Total Trials": len(df),
#     "Trials with Valid Duration": len(df_filtered),
#     "Top Condition": df['Conditions'].value_counts().idxmax(),
#     "Top Intervention": df['Interventions'].value_counts().idxmax(),
#     "Average Duration (Days)": df_filtered['Duration (days)'].mean(),
#     "Missing Start Dates": df['Start Date'].isnull().sum(),
#     "Missing Completion Dates": df['Primary Completion Date'].isnull().sum(),
#     "Missing Phases": df['Phases'].isnull().sum(),
# }

# # Print Summary
# for key, value in summary.items():
#     print(f"{key}: {value}")



# # In[16]:


# # --- Graphs ---

# # 1. Top 10 Conditions
# top_conditions = df['Conditions'].value_counts().head(10)
# plt.figure(figsize=(10, 6))
# top_conditions.plot(kind='bar')
# plt.title("Top 10 Conditions Being Studied")
# plt.xlabel("Conditions")
# plt.ylabel("Number of Trials")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()



# # In[12]:


# # 2. Distribution of Overall Status
# status_distribution = df['Overall Status'].value_counts()
# plt.figure(figsize=(8, 6))
# status_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=140)
# plt.title("Distribution of Overall Status")
# plt.ylabel("")  # Remove y-axis label for clarity
# plt.tight_layout()
# plt.show()


# # In[13]:


# # 3. Trials by Start Year
# df['Start Year'] = df['Start Date'].dt.year
# trials_by_year = df['Start Year'].value_counts().sort_index()
# plt.figure(figsize=(10, 6))
# trials_by_year.plot(kind='bar')
# plt.title("Number of Trials by Start Year")
# plt.xlabel("Year")
# plt.ylabel("Number of Trials")
# plt.tight_layout()
# plt.show()


# # In[14]:


# # 4. Duration Distribution
# plt.figure(figsize=(10, 6))
# df_filtered['Duration (days)'].plot(kind='hist', bins=30, edgecolor='black')
# plt.title("Distribution of Trial Durations")
# plt.xlabel("Duration (Days)")
# plt.ylabel("Number of Trials")
# plt.tight_layout()
# plt.show()


# # In[15]:


# # 5. Phases Distribution
# phases_distribution = df['Phases'].value_counts()
# plt.figure(figsize=(10, 6))
# phases_distribution.plot(kind='bar')
# plt.title("Distribution of Trials by Phase")
# plt.xlabel("Phases")
# plt.ylabel("Number of Trials")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()


# # In[ ]:





# # In[ ]:





# # In[ ]:





# # In[ ]:




