# apt install sshpass
sshpass -p "ubuntu" scp ~/github/f1tenth-course-labs/race/src/dist_finder.py ~/github/f1tenth-course-labs/race/src/debug_lidar.py ~/github/f1tenth-course-labs/race/src/control.py ~/github/f1tenth-course-labs/race/src/kill.py ubuntu@192.168.1.1:~/catkin_ws/src/f1tenth-course-labs/race/src/
sshpass -p "ubuntu" scp ~/github/f1tenth-course-labs/race/launch/wall_follow.launch ubuntu@192.168.1.1:~/catkin_ws/src/f1tenth-course-labs/race/launch/
sshpass -p "ubuntu" scp ~/github/f1tenth-course-labs/race/make.sh ubuntu@192.168.1.1:~/catkin_ws/

