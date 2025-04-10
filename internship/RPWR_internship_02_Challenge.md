# Tortugabot the Archaeologist

Collect all treasures on the map. For the challange we need a map. Follow the Setup guide for how to record a map.

## Get the Referee 
The Referee will set the challenge for the internship. It will run on your personal PC. Do the following to get the Referee: 
* `git pull` the repository `artnie/rpwr-assignments`. You will find the code in `internship/src`.
* start the docker container
* create your own ros package. There you can put the referee and your own code. Make the python files executable with `chmod +x *py`
* go to the directory `~/workspace/ros` and build the workspace with `catkin build`. This will be the workspace for your code.
* `source devel/setup.bash`
* remember to `source` this repository automatically when you open a new terminal by putting the above line into your `.bashrc` file

Before you start the Referee, bringt the tortugabot to life. We need the following launchfiles
```bash
# Tortugabot
roslaunch tortugabot_bringup base_and_joy_and_laser.launch
# in another terminal
roslaunch tortugabot_bringup amcl.launch
# in yet another terminal
roslaunch tortugabot_bringup move_base.launch
```
Launch your Docker Container. Then the Referee can be run. Execute this on your personal PC.
```bash
rosrun <YOUR_ROS_PACKAGE> referee.py
```
Check out the TF frames in Rviz.

## World-state and Referee behaviour 

The Referee behaves as follows:
* When the `/base_footprint` frame is close to a treasure or trash, the name of the frame is published to the `/goal_collected` topic
* When it is close to the depot, it drops off all objects and publishes 'unloading' to the  `/goal_collected` topic.
* The tortugabot can only hold 2 treasures. When the robot gets near another treasure, the Referee will not register it.

To keep track how many and which treasures have been picked, implement a subscriber to the `/goal_collected` topic.

Feel free to change the coordinates of the treasures, trashes and depots in `referee.py`


## Move Base
```python
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
```

## Where to start with your own code

* Implement a strategy to collect and store all treasures. There are many possible strategies. Examples: shortest overall travel distance, minimal amount of trash collected, fastest time to complete ...
* Instead of hardcoding the locations and amount of the frames you can randomize it. Then you need a Subscriber to track the amount of treasures availabe and their frame_ids.
* Navigate through difficult parts, like doors.

## Next week
Next week you let the real tortugabot follow the wall and this time collisions have consequences. The avoidance of collisions and the time required to drive along the wall are important. MoveBase is not recommended.
