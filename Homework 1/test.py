import rosbag

tag_x = []
tag_y = []
tag_z = []

bag = rosbag.Bag('cse668.bag')

read = bag.read_messages()

msg_count = 0

for topic, msg, t in read:
	if topic == "/tag_detections":
		for detection in msg.detections:
			print(detection.pose.pose.position)