import rosbag
bag = rosbag.Bag('cse668.bag')
topics = bag.get_type_and_topic_info()[1].keys()
print topics
types = []
for i in range(0,len(bag.get_type_and_topic_info()[1].values())):
    types.append(bag.get_type_and_topic_info()[1].values()[i][0])