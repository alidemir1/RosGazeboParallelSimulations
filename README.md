# RosGazeboParallelSimulations
Parallel Gazebo Simulations with ROS

![Parallel_Simulations](https://github.com/alidemir1/RosGazeboParallelSimulations/master/parallelsim.gif)

## How to Run
* First run shell files (gazeboSimulation0.sh and gazeboSimulation1.sh) under startSimulations folder on different Terminals

* Then run parallelSimulationNode.py on another terminal. So you should have 3 different terminal running scripts at the same
time.

## Requirements
* Python 2.7
* ROS (tried on Kinetic)

And if you don't have kobuki run below command change ${ROS_DISTRO} with your ROS distribution.

```
sudo apt-get install ros-${ROS_DISTRO}-kobuki-gazebo 
```
