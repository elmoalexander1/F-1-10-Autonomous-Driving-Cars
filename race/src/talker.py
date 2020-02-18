#!/usr/bin/env python

import rospy
from race.msg import drive_values
from race.msg import drive_param
from std_msgs.msg import Bool


"""
What you should do:
 1. Subscribe to the keyboard messages (If you use the default keyboard.py, you must subcribe to "drive_paramters" which is publishing messages of "drive_param")
 2. Map the incoming values to the needed PWM values
 3. Publish the calculated PWM values on topic "drive_pwm" using custom message drive_values
"""


def talker():


    def callback(drive_param_data):

        msg = drive_values()
        msg.pwm_drive = int((drive_param_data.velocity + 100) * 32.77 + 6554)
        msg.pwm_angle = int((drive_param_data.angle + 100) * 32.77 + 6554)

        print("---------")
        print("pwm_drive: " + str(msg.pwm_drive))
        print("pwm_angle: " + str(msg.pwm_angle))
        print("---------")
        print()

        pub.publish(msg)

        rate.sleep()


    rospy.init_node('talker', anonymous=True)

    rate = rospy.Rate(50) #TODO: figure out if appropriate (or even if we should have at all)

    pub = rospy.Publisher("drive_pwm", drive_values)

    print("NODE STARTED")

    rospy.Subscriber("drive_parameters", drive_param, callback)

    rospy.spin()

if __name__ == "__main__":
    talker()
