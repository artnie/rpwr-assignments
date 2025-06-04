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

## Download files from remote

On your own machine, copy the Bagfile (or map) from the remote.

Assuming the Bag is on IP 10.0.1.34 on the `Desktop`:
```bash
scp -r roscourse@10.0.1.34:Desktop/rosbag* .
```
### Or: use midnight commander

`mc` is a command-line file explorer that allows for ssh connections. 
```bash
sudo apt install mc
```
`Left` > `Shell Link` > `roscourse@10.0.1.34`

Use F5 to copy from side to side.
