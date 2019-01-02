
# coding: utf-8

# # Mácio Matheus Arruda
# 
# --------------------------------------------
# ## The Brazilian tourism agency plans to organize their first trip to Toronto in Canada, and they plan to start with the city of North York.
# 
# #### To create the best itinerary for your clients, the travel agency is looking for which districts near North York
# #### visit, for that, he had commissioned an analysis of characteristics and the most relevant places in these neighborhoods.
# 
# #### Mainly, the tourism agency focuses on hotels, restaurants, parks, shops, places, squares, etc.
# 
# #### Question: So, what are the characteristics of the neighborhoods neighboring North York and what places should the Brazilian tourism agency  visit to provide the best tour to its clients?
# 

# In[1]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup as bs
import requests
from geopy.geocoders import Nominatim 
import folium


# ### Load the pandas dataframe with Toronto data

# In[2]:


df_toronto = pd.read_csv('toronto_data.csv')
df_toronto.tail(50)


# ### Create a simple map of Toronto City

# In[3]:


# for the city Toronto, latitude and longtitude are manually extracted via google search
toronto_latitude = 43.6532; toronto_longitude = -79.3832
map_toronto = folium.Map(location = [toronto_latitude, toronto_longitude], zoom_start = 11)

# add markers to map
for lat, lng, borough, neighborhood in zip(df_toronto['Latitude'], df_toronto['Longitude'], df_toronto['Borough'], df_toronto['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=7,
        popup=label,
        color='green',
        fill=True,
        fill_opacity=0.4).add_to(map_toronto)  
    

map_toronto


# #### Below, a printscreen containing the plotted map (if there is a problem in the previous cell)

# ![Folium map screenshot](https://raw.githubusercontent.com/macio-matheus/Coursera_Capstone/master/week4/screenshot_folium_map_toronto.png)

# ### Create a new data frame with neighborhoods in North York 

# In[4]:


CLIENT_ID = 'foo' # your Foursquare ID
CLIENT_SECRET = 'foo' # your Foursquare Secret
VERSION = '20180604'


# In[5]:


nyork_data = df_toronto[df_toronto['Borough'] == 'North York'].reset_index(drop=True)
nyork_data.drop(['Unnamed: 0'], axis=1, inplace=True)
nyork_data


# ### Create a map of North York and its neighbourhoods

# In[6]:


address_nyork = 'North York,Toronto'
latitude_nyork = 43.773077
longitude_nyork = -79.257774
print('The geograpical coordinate of North York are {}, {}.'.format(latitude_nyork, longitude_nyork))


# In[7]:


map_nyork = folium.Map(location=[latitude_nyork, longitude_nyork], zoom_start=13)

# add markers to map
for lat, lng, label in zip(nyork_data['Latitude'], nyork_data['Longitude'], nyork_data['Neighborhood']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=9,
        popup=label,
        color='blue',
        fill=True,
        fill_opacity=0.5).add_to(map_nyork)  
    
map_nyork


# #### Below, a printscreen containing the plotted map (if there is a problem in the previous cell)

# ![Folium map screenshot](https://raw.githubusercontent.com/macio-matheus/Coursera_Capstone/master/week4/screenshot_folium_map_northyork.png)

# ### Get the top 100 venues in the neighborhood 'Hillcrest Village', from North York

# In[8]:


neighborhood_latitude = nyork_data.loc[0, 'Latitude'] # neighbourhood latitude value
neighborhood_longitude = nyork_data.loc[0, 'Longitude'] # neighbourhood longitude value

neighborhood_name = nyork_data.loc[0, 'Neighborhood'] # neighbourhood name

print('Latitude and longitude values of "{}" are {}, {}.'.format(neighborhood_name, 
                                                               neighborhood_latitude, 
                                                               neighborhood_longitude))


# In[9]:


LIMIT = 100
radius = 1000
url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&ll={},{}&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude_nyork, longitude_nyork, VERSION, radius, LIMIT)


# In[10]:


results = requests.get(url).json()
results


# In[11]:


def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    return categories_list[0]['name']


# In[12]:


import json
from pandas.io.json import json_normalize

venues = results['response']['groups'][0]['items']  
nearby_venues = json_normalize(venues)
filtered_columns = ['venue.name', 'venue.categories', 'venue.location.lat', 'venue.location.lng']
nearby_venues =nearby_venues.loc[:, filtered_columns]
nearby_venues['venue.categories'] = nearby_venues.apply(get_category_type, axis=1)
nearby_venues.columns = [col.split(".")[-1] for col in nearby_venues.columns]

nearby_venues.head(10)


# In[13]:


print('{} venues were returned by Foursquare.'.format(nearby_venues.shape[0]))


# In[14]:


def getNearbyVenues(names, latitudes, longitudes, radius=500):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
        print(name)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood', 
                  'Neighborhood Latitude', 
                  'Neighborhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


# ### Get venues for each neighborhood in North York

# In[15]:


nyork_venues = getNearbyVenues(names=nyork_data['Neighborhood'], latitudes=nyork_data['Latitude'], longitudes=nyork_data['Longitude'])


# In[16]:


nyork_venues.tail(10)


# In[17]:


nyork_venues.groupby('Neighborhood').count()


# In[18]:


print('There are {} uniques categories.'.format(len(nyork_venues['Venue Category'].unique())))


# In[19]:


# one hot encoding
nyork_onehot = pd.get_dummies(nyork_venues[['Venue Category']], prefix="", prefix_sep="")

# add neighborhood column back to dataframe
nyork_onehot['Neighborhood'] = nyork_venues['Neighborhood'] 

# move neighborhood column to the first column
fixed_columns = [nyork_onehot.columns[-1]] + list(nyork_onehot.columns[:-1])
nyork_onehot = nyork_onehot[fixed_columns]

nyork_onehot.head(20)


# In[20]:


nyork_onehot.shape


# In[21]:


nyork_grouped = nyork_onehot.groupby('Neighborhood').mean().reset_index()
nyork_grouped.head(10)


# ### Get top 10 venues per neighborhood

# In[22]:


def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]


# In[23]:


num_top_venues = 10

indicators = ['st', 'nd', 'rd']

# create columns according to number of top venues
columns = ['Neighborhood']
for ind in np.arange(num_top_venues):
    try:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    except:
        columns.append('{}th Most Common Venue'.format(ind+1))

# create a new dataframe
neighborhoods_venues_sorted = pd.DataFrame(columns=columns)
neighborhoods_venues_sorted['Neighborhood'] = nyork_grouped['Neighborhood']

for ind in np.arange(nyork_grouped.shape[0]):
    neighborhoods_venues_sorted.iloc[ind, 1:] = return_most_common_venues(nyork_grouped.iloc[ind, :], num_top_venues)

neighborhoods_venues_sorted


# ### Run k-means to cluster the neighborhoods into 3 clusters

# In[24]:


# import k-means from clustering stage
from sklearn.cluster import KMeans

nyork_data = nyork_data.drop(16)
# set number of clusters
kclusters = 3
nyork_grouped_clustering = nyork_grouped.drop('Neighborhood', 1)
# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(nyork_grouped_clustering)

# check cluster labels generated for each row in the dataframe
kmeans.labels_[0:10] 


# ### Include kmeans.labels_ into the original North York dataframe

# In[25]:


nyork_merged = nyork_data

# add clustering labels
nyork_merged['Cluster Labels'] = kmeans.labels_
nyork_merged = nyork_merged.join(neighborhoods_venues_sorted.set_index('Neighborhood'), on='Neighborhood')
nyork_merged


# ### Visualize the clusters in the map

# In[26]:


# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# create map
map_clusters = folium.Map(location = [latitude_nyork, longitude_nyork], zoom_start=11)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i+x+(i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(nyork_merged['Latitude'], nyork_merged['Longitude'], nyork_merged['Neighborhood'], nyork_merged['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=8,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=1.0).add_to(map_clusters)
       
map_clusters


# #### Below, a printscreen containing the plotted map (if there is a problem in the previous cell)

# ![Folium map screenshot](https://raw.githubusercontent.com/macio-matheus/Coursera_Capstone/master/week4/screenshot_folium_map_clusteres.png)

# ### Examine each of the five clusters

# In[27]:


nyork_merged.loc[nyork_merged['Cluster Labels'] == 0, nyork_merged.columns[[1] + list(range(5, nyork_merged.shape[1]))]]


# In[28]:


nyork_merged.loc[nyork_merged['Cluster Labels'] == 1, nyork_merged.columns[[1] + list(range(5, nyork_merged.shape[1]))]]


# In[29]:


nyork_merged.loc[nyork_merged['Cluster Labels'] == 2, nyork_merged.columns[[1] + list(range(5, nyork_merged.shape[1]))]]    

