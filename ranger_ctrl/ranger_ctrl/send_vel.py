import rclpy
from rclpy.node import Node
from ranger_msgs.msg import *
from sensor_msgs.msg import BatteryState
from geometry_msgs.msg import Twist




class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('velocity_publisher')
        
        self.create_subscription (ActuatorStateArray, '/actuator_state',self.actuator_state_callback,10)
        self.create_subscription (BatteryState, '/battery_state',self.battery_state_callback,10)
        self.create_subscription (MotionState, '/motion_state',self.motion_state_callback,10)
        self.create_subscription (SystemState, '/system_state',self.system_state_callback,10)
        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        self.timer = self.create_timer(0.1, self.publish_velocity)
        
    def publish_velocity(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.1
        self.publisher_.publish(msg)

    def actuator_state_callback(self, msg):
       pass
    def battery_state_callback(self, msg):
        pass
    def motion_state_callback(self, msg):
        pass
    def system_state_callback(self, msg):
        pass
        

def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()