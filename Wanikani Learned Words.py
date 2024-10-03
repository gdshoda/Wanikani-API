#!/usr/bin/env python
# coding: utf-8

# In[53]:


import requests
import time
from datetime import datetime


# In[2]:


#assigning my API token to a variable
API_TOKEN = "4bad81c8-a0b2-4002-b45b-92751649ce6c"


# In[31]:


#assigning the endpoint url to a variable
API_URL = "https://api.wanikani.com/v2/assignments"


# In[32]:


#creating my headers for the API request
headers = {
    'Authorization' : f'Bearer {API_TOKEN}'
}


# In[33]:


#setting my parameters to only get learned vocabulary
params = {
    'subject_types':'vocabulary',
    'srs_stages': '2,3,4,5,6,7,8,9'
}


# In[8]:


#making the initial API call, in this response will be the next url to call for pagination
response = requests.get(API_URL, headers = headers, params = params)
print(response.status_code)


# In[9]:


#creating a python dictionary from the json response data
data = response.json()


# In[10]:


#creating an empty list to store the vocabulary id's in
vocabulary_list = []


# In[19]:


#iterating through our dictionary to pull out the vocabulary subject ids and add them to our vocab list
for assignment in data['data']:
    vocabulary_list.append(assignment['data']['subject_id'])


# In[30]:


#creating a while loop to check for the next url field in the json response for paginated responses from wanikani. When there is not a next url the loop will end
while data['pages']['next_url'] is not None:
    
    #sending API request for the next pages based off of wanikani's pagination
    newresponse = requests.get(data['pages']['next_url'], headers = headers, params = params)
    
    #delaying one second to not go past wanikani's 60 API calls per minute limit
    time.sleep(1)
    
    #verifying response code from the calls, will be commented out once while loop is confirmed working
    #print(response.status_code)
    
    #assigning the data to the new json response
    data = newresponse.json()
    
    #iterating through the new data to pull out the vocabulary IDs and append to the vocabulary list
    for assignment in data['data']:
        vocabulary_list.append(assignment['data']['subject_id'])
    
    #if we make a bad request, the loop will end so we hopefully don't get stuck in a permanent while loop
    if response.status_code != 200:
        break


# In[38]:


#could skip right to calling all subjects, but first I'm going to get my wanikani level so that I can limit the amount of API  calls I'm making
level_url = 'https://api.wanikani.com/v2/level_progressions'


# In[39]:


#getting my wanikani level data
level_response = requests.get(level_url, headers = headers)


# In[41]:


#converting the json data into a python dictionary
level_data = level_response.json()


# In[71]:


#calling my most recent level
most_recent_level = level_data['data'][-1]['data']['level']


# In[78]:


#generating the range of levels from 1 to the most recent level
api_call_levels = range(1,most_recent_level + 1)

#Converting the levels to a comma-separated string to use in the params of the api call
levels_string = ','.join(map(str, api_call_levels))


# In[149]:


#assigning the wanikani subjects url to a variable
subjects_url = 'https://api.wanikani.com/v2/subjects'


# In[150]:


#setting my api parameters to only retrieve vocabulary from the levels that I have all started
subject_params = {
    'types': 'vocabulary',
    'levels': levels_string
}


# In[151]:


#calling the subject api
subject_response = requests.get(subjects_url, headers = headers, params = subject_params)


# In[184]:


#getting the subject data into a dictionary so we can iterate through the paginated urls
subject_data = subject_response.json()


# In[185]:


#creating a list of the json responses to store the paginated results into here
all_subject_data = [subject_data]


# In[186]:


#creating a while loop to check for the next url field in the json response for paginated responses from wanikani. When there is not a next url the loop will end
while subject_data['pages']['next_url'] is not None:
    
    #sending API request for the next pages based off of wanikani's pagination
    new_subject_response = requests.get(subject_data['pages']['next_url'], headers = headers)
    
    #delaying one second to not go past wanikani's 60 API calls per minute limit
    time.sleep(1)
    
    #verifying response code from the calls, will be commented out once while loop is confirmed working
    print(new_subject_response.status_code)
    
    #assigning the data to the new json response
    subject_data = new_subject_response.json()
    
    all_subject_data.append(subject_data)
    
    #if we make a bad request, the loop will end so we hopefully don't get stuck in a permanent while loop
    if new_subject_response.status_code != 200:
        print(new_subject_response.status_code)

        break


# In[187]:


#creating an empty dictionary to store the vocabulary id's and the words associated with those ids
vocab_dict = {}


# In[189]:


#iterating through each json stored in the list from the paginated response
for subject in all_subject_data:
    
    #iterating through each data section in the json response from wanikani
    for data in subject['data']:
        #print(data)
        
        #setting the vocab id to a variable to be stored in a dictionary
        vocab_id = data['id']
        
        #setting the characters that make up the vocab word to a string to be stored in a dictionary
        vocab_word = data['data']['characters']
        
        #setting the vocab id as the key which then stores the id and the word to be found from our known vocab list of ids from our initial api call
        vocab_dict[vocab_id] = {'id': vocab_id,
                         'word': vocab_word}


# In[191]:


#creating an empty list to store the known vocab words
known_words = []


# In[192]:


#iterating through our list of known_vocab id's calling the newly created dictionary to get the vocab words
for x in vocabulary_list:
    
    #storing the located word in the known_words list
    known_words.append(vocab_dict[x]['word'])


# In[194]:


# Specify the file name to print the words into a text file
file_name = "wanikani known word.txt"

# Open the file in write mode an
with open(file_name, 'w', encoding='utf-8') as file:
    # Writing each known word in the list to the file, followed by a newline character
    for string in known_words:
        file.write(string + '\n')


# In[195]:


import os

#seeing the working directory where the text file was printed
print(os.getcwd())


# In[ ]:




