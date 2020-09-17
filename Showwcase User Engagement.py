#!/usr/bin/env python
# coding: utf-8

# # Showwcase User Engagement (Vaishnavi Lolla)

# In[125]:


# import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[126]:


# Read in the file

df = pd.read_csv("showwcase_sessions.csv",sep=',')


# In[127]:


# Data Cleaning (dropping null values)

df = df.dropna()


# In[128]:


# Exploring the Data

df.head()
df.describe()
df.info()


# In[205]:


df.customer_id.nunique()

# There are 48 unique customers in the dataset


# ## Key Performance Indicators (KPIs)

# ### 1. Number of Sessions vs Customers

# In[182]:


# Session Count Distribution

count_sessions = df.groupby(['customer_id']).agg({'session_id': 'nunique'}).reset_index()['session_id']
count_sessions = count_sessions.sort_values()
plt.hist(count_sessions)
plt.title('Number of Session vs Customers')
plt.xlabel('No. of Sessions')
plt.ylabel('No. of Customers')


# In[177]:


# We can observe that there are less number of sessions for more customers i.e., almost 18 customers have 1 to 3 sessions.
# And only 2 customers have more than 20 sessions.


# ### 2. Engagement Rate

# In[184]:


# Engagement Rate based on Likes

df[["likes_given"]] *= 1
print(str(round(df['likes_given'].mean()*100, 2)) + '%')

# Engagement Rate based on Comments

df[["comment_given"]] *= 1
print(str(round(df['comment_given'].mean()*100, 2)) + '%')

# Engagement Rate based on at least one project added

df[["projects_added"]] *= 1
print(str(round(df['projects_added'].mean()*100, 2)) + '%')

# Engagement rate based on Likes & Comments & atleast one project added

df['engage'] = df['likes_given'] * df['comment_given'] * df['projects_added']
print(str(round(df['engage'].mean()*100, 2)) + '%')


# In[ ]:


# We can observe that the user engagement rate is good although there are less number of sessions for most users.
# The engagement rate based on likes is 71.24%
# The engagement rate based on comments is 74.92%
# The engagement rate based on projects added is 75.59%
# The overall engagements rate is 41.47% (likes, comments and projects added)


# ### 3. Impact of Bugs occurred based on Session duration

# In[189]:


#session_duration vs bugs

# Divided the session duration into 4 quartiles (bins) and analyzed the impact of bugs for each of the quartile

session_bins= [0,611,1152,1778,2395]
session_labels = ['First Quartile - Lowest Session Duration',
          'Second Quartile',
          'Third Quartile',
          'Fourth Quartile - Highest Session Duration']


df['session_duration_group'] = pd.cut(df['session_duration'], bins=session_bins, labels=session_labels, right=True)
df['session_duration_group'] = df['session_duration_group'].cat.add_categories('Unknown')

df['session_duration_group'].fillna('Unknown', inplace =True) 
df


# In[190]:


df.isnull().sum()


# In[191]:


df.groupby(['session_duration_group'])['bugs_in_session'].agg('sum')


# In[ ]:


# Although the bugs occurred in all the four quartiles are comparable to each other, the number of bugs occurred in the
# third quartile are slightly lesser. We could dig deeper and take a look at the characterstics of those users.
# Since we don't observe any significant impact of bugs occurred on the session duration, there might be some other factors
# contributing to the reduced session duration which might need additional data.
# We might want to understand what kind of bugs occurred that forced the user to leave the platform.


# In[193]:


df.groupby(['session_duration_group','bug_occured']).agg({'customer_id': 'nunique'})


# In[194]:


df.groupby(['session_duration_group']).agg({'customer_id': 'nunique'})


# Number of users in each quartile also seem to be comparable. There might be a need to market the product even more to see
# a significant difference since the data provided is not showing any huge differences between these categories.


# ### 4. Observations based on Day of the Week

# In[195]:


#convert to date
df['login_date']= pd.to_datetime(df['login_date'])
df['dayofweek'] = df['login_date'].dt.dayofweek.fillna(0).astype(int)
df['dayofweek']


# In[198]:


# separate dictionary which maps values to labels
day={0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}
df['day_name'] = df.dayofweek.apply(lambda x:day[x])
df["day_name"] = df["day_name"].astype("category")


# In[199]:


df


# In[200]:


# Based on Customer ID
print(df.groupby(['day_name','dayofweek']).agg({'customer_id': 'nunique'}).reset_index())
# Based on Session ID
print(df.groupby(['day_name','dayofweek']).agg({'session_id': 'nunique'}).reset_index())


# In[201]:


df_day_cust = df.groupby(['day_name','dayofweek']).agg({'customer_id': 'nunique'}).reset_index().sort_values(by='dayofweek')
df_day_cust


# In[202]:


# Plot showing usage based on the day of the week

plt.figure(figsize=(8, 6))
plt.scatter(x=df_day_cust['day_name'], y=df_day_cust['customer_id'])
plt.plot([0, 7], [0, 50], '--k') # 45 degree line
plt.axis('tight')
plt.xlabel('# Day of Week')
plt.ylabel('No. of Customers')
plt.show()


# In[ ]:


# We can observe that the user engagement is maximum at the beginning and at the end of the week. 
# It is comparatively lesser during the middle of the week.

