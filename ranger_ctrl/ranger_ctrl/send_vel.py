#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ranger_msgs.msg import *
from sensor_msgs.msg import BatteryState
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time
import numpy as np
import transforms3d



class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('velocity_publisher')
        self.start_time = time.time()
        self.create_subscription (ActuatorStateArray, '/actuator_state',self.actuator_state_callback,10)
        self.create_subscription (BatteryState, '/battery_state',self.battery_state_callback,10)
        self.create_subscription (MotionState, '/motion_state',self.motion_state_callback,10)
        self.create_subscription (SystemState, '/system_state',self.system_state_callback,10)
        self.create_subscription (Odometry, '/odom', self.odom_callback,10)
        
        self.odom_received = False
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        self.kp_linear = 0.5
        self.kp_angular = 1
        
        self.ki_linear = 0.0
        self.ki_angular = 0.0
        
        self.kd_linear = 0.0
        self.kd_angular = 0.0
        
        
        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        # # self.publish_velocity_timer(1.0)
        # self.publish_velocity()
        # self.timer = self.create_timer(.02, self.publish_velocity)
        
        # self.navigate_to_goal(0,0,0) 
        while not self.odom_received:
            print ("waiting for odom")
            rclpy.spin_once(self, timeout_sec=0.02)
        self.navigate_to_goal(0,0,np.pi/2)
    
    def publish_velocity_timer (self,dur):
        start_time = time.time()
        while time.time() - start_time < dur:
            self.publish_velocity()
        
        
    def publish_velocity(self,x,y,z):
        # if time.time() - self.start_time > 10.0:
        #     return        
        if np.abs(x) > .3: x = np.sign(x) *.3
        if np.abs(y) > .3: y = np.sign(y)*.3
        if np.abs(z) > .5: z = np.sign(z)*.5

        msg = Twist()
        msg.linear.x = x
        msg.linear.y = y
        msg.angular.z = z
        self.publisher_.publish(msg)

    def actuator_state_callback(self, msg):
       pass
    def battery_state_callback(self, msg):
        pass
    def motion_state_callback(self, msg):
        pass
    def system_state_callback(self, msg):
        pass
    def odom_callback (self,msg):
        
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        
        quat_x = msg.pose.pose.orientation.x
        quat_y = msg.pose.pose.orientation.y
        quat_z = msg.pose.pose.orientation.z
        quat_w = msg.pose.pose.orientation.w
        
        # Convert quaternion to Euler angles
        euler = transforms3d.euler.quat2euler([quat_w, quat_x, quat_y, quat_z])
        self.theta = euler[2]
        self.odom_received = True
        # print ("theta is", np.rad2deg(self.theta))
        
    
    def navigate_to_goal (self, x,y,theta):
        
        prev_err_x, prev_err_y, prev_err_theta, error_sum_x, error_sum_y, error_sum_theta = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        while (abs(self.x - x) > 0.01 or abs(self.y - y) > 0.01 or abs(np.rad2deg(self.theta - theta)) > 1):
            # Calculate velocity commands using PID controller
            velocity_x, velocity_y, velocity_theta, prev_err_x, prev_err_y, prev_err_theta, error_sum_x, error_sum_y, error_sum_theta =     \
            self.PID_controller(x, y, theta, prev_err_x, prev_err_y, prev_err_theta, error_sum_x, error_sum_y, error_sum_theta, 0.02)
            
           
            self.publish_velocity(velocity_x, velocity_y, velocity_theta)
            rclpy.spin_once(self, timeout_sec=0.02) 
        print ("goal reached")
                
    def PID_controller (self, goal_x, goal_y, goal_theta, prev_err_x, prev_err_y, prev_err_theta, error_sum_x, error_sum_y, error_sum_theta, dt):
        # Calculate errors
        error_x = goal_x - self.x
        error_y = goal_y - self.y
        error_theta = goal_theta - self.theta
        # Proportional term
        P_x = self.kp_linear * error_x
        P_y = self.kp_linear * error_y
        P_theta = self.kp_angular * error_theta
        # Integral term
        error_sum_x += error_x * dt
        error_sum_y += error_y * dt
        error_sum_theta += error_theta * dt
        I_x = self.ki_linear * error_sum_x
        I_y = self.ki_linear * error_sum_y
        I_theta = self.ki_angular * error_sum_theta
        # Derivative term
        D_x = self.kd_linear * (error_x - prev_err_x) / dt
        D_y = self.kd_linear * (error_y - prev_err_y) / dt
        D_theta = self.kd_angular * (error_theta - prev_err_theta) / dt
        # sum control output
        control_x = P_x + I_x + D_x
        control_y = P_y + I_y + D_y
        control_theta = P_theta + I_theta + D_theta
        
        # Update previous errors
        prev_err_x = error_x
        prev_err_y = error_y
        prev_err_theta = error_theta
        
        return control_x, control_y, control_theta, prev_err_x, prev_err_y, prev_err_theta, error_sum_x, error_sum_y, error_sum_theta

def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()