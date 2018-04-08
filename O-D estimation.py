
# coding: utf-8

# In[203]:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial.distance import cdist



# <h2>Remove estimated intersections in route:</h2>

# In[330]:

def remove_inter(df):
    clean_df = []

    for name, group in df.groupby(["id"]):#, df.time.dt.day]):
        #print(name, group)
        group["cluster"] = (group.time.diff() > pd.Timedelta(minutes=10)).cumsum()
    
        clean_df += [group.groupby(group.cluster).first()]
        #print(group.groupby(group.cluster).first())#.sort_values(group.time).head(1))
        #for name, g in group.groupby(group.cluster):
            #print(name, g)
        #print()
        #print()

    clean = pd.concat(clean_df)
    return clean.drop("cluster", axis=1)


# <h2>Estimate Destination:</h2>

# In[331]:

def get_OD(clean_df):  
    OD = []
    for name, group in clean_df.groupby(clean_df.id):
        group_dest = group.copy()
        group.columns = columns_orig
        OD += [pd.concat([group, group_dest.shift(-1)], axis=1).drop(["time", "id"], axis=1)] 

    return pd.concat(OD)




# <h2>Clustering Metric:</h2>

# In[332]:

def bundling_metric(X):
    
    def pairwise(l1,l2):
        
        return np.sum(np.dot(np.sum(np.square(l1 - l2)),
                             np.log(1 + np.abs((l1[:2] - l2[:2])**2 - (l1[2:] - l2[2:])**2))))
    
    return cdist(X, X, metric=pairwise)


# <h2>Clustering</h2>

# In[333]:

def get_clusters(X, n_clusters, metric):
    X = metric(X)
    model = AgglomerativeClustering(n_clusters=n_clusters, linkage="average", affinity='precomputed')
    model.fit(X)
    
    #X[model.labels_ == l]
    
    return model.labels_


# In[334]:

def cluster(df, n_clusters, freq=False):
    df = df.dropna(axis=0, how='any')
    clustered = []

    if freq:
        groups = []
        for name, group in df.groupby([df.time_orig.dt.hour]):

            if group.shape[0] == 1:
                continue
       
            group["cluster"] = get_clusters(group.loc[:,"lat_orig":"lon"].values, n_clusters, bundling_metric)
            groups += [group]
            grouped = group.groupby(group.cluster)
            representative = []
            for name, g in grouped:
                representative += [[g.lat_orig.mean(), g.long_orig.mean(), g.lat.mean(), g.lon.mean(), g.shape[0]]]
        #representative = grouped.first()
        #representative["count"] = grouped.size()
            clustered += [representative]
        return clustered, groups
    else:
        df["cluster"] = get_clusters(df.loc[:, "lat_orig":"lon"].values, n_clusters, bundling_metric)

        grouped = df.groupby(df.cluster)
        representative = []
        for name, g in grouped:
            representative += [[g.lat_orig.mean(), g.long_orig.mean(), g.lat.mean(), g.lon.mean(), g.shape[0], name]]
        clustered += [representative]
    #return pd.concat(clustered)
        return clustered, df


# In[335]:

def plot_cluster(cluster):
    
    ax = cluster.plot.scatter("lat_orig", "long_orig")
    cluster.plot.scatter("lat", "lon", ax=ax)
    plt.show()
    


# In[336]:


#plot_cluster(clusters[0])


# In[337]:

def cluster_on_map(clustered, original, df=True):


    print(clustered)
    colors = sum([["green", "blue", "red", "orange", "brown", "yellow",
                   "white"] for i in range(1000)], [])
    if df:
        m = folium.Map(location=[clustered.lat.mean(), clustered.lon.mean()])
    else:
        m = folium.Map(location=[sum([cl[0] for cl in clustered]) / len(clustered), sum([cl[1] for cl in clustered])/len(clustered)])



    i = 0
    if df:
        for index, row in clustered.iterrows():

            folium.features.PolyLine([row.loc["lat_orig":"long_orig"].values.tolist(),
                                       row.loc["lat":"lon"].values.tolist()], color=colors[i], weight=row["count"]).add_to(m)
            i += 1
        return m

    for r in clustered:
        folium.features.PolyLine([r[:2],
                                  r[2:4]], color=colors[i], weight=r[4]).add_to(m)

        #for name, group in original.groupby(original.cluster):
         #   if name == r[5]:
         #       for index, row in group.iterrows():
          #          folium.Marker([row.lat, row.lon], icon=folium.Icon(color=colors[i])).add_to(m)
           #         folium.Marker([row.lat_orig, row.long_orig], icon=folium.Icon(color=colors[i])).add_to(m)

        #folium.features.PolyLine([row.loc["lat_orig":"long_orig"].values.tolist(),
        #                           row.loc["lat":"lon"].values.tolist()], color=colors[i], weight=row["count"]).add_to(m)
        i+=1
    return m


# In[338]:

# In[326]:

import pymongo
import pandas as pd

def getDbMetrics():

    client = pymongo.MongoClient()
    db = client['hack']
    collection = db.data
    aux = collection.find()
    col = ["id_orig", "time_orig", "lat_orig", "long_orig", "lat", "lon"]
    listona =[]

    for item in aux:
        listona.append([item['id_orig'],item['time_orig'],item['lat_orig'],item['long_orig'],item['lat'], item['lon']])

    df = pd.DataFrame(listona, columns = col)


    return df


a = getDbMetrics()


toy_data = [[1, "1:3:12", -23.613, -46.0443],
            [1, "1:3:13", -23.613, -46.6443],
            [1, "1:3:50", -23.713, -46.6443],
            [1, "1:4:12", -23.814, -46.6443],
            [1, "1:4:13", -23.613, -46.0443],
            [1, "1:4:50", -23.713, -46.0443],
            [2, "1:3:12", -23.313, -46.9443],
            [2, "1:3:13", -23.513, -46.9443],
            [2, "1:3:50", -23.713, -46.9443],
            [2, "1:4:12", -23.314, -46.9443],
            [2, "1:4:13", -23.513, -46.9443],
            [2, "1:4:50", -23.713, -46.9443]]

columns = ["id", "time", "lat", "lon"]
columns_orig = ["id_orig", "time_orig", "lat_orig", "long_orig"]


# In[327]:

df = pd.DataFrame(toy_data, columns=columns)


# In[328]:

a.time_orig = pd.to_datetime(a.time_orig, format='%Y-%m-%d %H:%M')#format='%Y-%m-%d %H:%M:%S')

df.time = pd.to_datetime(df.time, format='%d:%H:%M')#format='%Y-%m-%d %H:%M:%S')
#a.

# print(df)
# print(get_OD(remove_inter(df)))
# print(a)

# clusters2 = cluster(get_OD(remove_inter(df)), 2)
#print a
clusters, orig = cluster(a, 4)

m = cluster_on_map(clusters[0], orig, df=False)
m.save("map3.html")

a["count"] = [1 for i in range(a.shape[0])]
m = cluster_on_map(a, a)
m.save("map2.html")

# In[ ]:



