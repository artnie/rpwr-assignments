#!/usr/bin/env python

import rospy
import tf2_ros
import numpy as np
from geometry_msgs.msg import Vector3, TransformStamped
from std_msgs.msg import String
import random

TRUNK_MAX_SIZE = 2
TRASH_AMOUNT = 20
TRASH_INDEX = 3
DISTANCE_TOLERANCE = 0.2

# To choose the frame position, use rviz to find suitable coordinates.
# Open Xpra Desktop
# Open rviz
# In terminal: rostopic echo /clicked_point
# In rviz: Click 'publish point', then click on a place in the map

treasures = [
    ("treasure1", [2.0, 0.0, 0.0]), 
    ("treasure2", [1.0, 0.0, 0.0])
]

trashes = [
    ("trash1", [3.0, 0.0, 0.0]), 
    ("trash2", [-2.0, 0.0, 0.0])
]

depots = [
    ("depot1", [4.0, 0.0, 0.0], "goal"), 
    ("depot2", [-4.0, 0.0, 0.0], "trash")
]

trunk = []

rospy.init_node('control_referee')
rate = rospy.Rate(10)

tf_buffer = tf2_ros.Buffer()
tf_listener = tf2_ros.TransformListener(tf_buffer)
tf_broadcaster = tf2_ros.TransformBroadcaster()

goal_reached_pub = rospy.Publisher('/goal_collected', String, queue_size=1)

def publish_frames():
    for frame in treasures + trashes + depots:
        tf_goal = TransformStamped()
        tf_goal.header.stamp = rospy.Time.now()
        tf_goal.header.frame_id = "map"
        tf_goal.child_frame_id = frame[0]
        tf_goal.transform.translation = Vector3(*frame[1])
        tf_goal.transform.rotation.w = 1.0 

        tf_broadcaster.sendTransform(tf_goal)

def check_frames():
    try:
        for frame in treasures + trashes + depots:
            trans = tf_buffer.lookup_transform("base_footprint", frame[0], rospy.Time()).transform.translation
            distance = np.linalg.norm(np.array([trans.x, trans.y, trans.z]))
            if distance < DISTANCE_TOLERANCE:
                if frame[0].startswith("treasure") and len(trunk) < TRUNK_MAX_SIZE:
                    treasures.remove(frame)
                    trunk.append(frame[0])
                    goal_reached_pub.publish(frame[0])
                    rospy.loginfo(frame[0] + " collected.\nRemaining treasures: " + str(treasures) + "\nTrunk: " + str(trunk))
                elif frame[0].startswith("trash") and len(trunk) < TRUNK_MAX_SIZE:
                    trashes.remove(frame)
                    trunk.append(frame[0])
                    goal_reached_pub.publish(frame[0])
                    rospy.loginfo(frame[0] + " collected." + "\nTrunk: " + str(trunk))
                elif frame[0].startswith("depot") and len(trunk) > 0:
                    rospy.loginfo("Unloading " + str(trunk))
                    trunk.clear()
                    goal_reached_pub.publish("unloading")
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            pass

def trashify():
    global TRASH_INDEX
    while len(trashes) < TRASH_AMOUNT:
        # Adjust min-max values to your map.
        x = random.uniform(-10, 13)
        y = random.uniform(-11, 6)
        
        trashes.append((f"trash{TRASH_INDEX}", [x, y, 0.0]))
        TRASH_INDEX+=1  

if __name__ == '__main__':
    try:
        while not rospy.is_shutdown() and len(treasures + trunk) > 0:
            check_frames()
            trashify()
            publish_frames()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass


