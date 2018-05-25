#! /usr/bin/env python



import os
import multiprocessing as mp

import rospy
from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelState
import time

#adjust as much as you need, limited number of physical cores of your cpu
numberOfCpuCore_to_be_used = 2

#######ROS PARAMETERS############
x = 0.0
y = 0.0
x_vel = 0.0
y_vel = 0.0
theta = 0.0
speed = Twist()


class Worker(mp.Process):
    def __init__(self, someGlobalNumber, name):
        super(Worker, self).__init__()
        self.name = 'w%i' % name
        self.port = name
        self.global_number = someGlobalNumber
    def run(self):

        #to parallelizing
        os.environ['ROS_MASTER_URI'] = "http://localhost:1135" + str(self.port) + '/'
        rospy.init_node('parallelSimulationNode')
        
        def currentState(msg):
            global x
            global y
            global theta
            global x_vel
            global y_vel
            

            x = msg.pose[msg.name.index('mobile_base')].position.x
            y = msg.pose[msg.name.index('mobile_base')].position.y
            x_vel = msg.twist[msg.name.index('mobile_base')].linear.x
            y_vel = msg.twist[msg.name.index('mobile_base')].linear.y
            rot_q = msg.pose[msg.name.index('mobile_base')].orientation
            (roll,pitch,theta) = euler_from_quaternion ([rot_q.x,rot_q.y,rot_q.z,rot_q.w])

          
            
        sub = rospy.Subscriber("/gazebo/model_states",ModelStates,currentState)
        pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)

        rate = rospy.Rate(10)








        #file to keep episode numbers when agent accomplished to navigate
        
       
        while not rospy.is_shutdown(): 
            speed.linear.x = 0.4
            speed.angular.z = 0.5
            if self.port % 2 == 0:
                speed.angular.z = -0.5

            #Publishing speed Values to generate new states#######################################
            pub.publish(speed)
            with self.global_number.get_lock():
                self.global_number.value += 1
            print self.name, 'global_number: ', self.global_number.value
            rate.sleep()




               



if __name__ == "__main__":
    #initializing some shared values between process
    global_number = mp.Value('i', 0)

    # parallel training
    workers = [Worker(global_number, i) for i in range(numberOfCpuCore_to_be_used)]
    [w.start() for w in workers]
    [w.join() for w in workers]