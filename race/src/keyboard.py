#!/usr/bin/env python

import rospy
from race.msg import drive_param # import the custom message
import curses
forward = 0;
left = 0;

stdscr = curses.initscr()
stdscr.nodelay(True)
curses.cbreak()
stdscr.keypad(1)
rospy.init_node('keyboard_talker', anonymous=True)
pub = rospy.Publisher('drive_parameters', drive_param)

stdscr.refresh()
rate = rospy.Rate(50) #TODO: figure out if appropriate (or even if we should have at all)

print("NODE STARTED")

# count = 0
key = ''
while key != ord('q'):
    rate.sleep()

    key = stdscr.getch()
    curses.flushinp()

    stdscr.refresh()
    
    # fill in the conditions to increment/decrement throttle/steer

    if key == curses.KEY_UP:
        forward += .1
    if key == curses.KEY_DOWN:
        forward -= .1
    if key == curses.KEY_LEFT:
        left += .1
    if key == curses.KEY_RIGHT:
        left -= .1

    if forward > 100:
        forward = 100
    elif forward < -100:
        forward = -100

    if left > 100:
        left = 100
    elif left < -100:
        left = -100

    if key == curses.KEY_DC:
        # this key will center the steer and throttle
        forward = 0
        left = 0

    if not (key == curses.KEY_DC or key == curses.KEY_UP or key == curses.KEY_DOWN or key == curses.KEY_LEFT or key == curses.KEY_RIGHT):

        if forward > 0:
            forward -= .1
        elif forward < 0:
            forward += .1

        # if left > 0:
        #     left -= .1
        # elif left < 0:
        #     left += .1

        if abs(forward) < .1:
            forward = 0
        if abs(left) < .1:
            left = 0
        
    msg = drive_param()
    msg.velocity = forward
    msg.angle = -1 * left
    # print("---------")
    # print("velocity: " + str(msg.velocity))
    # print("angle: " + str(msg.angle))
    # print("---------")
    # print()
    pub.publish(msg)
    # rospy.spin()

curses.endwin()
