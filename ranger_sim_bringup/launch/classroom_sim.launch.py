#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command
import os
def generate_launch_description():
    world_path = os.path.join(os.getcwd(), 'src', 'ranger_sim_bringup', 'worlds', 'robotics_room.sdf')
    xacro_path = os.path.join(
        os.getcwd(), 'src', 'ugv_gazebo_sim', 'ranger_mini','ranger_mini_v3_gazebo','xacro', 'ranger_mini_gazebo.xacro'
    )

    parameters = [{'use_sim_time': True}]
    ld = LaunchDescription()
    # Launch Gazebo with your world file.
    
    
    ign_gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', world_path],
        output='screen'
    )
    ld.add_action(ign_gazebo)
    
    
    clock_bridge = Node(
       package='ros_gz_bridge',
       executable='parameter_bridge',
       arguments=['/clock@rosgraph_msgs/msg/Clock@ignition.msgs.Clock'],
       output='screen',
       parameters=parameters
    )
    ld.add_action(clock_bridge)

    
    cmd_vel_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist'],
        output='screen',
        parameters=parameters

    )
    ld.add_action(cmd_vel_bridge)
 

    
    
    # Robot state publisher from URDF
 
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': Command(['python3', '-m', 'xacro', xacro_path]),
            'use_sim_time': True
        }]
    )
    ld.add_action(robot_state_publisher)

    
    spawn_publisher = Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-topic', 'robot_description',
                '-name', 'your_robot',
                '-x', '0', '-y', '0', '-z', '0.1'  # Spawn position
            ],
            output='screen'
        )
    ld.add_action(spawn_publisher)


 
    
    return ld