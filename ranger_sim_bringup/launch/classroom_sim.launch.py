#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition
from nav2_common.launch import ReplaceString



def generate_launch_description():
    # Specify the name of the package
    pkg_name = "ranger_mini"
    namespace = "ranger_mini"

    launch_file_dir = os.path.join(get_package_share_directory("ranger_sim_bringup"), "launch")
    pkg_gazebo_ros = get_package_share_directory("ros_gz_sim")

    # Arguments and parameters
    use_rviz = LaunchConfiguration("use_rviz", default="true")
    rviz_config_file = LaunchConfiguration(
        "rviz_config_file", default="ranger_mini.rviz"
    )
    use_sim_time = LaunchConfiguration("use_sim_time", default="true")
    x_pose = LaunchConfiguration("x_pose", default="0.0")
    y_pose = LaunchConfiguration("y_pose", default="0.0")
    yaw_pose = LaunchConfiguration("yaw_pose", default="0.0")
    world_name = LaunchConfiguration("world_name", default="empty.world")

    declare_world_name_arg = DeclareLaunchArgument(
        "world_name", default_value=world_name, description="Specify Gazebo world name"
    )

    declare_user_rviz_arg = DeclareLaunchArgument(
        "use_rviz", default_value=use_rviz, description="Run rviz if true"
    )

    declare_rviz_config_file_arg = DeclareLaunchArgument(
        "rviz_config_file",
        default_value=rviz_config_file,
        description="Rviz configuration file",
    )

    # Set GAZEBO environment variables
    install_dir = get_package_prefix("ranger_mini")
    gazebo_models_path = os.path.join(pkg_name, "meshes")

    if "GZ_SIM_RESOURCE_PATH" in os.environ:
        os.environ["GZ_SIM_RESOURCE_PATH"] = (
            os.environ["GZ_SIM_RESOURCE_PATH"] + ":" + install_dir + "/share/"
        )
    else:
        os.environ["GZ_SIM_RESOURCE_PATH"] = install_dir + "/share/"

    os.environ["GZ_SIM_SYSTEM_PLUGIN_PATH"] = ":".join(
        [
            os.environ.get("GZ_SIM_SYSTEM_PLUGIN_PATH", default=""),
            os.environ.get("LD_LIBRARY_PATH", default=""),
        ]
    )

    # To support pre-garden. Deprecated.
    os.environ["IGN_GAZEBO_SYSTEM_PLUGIN_PATH"] = ":".join(
        [
            os.environ.get("IGN_GAZEBO_SYSTEM_PLUGIN_PATH", default=""),
            os.environ.get("LD_LIBRARY_PATH", default=""),
        ]
    )

    world = PathJoinSubstitution(
        [get_package_share_directory("ranger_sim_bringup"), "worlds", world_name]
    )

    # gzserver_cmd = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(pkg_gazebo_ros, "launch", "gz_sim.launch.py")
    #     ),
    #     launch_arguments={
    #         "gz_args": ["--verbose 4 -r " ,world],
    #         "on_exit_shutdown": "true",
    #         "gui": "false",
    #     }.items(),
    # ) 
    
    gzserver_cmd = LaunchDescription([
        ExecuteProcess(
            cmd=["ign", "gazebo", "-r","-s", world],
            output="screen"
        )
    ])

    # Add namespace to rviz config file
    namespaced_rviz_config_file = ReplaceString(
        source_file=PathJoinSubstitution(
            [get_package_share_directory("ranger_sim_bringup"), "rviz", rviz_config_file]
        ),
        replacements={"/robot_namespace": ("/", namespace)},
    )

    # Nodes
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        namespace=namespace,
        name="rviz2",
        arguments=["-d", namespaced_rviz_config_file],
        condition=IfCondition(use_rviz),
        remappings=[
            ("/goal_pose", "goal_pose"),
            ("/clicked_point", "clicked_point"),
            ("/initialpose", "initialpose"),
            ("/move_base_simple/goal", "move_base_simple/goal"),
            ("/tf", "tf"),
            ("/tf_static", "tf_static"),
        ],
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, "ranger_mini_robot_state_publisher.launch.py")
        ),
        launch_arguments={"use_sim_time": use_sim_time, "namespace": namespace}.items(),
    )

    
    four_ws_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_prefix("four_ws_control"),"lib","four_ws_control","four_ws_control.launch.py")],
        )
    )
    
    robot_spawn_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, "ranger_mini_spawn.launch.py")
        ),
        launch_arguments={
            "namespace": namespace,
            "x_pose": x_pose,
            "y_pose": y_pose,
            "yaw_pose": yaw_pose,
        }.items(),
    )
    
    publish_tf = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, "tf_publisher.launch.py")
        )
    )

    # Ros Bridge Gazebo
    namespaced_bridge_file = os.path.join(
        get_package_share_directory("ranger_sim_bringup"),
        "config",
        "ranger_mini_bridge_ros_gz.yaml",
    )

    ros_gz_bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["--ros-args", "-p", f"config_file:={namespaced_bridge_file}"],
    )

    ros_gz_bridge_image_node = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=["/ranger_mini/rgb_cam/image_raw"],
    )
    
    spawn_position_controller = ExecuteProcess( 
        cmd=[
        'ros2', 'run', 'controller_manager', 'spawner', 'forward_position_controller',
        '--controller-manager', '/controller_manager'
    ],
    output='screen' )

    
    spawn_velocity_controller = ExecuteProcess(
    cmd=[
        'ros2', 'run', 'controller_manager', 'spawner', 'forward_velocity_controller',
        '--controller-manager', '/controller_manager'
    ],
    output='screen'
)

    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_world_name_arg)
    ld.add_action(declare_user_rviz_arg)
    ld.add_action(declare_rviz_config_file_arg)

    # Add the commands to the launch description
    ld.add_action(gzserver_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(robot_spawn_cmd)
    ld.add_action(ros_gz_bridge_node)
    ld.add_action(ros_gz_bridge_image_node)
    
    ld.add_action(spawn_position_controller)
    ld.add_action(spawn_velocity_controller)
    ld.add_action(publish_tf)
    ld.add_action (four_ws_launch)

    ld.add_action(rviz_node)
    

    return ld
