import rosbag
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
odom_x = []
odom_y = []
odom_z = []
tag_x = []
tag_y = []
tag_z = []

bag = rosbag.Bag('cse668.bag')

read = bag.read_messages()

msg_count = 0

for topic, msg, t in read:
	msg_count += 1
	if (msg_count % 100)==0:
		#print "Topic ",topic,"\n\n", "Message ", msg, "\n\n", "Timestamp ", t, "\n\n\n"
		if topic == "/odom":
			odom_x.append(msg.pose.pose.position.x)
			odom_y.append(msg.pose.pose.position.y)
	if topic == "/tag_detections":
		for detection in msg.detections:
			tag_x.append(detection.pose.pose.position.x)
			tag_y.append(detection.pose.pose.position.y)
			tag_z.append(detection.pose.pose.position.z)


odom_x = pd.Series(odom_x)
odom_y = pd.Series(odom_y)
odom_z = pd.Series(odom_z)

tag_x = pd.Series(tag_x)
tag_y = pd.Series(tag_y)
tag_z = pd.Series(tag_z)

# sns.regplot(x=tag_x,y=tag_y,fit_reg=False)
# plt.show()
