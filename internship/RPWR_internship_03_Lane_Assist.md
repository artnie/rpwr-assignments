# Recap 

Collect and store all treasures on the map you recorded. Follow the Setup guide for how to record a map. Movement is done by the MoveBase-Client. 

## Startup 

We need the following launchfiles
```bash
# Tortugabot
roslaunch tortugabot_bringup base_and_joy_and_laser.launch
# in another terminal
roslaunch tortugabot_bringup amcl.launch
# in yet another terminal
roslaunch tortugabot_bringup move_base.launch
```
Launch your Docker Container. Then the Referee and your code can be run. Execute this on your personal PC.
```bash
rosrun <YOUR_ROS_PACKAGE> referee.py
rosrun <YOUR_ROS_PACKAGE> <YOUR_CODE>
usw.
```

Now the robot should start moving. Check out the TF frames in Rviz.

## Exam 

For the exam, the robot should show what it got in a live demo. Create a scenario that shows the robot's ability to pick up treasures and trashes and react accordingly. The minimum requirement is that the robot collects at least 2 treasures and on his way is at least one trash that forces the robot to change his movement plan. The robot should move through the door in the hallway at least once. Everything should be done within a reasonable time. This is the minimum requirement and you can add further challenges.

After the demo you have to present your code and explain what you did. Make your code presentable. `rostopic echo /<TOPIC>` can help to visualize what the robot is doing. 

# Next part: Driving with Lane Keeping Assist

No ActionBase-Client! 

You control the robot with the PS3-Controller and have to drive along the hallway. The robot should detect collisions and correct the movement to avoid an accident. There are three collision regions "LEFT", "RIGHT" and "FRONT" like in assignment 5. The correction should be as smooth as possible. You don't want to slow down. Only stop if there is something directly in front of the robot. Driving through a door should still be possible.

The PS3-Controller sends a lot of messages. You have to throttle it to be able to send your movement corrections. 

## Autonomous driving

The robot can switch between two modes. 

First mode is driving with the PS3 Controller and adding a lane keeping assist. The robot should start close to a wall, drive in the hallway, and avoid hitting the wall. 
Optional: Follow the wall by moving closer/further to/from the wall.

The second mode is autonomous driving mode (MoveBase-Client). Driving through the door in the hallway is required. Use the waypint published by the referee. Main focus is on the internl belief state and decision-making: when to go to the depot.
Optional: One way to switch modes is to map an unused button of the PS3-Controller to switch modes. 
