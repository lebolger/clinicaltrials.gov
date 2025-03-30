#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd

# Initial URL for the API call
base_url = "https://clinicaltrials.gov/api/v2/studies"

# Parameters for the API request
params = {
    'filter.overallStatus': 'NOT_YET_RECRUITING,RECRUITING',
    'filter.advanced': 'AREA[StartDate]RANGE[01/01/2024,MAX]',
    'pageSize': 1000,
    'format': 'json',
}

# Initialize an empty list to store the data
data_list = []

# Loop until there is no nextPageToken
while True:
    # Send a GET request to the API
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        studies = data.get('studies', [])  # Extract the list of studies

        # Append the studies to the data list
        data_list.extend(studies)

        # Check for nextPageToken and update the params or break the loop
        nextPageToken = data.get('nextPageToken')
        if nextPageToken:
            params['pageToken'] = nextPageToken  # Set the pageToken for the next request
        else:
            break  # Exit the loop if no nextPageToken is present
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        break

# Create a DataFrame from the list of studies
df = pd.json_normalize(data_list)

# Optionally, save the DataFrame to a CSV file
df.to_csv("clinical_trials_data_complete_v2.csv", index=False)


# In[ ]:





# In[ ]:




