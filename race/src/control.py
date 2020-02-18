#!/usr/bin/env python
import rospy
import sys
from race.msg import drive_param
from race.msg import pid_input


# kp = 14.0
# kd = 0.09
# servo_offset = 18.5	# zero correction offset in case servo is misaligned. 
# prev_error = 0.0 
# TODO: might need to decrease
# vel_input = 25.0	# arbitrarily initialized. 25 is not a special value. This code can input desired velocity from the user.
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)


if __name__ == '__main__':


    def control(data):
        global kp
        global kd
        global prev_angle
        global prev_error
        global vel_input
        ## Your code goes here
        # 1. Scale the error
        # data.pid_error *= 10 
        # 2. Apply the PID equation on error to compute steering
        pid = data.pid_error * kp + kd * (data.pid_error - prev_error)
        print("pid: " + str(pid))
        # 3. Make sure the steering value is within bounds for talker.py
        angle = pid
        prev_error = data.pid_error

        print("angle:" + str(angle))

        if angle<-100:
            angle = -100
        if angle>100:
            angle = 100

        prev_angle = angle

        msg = drive_param()
        msg.velocity = vel_input	
        msg.angle = angle
        pub.publish(msg)


    global kp
    global kd
    global prev_angle
    global vel_input
    print("Listening to error for PID")
    prev_angle = 0
    prev_error = 0
    
    kp = float(sys.argv[1])
    print("kp set to %f" % kp)

    kd = float(sys.argv[2])
    print("kd set to %f" % kd)

    vel_input = float(sys.argv[3])
    print("vel_input set to %f" % vel_input)

    rospy.init_node('pid_controller', anonymous=True)
    rospy.Subscriber("error", pid_input, control)
    rospy.spin()
