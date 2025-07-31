import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description ():
    return LaunchDescription (
        [
            Node (
                package = 'ranger_sim_bringup',
                executable = 'tf_publisher.py',
                name = 'odom_tf_broadcaster',
                output = 'screen',
                parameters=[{"use_sim_time": True}],
                arguments=['--ros-args', '--log-level', 'debug']
            )
        ]
    )