# Group Assignment Exam 

The exam is due on the 2nd of July. Every team has 20 minutes for their presentation.

You get credit for functionality you added depending on the complexity. The general areas are:
* Repel: Avoid collisions before they happen.
* Attraction: follow something fixed (e.g. a wall) or dynamic (a person)
* Visualization (of detection/goals/intentions)

The robot should show what it got in a live demo. Create a suitable scenario that shows the robots abilities. Schedule your time appropriately and move on to backup-material of the live-demo does not work. 

In the following are a few examples for your challenges. 
# Challenges

Solve 3 challenges. 

Either **Lane Keeping Assist** or **Follow a person** must be implemented. Choose 2 more challenges from the list.

**Visualize** your contribution appropriately. If you find a way of visualization more suitable than the proposed one, go for it.

Tip: Record [[ROS Bagfiles]] to work offline.
## Lane Keeping Assist
You control the robot with the PS3-Controller and have to drive along the hallway. The robot should detect collisions and correct the movement to avoid an accident. There are three collision regions "LEFT", "RIGHT" and "FRONT" like in assignment 4. The correction should be as smooth as possible. You don't want to slow down. Only stop if there is something directly in front of the robot. 

The PS3-Controller sends a lot of messages. You have to throttle it to be able to send your movement corrections. 
### Visualize
Publish a marker for potential collisions to the left, right and front.

## Follow a person
The robot can detect a person in front of them, and adjusts its position such that it is always facing the person. The PS3-controller should only be used for linear velocity to drive forward, while the angle is automatically detected.
### Visualize
The direction of the person the robot are following.

### Stay in line!
Keep the distance to the person in front of you. If it moves forward, follow it but stop at a save distance. Allow forwards cmd_vel if appropriate.
#### Visualize
The person to follow.

### Knock-Knock
Put the robot in front of a door. Stand still as long the door is closed. When the door is open and the path is free, drive through the door without collision. Block forwards cmd_vel until door is open.
#### Visualize
If the door is open of closed.

### Filter the scan
Write a filter for the /scan topic to reduce noise. This involves reducing the resolution by migrating similar datapoints close to each other. Also remove points that are too close - as for the pole reflections - or too far away. Calculations must be quick to filter in real time. The /scan topic runs at 40Hz. 
#### Visualize
Compare the old and new scan.

### Localization
Launch the nav2 localization from your own launchfile using your own map. Get inspiration from here: https://github.com/secorolab/turtlebot4/blob/jazzy/turtlebot4_navigation/launch/localization.launch.py 
#### Visualize
Move around showing the robot on the map.

### Move to pose
With the localization available, move to a goal pose on the map. To move around a corner, re-use behavior from the Lane-Keeping Assistant, or integrate the move-base library.
#### Visualize
Path to goal.
