#!/usr/bin/env python

import rospy
import tf2_ros
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

rospy.init_node('control_navigator')
rate = rospy.Rate(10)

tf_buffer = tf2_ros.Buffer()
tf_listener = tf2_ros.TransformListener(tf_buffer)
client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
client.wait_for_server()

def goal_collected_callback(msg):
    pass

rospy.Subscriber("/goal_collected", String, goal_collected_callback)

if __name__ == '__main__':
    try:
        trans = tf_buffer.lookup_transform('map', "treasure1", rospy.Time())
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position = trans.transform.translation
        goal.target_pose.pose.orientation = trans.transform.rotation

        client.send_goal(goal)
        client.wait_for_result()
   
    except (tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException, tf2_ros.LookupException, rospy.ROSInterruptException):
        pass