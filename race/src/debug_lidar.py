#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan


def talker():
    pub = rospy.Publisher('scan', LaserScan, queue_size=10)
    rospy.init_node('debug_lidar', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    print("NODE STARTED: ")
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        # rospy.loginfo(hello_str)
        # pub.publish(hello_str)

        arr = [0 for i in range(240)]
        arr[30] = .5
        arr[80] = .7778

        msg = LaserScan() 
        msg.ranges = arr
        pub.publish(msg)

        rate.sleep()
    print("NODE STOPPED: ")


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
