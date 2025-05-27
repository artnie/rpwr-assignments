The ROS MiddleWare (RMW) decides about communication protocols on UDP-level. CycloneDDS is recommended oder FastDDS for WiFi and Navigation. The turtlebots have CycloneDDS as default.

Install Cyclone ROS middleware via APT
```bash
sudo apt install ros-jazzy-rmw-cyclonedds-cpp
```
Create a config file `cyclonedds.xml` and adjust the `NetworkInterface` name to the interface with which you connect to the robot
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<CycloneDDS xmlns="https://cdds.io/config" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://cdds.io/config https://raw.githubusercontent.com/eclipse-cyclonedds/cyclonedds/master/etc/cyclonedds.xsd">
    <Domain Id="any">
        <General>
            <Interfaces>
                <NetworkInterface name="wlp4s0"/>
            </Interfaces>
            <AllowMulticast>true</AllowMulticast> 
        </General>      
    </Domain>
</CycloneDDS>
```
Check your interfaces with
```
ip a
```
and pick the one for wifi, usually starting with w.

Use cyclone in the .bashrc
```bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI="${HOME}/cyclonedds.xml"
```
If ROS was already running, kill the daemon to activate the RMW change
```bash
ros2 daemon stop
```
Check the RMW in use with
```bash
ros2 doctor --report
```
## Un-use

If you want to go back to the default Fast DDS
```bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
```