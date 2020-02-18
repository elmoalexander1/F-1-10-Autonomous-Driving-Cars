#!/usr/bin/env python
import sys
import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input


##	Input: 	data: Lidar scan data
##			theta: The angle at which the distance is requried
##	OUTPUT: distance of scan at angle theta


# Some useful variable declarations.
angle_range = 240	# sensor angle range of the lidar
car_length = float(sys.argv[2])	# distance (in m) that we project the car forward for correcting the error. You may want to play with this
desired_trajectory = float(sys.argv[1])	# distance from the wall (left or right - we cad define..but this is defined for right). You should try different values
vel = 15 		# this vel variable is not really used here.
error = 0.0
pub = rospy.Publisher('error', pid_input, queue_size=10)
max_length = 5

theta1 = int(sys.argv[3])
theta2 = int(sys.argv[4])


# Find the index of the arary that corresponds to angle theta.
# Return the lidar scan value at that index
# Do some error checking for NaN and ubsurd values
## Your code goes here
def getRange(data,theta):

    ray_index = (30 + theta) * (len(data.ranges)/240)
    
    if (math.isnan(data.ranges[ray_index])):
        return max_length
    else:
        return data.ranges[ray_index]


def calc_error(des_traj,theta, b, a):

    swing = math.radians(theta)

    # print("a: " + str(a))
    # print("b: " + str(b))
    # print("theta: " + str(theta))
    # print("swing: " + str(swing))

    ## Your code goes here to compute alpha, AB, and CD..and finally the error.

    alpha = math.atan( (a * math.cos(swing) - b ) / (a * math.sin(swing) ) ) # DANGER: wrong equation
    # alpha = math.atan2(a * math.cos(swing)- b , a * math.sin(swing))

    AB = b * math.cos(alpha)

    CD = AB + car_length * math.sin(alpha) 
    
    error = des_traj - CD
    
    return error


def callback(data):
    b1 = getRange(data,0)	# Note that the 0 implies a horizontal ray..the actual angle for the LIDAR may be 30 degrees and not 0
    a1 = getRange(data,theta1) 
    err1 = calc_error(desired_trajectory, theta1, b1, a1 )

    b2 = getRange(data,0)	# Note that the 0 implies a horizontal ray..the actual angle for the LIDAR may be 30 degrees and not 0
    a2 = getRange(data,theta2) 
    err2 = calc_error(desired_trajectory, theta2, b2, a2 )

    # print("a: " + str(a))
    # print("b: " + str(b))
    # print("swing: " + str(swing))
    # print("alpha: " + str(alpha))
    # print("AB: " + str(AB))
    # print("CD: " + str(CD))
    
    print("error1: " + str(err1))
    print("error2: " + str(err2))

    error = .35*err1 + .65*err2

    # TODO: if EC then take into account prev err and change car_length

    msg = pid_input()
    msg.pid_error = error*-1		# this is the error that you wantt o send to the PID for steering correction.
    msg.pid_vel = vel		# velocity error is only provided as an extra credit field. 
    pub.publish(msg)
	

if __name__ == '__main__':
    print("Laser node started")
    rospy.init_node('dist_finder',anonymous = True)
    rospy.Subscriber("scan",LaserScan,callback)
    rospy.spin()
