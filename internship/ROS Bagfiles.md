Bagfiles can record topic data, so you can work on it locally, independently and without using constantly needing the robot. Use this, for example, to test a /scan filter or classifier before bringing it on the robot. 

Use Bagfiles to record all topics.
```bash
ros2 bag record --all-topics
```
or specific ones
```bash
ros2 bag record --topics /scan
```
Replay them with in a loop (-l)
```bash
ros2 bag play rosbag_yyyy_mm_dd-hh_mm_ss -l
```
Get into 
```bash
ros2 bag info rosbag_yyyy_mm_dd-hh_mm_ss
```