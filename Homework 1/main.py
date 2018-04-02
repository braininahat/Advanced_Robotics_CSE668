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
	# msg_count+=1
	# if (msg_count%2)==0:
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

















# 	msg_count += 1
# 	if (msg_count % 100)==0:
# 		#print "Topic ",topic,"\n\n", "Message ", msg, "\n\n", "Timestamp ", t, "\n\n\n"
# 		if topic == "/odom":
# 			odom_x.append(msg.pose.pose.position.x)
# 			odom_y.append(msg.pose.pose.position.y)
# 	if topic == "/tag_detections":
# 		for detection in msg.detections:
# 			tag_x.append(detection.pose.pose.position.x)
# 			tag_y.append(detection.pose.pose.position.y)
# 			tag_z.append(detection.pose.pose.position.z)


odom_x = pd.Series(odom_x)
odom_y = pd.Series(odom_y)
odom_z = pd.Series(odom_z)

tag_x = pd.Series(tag_x)
tag_y = pd.Series(tag_y)
tag_z = pd.Series(tag_z)

sns.regplot(x=tag_x,y=tag_z,fit_reg=False)
sns.regplot(x=odom_x,y=odom_y,fit_reg=False)
plt.show()
