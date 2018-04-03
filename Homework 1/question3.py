import rosbag
from sklearn.cluster import KMeans
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

pairs = []

bag = rosbag.Bag('cse668.bag')

read = bag.read_messages()

msg_count = 0
center_count = 0
tag_ids = []

odom_x = []
odom_y = []
odom_z = []
tag_x = []
tag_y = []
tag_z = []


for topic, msg, t in read:
	if topic == "/odom":
		buffered = msg
	elif topic == "/tag_detections":
		pairs.append({"odom": buffered, "tag": msg})

for pair in pairs:
	
	tag = pair["tag"]
	for data in tag.detections:
		if data.id not in tag_ids:
			tag_ids.append(data.id)

		tag_x.append(data.pose.pose.position.x)
		tag_y.append(data.pose.pose.position.y)
		tag_z.append(data.pose.pose.position.z)

	odom = pair["odom"]
	odom_x.append(odom.pose.pose.position.x)
	odom_y.append(odom.pose.pose.position.y)
	odom_z.append(odom.pose.pose.position.z)

tag_coords = np.asarray(zip(tag_x, tag_z))
kmeans = KMeans(n_clusters=len(tag_ids)).fit(tag_coords)
tag_coords = pd.DataFrame(kmeans.cluster_centers_)
tag_x = tag_coords.iloc[:,0]
tag_z = tag_coords.iloc[:,1]

odom_x = pd.Series(odom_x)
odom_y = pd.Series(odom_y)
odom_z = pd.Series(odom_z)

tag_x = pd.Series(tag_x)
tag_y = pd.Series(tag_y)
tag_z = pd.Series(tag_z)

sns.regplot(x=tag_x,y=tag_z,fit_reg=False)
sns.regplot(x=odom_x,y=odom_y,fit_reg=False)
plt.show()
