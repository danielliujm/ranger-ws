#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, PoseArray
from tf2_msgs.msg import TFMessage  
from rclpy.qos import QoSProfile, QoSDurabilityPolicy

import tf2_ros

class FakeOdomTFBroadcaster(Node):
    def __init__(self):
        super().__init__('odom_tf_broadcaster')
        # self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        
        # self.declare_parameter('use_sim_time', True)

        # Subscribe to the odometry topic
        self.subscription = self.create_subscription(
            PoseArray,
            '/ranger_mini/ground_truth_pose',  # Match this with your odometry topic
            self.handle_odom,
            10
        )
        
        # self.create_subscription( TFMessage, "ranger_mini/tf", self.republish_tf,10)
    
        # self.create_subscription (TFMessage, "ranger_mini/tf_static", self.republish_tf_static,10)
        
        tf_static_qos = QoSProfile(
            depth=10,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )

        
        self._tf_republihser = self.create_publisher (TFMessage, "/ranger_mini/tf", 10)
        self._tf_static_republihser = self.create_publisher (TFMessage, "tf_static", qos_profile = tf_static_qos)
        
        
        self.tf_publisher = self.create_publisher(TFMessage, '/ranger_mini/gt_tf', 10)
        
        
        # self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        # self.timer = self.create_timer(0.05, self.broadcast)
        
        self.get_logger().info("####################################################################################### STARTING TF BROADCASTER ##########################################################################################")



    def handle_odom(self, msg):
        # self.get_logger().info('Received odometry message')
        ranger_pose = msg.poses[0]
        
        
        
        
        
        t = TransformStamped()

        t.header.stamp = msg.header.stamp
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'

        t.transform.translation.x = ranger_pose.position.x
        t.transform.translation.y = ranger_pose.position.y
        t.transform.translation.z = ranger_pose.position.z
        
        # t.transform.translation = ranger_pose

        t.transform.rotation = ranger_pose.orientation
        
        tm = TFMessage()
        tm.transforms.append(t)

        self._tf_republihser.publish(tm)


def main(args=None):
    rclpy.init(args=args)
    node = FakeOdomTFBroadcaster()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    
    
    # def broadcast(self):
    #     t = TransformStamped()
    #     t.header.stamp = self.get_clock().now().to_msg()
    #     t.header.frame_id = "odom"
    #     t.child_frame_id = "base_link"
    #     t.transform.translation.x = 0.0
    #     t.transform.translation.y = 0.0
    #     t.transform.translation.z = 0.0
        
    #     t.transform.rotation.x = 0.0
    #     t.transform.rotation.y = 0.0
    #     t.transform.rotation.z = 0.0
    #     t.transform.rotation.w = 1.0
        
    #     self.tf_broadcaster.sendTransform(t)
    #     self.get_logger().info ("publishing")
    
    # def republish_tf(self, msg):
    #     # msg.header.stamp = self.get_clock().now().to_msg()
    #     t = TransformStamped()
    #     t.header.stamp = self.get_clock().now().to_msg()
    #     t.header.frame_id = "odom"
    #     t.child_frame_id = "base_link"
    #     t.transform.translation.x = 0.0
    #     t.transform.translation.y = 0.0
    #     t.transform.translation.z = 0.0
        
    #     t.transform.rotation.x = 0.0
    #     t.transform.rotation.y = 0.0
    #     t.transform.rotation.z = 0.0
    #     t.transform.rotation.w = 1.0
        
    #     msg.transforms.append(t)
    #     self._tf_republihser.publish(msg)
    
    # def republish_tf_static(self):
    #     # msg.header.stamp = self.get_clock().now().to_msg()
    #     t = TransformStamped()
    #     t.header.stamp = self.get_clock().now().to_msg()
    #     t.header.frame_id = "odom"
    #     t.child_frame_id = "base_link"
    #     t.transform.translation.x = 0.0
    #     t.transform.translation.y = 0.0
    #     t.transform.translation.z = 0.32
        
    #     t.transform.rotation.x = 0.0
    #     t.transform.rotation.y = 0.0
    #     t.transform.rotation.z = 0.0
    #     t.transform.rotation.w = 1.0
        
    #     msg = TFMessage()
    #     msg.transforms.append(t)
    #     self._tf_static_republihser.publish(msg)
        