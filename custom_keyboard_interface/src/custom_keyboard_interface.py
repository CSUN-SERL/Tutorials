#!/usr/bin/env python
import roslib
import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty, configparser, os

os.chdir(os.getcwd() + '/Documents/husky_kinetic/src/custom_keyboard_interface/custom_keyboard_interface/src/')

config = configparser.ConfigParser()
config.read('config.ini')

forward = config['CONTROLS']['FORWARD']
left = config['CONTROLS']['LEFT']
right = config['CONTROLS']['RIGHT']
back = config['CONTROLS']['BACK']
drift_left = config['CONTROLS']['DRIFT_LEFT']
drift_right = config['CONTROLS']['DRIFT_RIGHT']

increase_max_speed = config['SPEEDBINDINGS']['INCREASE_MAX_SPEED']
decrease_max_speed = config['SPEEDBINDINGS']['DECREASE_MAX_SPEED']
increase_linear_speed = config['SPEEDBINDINGS']['INCREASE_LINEAR_SPEED']
decrease_linear_speed = config['SPEEDBINDINGS']['DECREASE_LINEAR_SPEED']
increase_angular_speed = config['SPEEDBINDINGS']['INCREASE_ANGULAR_SPEED']
decrease_angular_speed = config['SPEEDBINDINGS']['DECREASE_ANGULAR_SPEED']

msg = """
Reading from the keyboard  and Publishing to Twist! 
---------------------------
Moving around:
   {0}  {1}  {2}
   {3}  {4}  {5}

anything else : stop

{6}/{7} : increase/decrease max speeds by 10%
{8}/{9} : increase/decrease only linear speed by 10%
{10}/{11} : increase/decrease only angular speed by 10%

CTRL-C to quit
""".format(drift_left, forward, drift_right, left, back, right, increase_max_speed, decrease_max_speed, increase_linear_speed, decrease_linear_speed, increase_angular_speed, decrease_angular_speed)

moveBindings = {
		forward:(1,0,0,0),
		drift_right:(1,0,0,-1),
		left:(0,0,0,1),
		right:(0,0,0,-1),
		drift_left:(1,0,0,1),
		back:(-1,0,0,0),
		'.':(-1,0,0,1),
		'm':(-1,0,0,-1),
		'O':(1,-1,0,0),
		'I':(1,0,0,0),
		'J':(0,1,0,0),
		'L':(0,-1,0,0),
		'U':(1,1,0,0),
		'<':(-1,0,0,0),
		'>':(-1,-1,0,0),
		'M':(-1,1,0,0),
		't':(0,0,1,0),
		'b':(0,0,-1,0),
	       }

speedBindings={
		increase_max_speed:(1.1,1.1),
		decrease_max_speed:(.9,.9),
		increase_linear_speed:(1.1,1),
		decrease_linear_speed:(.9,1),
		increase_angular_speed:(1,1.1),
		decrease_angular_speed:(1,.9),
	      }

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

speed = .5
turn = 1

def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	
	pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
	rospy.init_node('teleop_twist_keyboard')

	x = 0
	y = 0
	z = 0
	th = 0
	status = 0

	try:
		print msg
		print vels(speed,turn)
		while(1):
			key = getKey()
			if key in moveBindings.keys():
				x = moveBindings[key][0]
				y = moveBindings[key][1]
				z = moveBindings[key][2]
				th = moveBindings[key][3]
			elif key in speedBindings.keys():
				speed = speed * speedBindings[key][0]
				turn = turn * speedBindings[key][1]

				print vels(speed,turn)
				if (status == 14):
					print msg
				status = (status + 1) % 15
			else:
				x = 0
				y = 0
				z = 0
				th = 0
				if (key == '\x03'):
					break

			twist = Twist()
			twist.linear.x = x*speed; twist.linear.y = y*speed; twist.linear.z = z*speed;
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th*turn
			pub.publish(twist)

	except:
		print e

	finally:
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

    		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


