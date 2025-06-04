In this internship you will write code to control Tortugabots on their way through the building. You will work in groups.  

The goal until the end of this internship is a group-presentation of self-implemented navigation, using the given programs. To evaluate your grade, the following aspects are considered:
* Repel: Avoid collisions before they happen.
* Attraction: follow something fixed (e.g. a wall) or dynamic (a person)
* Visualization (of detection/goals/intentions)

Today task on the robot is 
* start the robot, move it with the controller
* record a map with slam 

Furthermore we will brainstorm a few ideas to implement with what we have.

Presentation is given on Wednesday 2nd of July with complementary material. Slides with screenshots are good, a demo video even better. Consider Murphys Law: your live-demo will fail, so prepare backup material to showcase your work.

## Hardware components

Each Tortugabot system consists of multiple parts:
* Hokuyo LiDAR for sensing
* Roboclaw controlling 2 motor wheels (+ 2 more wheels for stability)
* Battery Pack, powering Roboclaw and Hokuyo
* Tortuga Laptop connected to Hokuyo and Roboclaw running their drivers
* PS3 Controller for teleoperation

**Flip the Tortugabot on its back while testing** so it doesn't run away.

## Boot the Tortugabot

Connect the battery to use motors and laser.
* The Roboclaw shows a constant green light. If it is red it needs more power - replace the battery. The green LED flickers for every message sent to the board.
* The Hokuyo LiDAR shows a constant blue LED if powered.
* Check the battery status by pressing the red button on it. 

Login to the Tortugabot laptop:

User: roscourse

PW: 10293847

## Connect remotely

Contain ROS-communication moslty between the tortugabot laptop and the hardware 

With your own laptop you can control the Turtle through the WiFi access point:
SSID: lispcourse
PW: turtlesalltheway

Check your own IPv4 address at the wireless interface. It should be something of the pattern `10.0.1.xx`. If not, you are not connected to the lispcourse network.
```bash
ip a
```
Now check if you can reach the Turtle, let's say tortuga6
```bash
ping 10.0.1.36
```
Connect to the tortuga Laptop via SSH
```bash
ssh roscourse@10.0.1.xx
```
* tortuga2: 10.0.1.33
* tortuga3: 10.0.1.32
* tortuga4: 10.0.1.35
* tortuga5: 10.0.1.34
* tortuga6: 10.0.1.36

In a terminal, start Byobu. This allows every SSH connection to have one terminal to manage the running processes. It will prevent you from having any rogue nodes running in the background.
```bash
# Tortugabot
byobu
```
* F2 - Create new window
* F3 - Move to previous window
* F4 - Move to next Window
* CTRL-D - Delete current window
* F6 - Detach from this session
* F7 - Enter copy/scrollback mode
* F8 - Rename current window

### Roboclaw for base movement

Connect the **Roboclaw** via USB. The socket is available on `ttyACM0`.  Check the availability with
```bash
ls /dev | grep ttyACM0
```
Start the Roboclaw driver
```bash
ros2 launch roboclaw_node roboclaw_launch.py
```
The last message should be `Roboclaw: Starting motor drive`.  It it complains about the `_port`, check the battery and USB connection.

Now check for the `/base/cmd_vel` topic
```bash
ros2 topic list
```
Send a command to test it, press CTRL-C to cancel
```bash
ros2 topic pub /base/cmd_vel geometry_msgs/msg/Twist 'linear:
  x: 0.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.2
' 
```
### PS3 controller for teleoperation

Connect the **PS3 controller** via Bluetooth: 
* Press the PS Button in the middle, 4 LEDs are blinking while searching
* Press again and the LED 1 stays on
* (Use the cable connection to save the controller's battery)

Start the PS3 controller teleop driver
```bash
ros2 launch roboclaw_node joy_teleop_launch.xml
```
The last message should be `Opened joystick: PLAYSTATION(R)3 Controller.  deadzone: 0.500000`. If not, make sure the controller is connected via Bluetooth. Check the topics for `/joy`. 

### Hokuyo LiDAR for sensing

Connect the **Hokuyo** via Ethernet. Set the wired connection to `Hokuyo`.  Check the connection
```bash
ping 192.168.200.11 # For the tortuga4 it is 192.168.0.10
```
Start the Hokuyo driver
```bash
ros2 launch urg_node2 urg_node2.launch.py
```
The last message should be 
`Connected to a network device with single scan. Hardware ID: H1411496`
Check the topics for `/scan`.

Throttle the scan messages down to 10hz
```bash
ros2 run topic_tools throttle messages /scan 10.0
```
Check the topics frequency
```bash
ros2 topic hz /scan
ros2 topic hz /scan_throttle
```
### Connect base and laser TF

Publish a static transform on TF between the `base_footprint` and the `laser`
```bash
ros2 run tf2_ros static_transform_publisher --frame-id base_footprint --child-frame-id laser
```
### RViz

On the turtlebot laptop, start RViz. Visualize TF and scan in RViz.

## Record a map of the floor

Launch a transform for the base_link as it is required for nav2
```bash
ros2 run tf2_ros static_transform_publisher --frame-id base_footprint --child-frame-id base_link
```
Start the navigation
```bash
ros2 launch nav2_bringup navigation_launch.py
```
Start SLAM
```bash
ros2 launch slam_toolbox online_async_launch.py
```
Start RViz on the tortuga laptop
```bash
ros2 run rviz2 rviz2 -d /opt/ros/jazzy/share/nav2_bringup/rviz/nav2_default_view.rviz
```
Drive around with the teleop controller. When you are done, save the map with 
```bash
ros2 run nav2_map_server map_saver_cli -f map
```
Put your two map files into `~/tortugabot_ws/src/tortugabot/tortugabot_bringup/map/`

Now with an updated map of the floor, start the map server:
```bash
ros2 launch tortugabot_bringup map_server.launch.py
```

In RViz add a new Map visualization.
* set the Topic to `/map`
* set the Topic Durability Policy to `Transient Local`
* set the global Fixed Frame to `/map`
* disable+enable the Map visualization

---
## Additional: ROS over WiFi

First of all, don't. ROS2 invokes a lot of overhead and floods the network with discovery messages until denial of service, when DDS is not configured properly.

Traffic statistics:
* Tortugabot localhost-only - 400 packages/minute
* Tortugabot + Rviz Remote + TF - 2.000 packages/minute 
* Tortugabot + Rviz Remote + TF + /scan - 12.000 packages/minute 

If you need to, install [[RMW - Cyclone DSS]] and share the same ROS_DOMAN_ID with the tortugabot.

Use wireshark to monitor the communication.