#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np
import sklearn.cluster


# In[3]:


data = np.arange(0,100)


# In[4]:


data = list(zip(data, data)) 


# In[ ]:


from sklearn.cluster import KMeans


# In[11]:


model = KMeans(n_clusters=3, init='random', max_iter=50)


# In[12]:


model.fit(data)


# In[13]:


model.cluster_centers_


# # Importing required libraries

# In[14]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[15]:


from google.colab import drive
drive.mount('/content/drive')


# # Creating dataframes

# In[16]:


DATA_FOLDER = '/content/drive/MyDrive/data/uber_rideshare/'


# In[ ]:


apr14 = pd.read_csv(DATA_FOLDER+'uber-raw-data-apr14.csv')
may14 = pd.read_csv(DATA_FOLDER+'uber-raw-data-may14.csv')
jun14 = pd.read_csv(DATA_FOLDER+'uber-raw-data-jun14.csv')
jul14 = pd.read_csv(DATA_FOLDER+'uber-raw-data-jul14.csv')
aug14 = pd.read_csv(DATA_FOLDER+'uber-raw-data-aug14.csv')
sep14 = pd.read_csv(DATA_FOLDER+'uber-raw-data-sep14.csv')


# In[ ]:


merged_df = pd.concat([apr14, may14, jun14, jul14, aug14, sep14])
merged_df


# # String to datetime conversion

# In[ ]:


apr14['Date/Time'] = pd.to_datetime(apr14['Date/Time'], format='%m/%d/%Y %H:%M:%S')
may14['Date/Time'] = pd.to_datetime(may14['Date/Time'], format='%m/%d/%Y %H:%M:%S')
jun14['Date/Time'] = pd.to_datetime(jun14['Date/Time'], format='%m/%d/%Y %H:%M:%S')
jul14['Date/Time'] = pd.to_datetime(jul14['Date/Time'], format='%m/%d/%Y %H:%M:%S')
aug14['Date/Time'] = pd.to_datetime(aug14['Date/Time'], format='%m/%d/%Y %H:%M:%S')
sep14['Date/Time'] = pd.to_datetime(sep14['Date/Time'], format='%m/%d/%Y %H:%M:%S')
merged_df['Date/Time'] = pd.to_datetime(merged_df['Date/Time'], format='%m/%d/%Y %H:%M:%S')


# In[ ]:


dfs = [apr14, may14, jun14, jul14, aug14, sep14, merged_df]
current_df = dfs[0]


# # Rideshare histogram

# In[ ]:


current_df['Time'] = current_df['Date/Time'].dt.time.apply(lambda x: int(x.strftime('%H%M%S')))
current_df


# In[ ]:


sns.histplot(current_df['Time'])


# # Filtering morning and evening rides

# In[ ]:


morning_df_idx = (current_df['Time'] > 50000) & (current_df['Time'] < 110000)
morning_df = current_df[morning_df_idx]
evening_df_idx = (current_df['Time'] > 150000) & (current_df['Time'] < 220000)
evening_df = current_df[evening_df_idx]


# In[ ]:


morning_df


# In[ ]:


evening_df


# In[ ]:


morning_coordinates = morning_df[['Lat','Lon']].sample(10000,random_state = 10).values
evening_coordinates = evening_df[['Lat','Lon']].sample(10000,random_state = 10).values


# # Installing folium
# for plotting coordinates

# In[ ]:


get_ipython().system('pip install folium')


# In[ ]:


import folium


# # Plotting morning rides on map

# In[ ]:


morning_map = folium.Map(location=[40.79658011772687, -73.87341741832425], zoom_start = 12, tiles='Stamen Toner')
for coordinate in morning_coordinates:
  folium.CircleMarker(radius=1,location=coordinate,fill=True).add_to(morning_map)
morning_map


# # Plotting evening rides on map

# In[ ]:


evening_map = folium.Map(location=[40.79658011772687, -73.87341741832425], zoom_start = 12, tiles='Stamen Toner')
for coordinate in evening_coordinates:
  folium.CircleMarker(radius=1,location=coordinate,color="#FF0000",fill=True).add_to(evening_map)
evening_map


# # Importing KMeans

# In[ ]:


from sklearn.cluster import KMeans
import numpy as np


# # Finding clusters

# In[ ]:


n_clusters = 6
model = KMeans(n_clusters=n_clusters, init='random', max_iter=300)
model.fit(morning_df[['Lat','Lon']])


# In[ ]:


morning_centroids = model.cluster_centers_
morning_centroids


# In[ ]:


for i, coordinate in enumerate(morning_centroids):
    folium.Marker(coordinate, popup='Centroid {}'.format(i+1), icon=folium.Icon(color='red')).add_to(morning_map)
morning_map


# ## for evening

# In[ ]:


n_clusters = 6
model = KMeans(n_clusters=n_clusters, init='random', max_iter=300)
model.fit(evening_df[['Lat','Lon']])


# In[ ]:


evening_centroids = model.cluster_centers_
evening_centroids


# In[ ]:


for i, coordinate in enumerate(evening_centroids):
    folium.Marker(coordinate, popup='Centroid {}'.format(i+1), icon=folium.Icon(color='blue')).add_to(evening_map)
evening_map


# # Finding clusters in whole selected dataframe

# In[ ]:


n_clusters = 8
model = KMeans(n_clusters=n_clusters, init='random', max_iter=300)
model.fit(current_df[['Lat','Lon']])


# In[ ]:


centroids = model.cluster_centers_
centroids


# In[ ]:


map = folium.Map(location=[40.79658011772687, -73.87341741832425], zoom_start = 12, tiles='Stamen Toner')
for i, coordinate in enumerate(centroids):
    folium.Marker(coordinate, popup='Centroid {}'.format(i+1), icon=folium.Icon(color='blue')).add_to(map)
map


# In[ ]:


new_ride = (40.70647056912189, -73.91116590442799)
folium.Marker(new_ride, popup='New Rider', icon=folium.Icon(color='green')).add_to(map)
map


# In[ ]:


centroid_idx = model.predict([new_ride])


# In[ ]:


centroids[centroid_idx]


# In[ ]:


folium.Marker(centroids[centroid_idx][0], icon=folium.Icon(color='yellow')).add_to(map)
map
