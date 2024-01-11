Hello everyone. In this intership you will write code to control Tortugabots on their way through the building. You will work in pairs - two people form a group. Each group can work on the turtles every Thursday afternoon. In the 5th week the turtles will be let loose to search for treasures.

## Lecture 1 - Remote control tortuga
The Tortugabot System consists of multiple parts:
* Hokuyo Laser Sensor for navigation
* Roboclaw controlling 2 motor wheels (+ 2 more wheels for stability)
* Battery Pack, powering Roboclaw and Hokuyo
* Tortuga Laptop connected to Hokuyo and Roboclaw, running ROSCORE and drivers
* Your Laptop, communicating with the Tortuga Laptop over WiFi
* PS3 Controller for Teleoperation

### Boot the Tortugabot
**Flip the Tortugabot on its back while testing** so you can work with it comfortably.

On the Tortugabot, connect the battery pack. Login to the laptop with the lispcourse user. The password is 10293847. Connect the laptop to the Hokuyo via LAN, and to the Roboclaw via USB. Make sure that the LAN connection says 'Hokuyo'. Activate the PS3 Controller to let it connect to the laptop via bluetooth. It will blink all 4 LEDs while searching and light the LED next to 1 when its connected. 

The file at `/home/lispcourse/.bashrc` is your config file for each new terminal. Add a few default values here.  Edit the `.bashrc` file and put the following at the bottom:
```bash
source /home/arthur/ros_ws/devel/setup.bash

export ROS_IP='<Tortugabot IP>'
export ROS_HOSTNAME=$ROS_IP
export ROS_MASTER_URI="http://$ROS_IP:11311"
```
Replace `<Tortugabot IP>` with the IP of the Tortugabot laptop. Make sure it's connected with the lispcourse WiFi, then check the IP with `ifconfig`. Open a new terminal and run `echo $ROS_MASTER_URI` to see if the changes are applied.

In one terminal run `roscore`, then open another terminal and run
```bash
# Tortugabot
roslaunch tortugabot_bringup base_and_joy_and_laser.launch
``` 
This will run the drivers for Roboclaw, Hokuyo and the PS3 Controller. Check the console for any errors. You should be able to move the Tortugabot with the Controller now: Hold L1 while using the left and right analog sticks.

### Connect to the Tortugabot remotely
Your personal laptop and the Tortugabot laptop communicate via ROS. For that they need to be in the same WiFi network. Make sure that both PCs are in the same WiFi. You will communicate with the Tortugabot via the Docker Image.
```yaml
version: '3'
services:
  pycram:
    image: intel4coro/artnie-2drpwr-2dassignments-a6f480:24885d1d20a2dc7df20203b27e4770ee22c29095
    build:
      context: .
      dockerfile: ./Dockerfile
    stdin_open: true
    tty: true
    ports: 
      - 8888:8888
    privileged: true
    volumes:
      - ./:/home/jovyan/work

    # for windows and mac, use 'network_mode: bridge'
    # network_mode: host
    # environment:
    #   - ROS_IP=localhost  # change localhost to your wifi IP
    #   - ROS_MASTER_URI=http://localhost:11311  # change 'localhost' to TURTLE IP
```
* `ROS_MASTER_URI` points to the roscore address. Find the IP of your Tortugabot with ifconfig
* `ROS_IP`, `ROS_HOSTNAME` is your personal laptops IP. Use ifconfig in the Docker Image

Connect to your Docker container
```bash
# Personal PC
docker exec -it cram_headless /bin/bash
```  
In the container, check if you can see the Tortugabot roscore
```bash
# Docker
rostopic list
```
If you can't, check your WiFi, then try to ping the Tortugabot laptop
```bash
# Docker
ping 192.168.101.<IP suffix of your tortuga>
```
If that works, check if the Tortugabot laptop is actually running a roscore. Double check your ROS_MASTER_URI with 
```bash
# Docker
echo $ROS_MASTER_URI
```

### Move the robot remotely
Make sure the Tortugabot moves through teleoperation from the PS3 Controller.

In the Docker container, check the rostopics for cmd_vel
```bash
# Docker
rostopic list | grep cmd_vel
```
If it shows the topic, check it out with
```bash
# Docker
rostopic echo /base/cmd_vel
```
and use the PS3 Controller so send some messages. Now send your own message with
```bash
# Docker
rostopic pub /base/cmd_vel TAB TAB 
```
Enter some value or rotational velocity around the Z-Axis and see the robot move. By design of the Tortugabot it can only process a linear velocity along its X-Axis, and angular velocity around the Z-Axis.

### Connect via SSH

From the Docker container you can connect to the Tortugabot via SSH:
```bash
# Docker
ssh lispcourse@192.168.101.<IP suffix of your Tortuga>
```
Enter the password 10293847 and you're in!

Since you want to launch multiple processes you should run
```bash
# Tortugabot
byobu
```

### Record a map of the ground floor
https://ai.uni-bremen.de/wiki/hardware/createmap 

Here you can find the usual approach to record a map. In the process the Tortugabot will do Simulateous Localization and Mapping (SLAM), combining its odometry (estimate of wheel rotation) and the laser sensor for orientation. While moving the Tortugabot with the PR3 controller, it explores more and more of the environment to build a map.

Place the Tortugabot at a starting position and turn its X-Axis accurately towards the direction it should move. This makes it easier later, when refining the map. The launch the launchfile for the base, so you are able to move the Tortugabot with your controller. Launching this will set the starting position of your robot.
```bash
# Tortugabot
roslaunch tortugabot_bringup base_and_joy_and_laser.launch
```
You can find the launchfile for mapping on the Tortugabot
```bash
# Tortugabot
roslaunch tortugabot_bringup gmapping.launch
```
Open up Rviz on your personal PC and visualize the progress of the map, laser data and TF (see screenshot further below). Move the Tortugabot around, carefully and slowly. When you are done, safe the recorded map:
```bash
# Tortugabot
rosrun map_server map_saver
```
This wil drop two files into your current location: `map.pgm` and `map.yaml`. Copy the files to the location of the Adaptive Monte-Carlo Localization (AMCL) package.
```bash
# Tortugabot
cp map* /home/arthur/ros_ws/src/tortugabot/tortugabot_bringup/maps/
```
Then adjust the launchfile for AMCL
```bash
# Tortugabot
roscd tortugabot_bringup/launch
nano amcl.launch
```
Change the map file loaded to yours.

Change your map manually if you need to, e.g. when a corridor is recorded shorter than it actually is. Copy a backup of your map and start refining it in. Install gimp or inkscape to edit the image.

When you have the map properly set up, run AMCL to make it localize.
```bash
# Tortugabot
roslaunch tortugabot_bringup amcl.launch
```

### RViz Setup
Hit the 'Add' button in the bottom left corner and add  TF, Map and LaserScan. In TF you can adjust the marker size. Map need the Topic `/map` and LaserScan the Topic `/scan`
![[rviz_setup.png]]
2D Pose Estimate, the button with the green arrow in the head row, can set the robots position on the map. Click the button, then click&drag on the map to set the point and orientation.

Save the config file.

### Move Base action server
Move Base needs the launchfiles  `base_and_joy_and_laser` and `amcl` to be running. Start the server like this:
```bash
# Tortugabot
roslaunch tortugabot_bringup move_base.launch
```
In RViz add
* another map, showing the global map topic
* then another one showing the local map
* the path planner

Next to the button 2D Pose Estimate there is 2D Nav Goal with a red arrow. Use that to send commands to the move base server.
