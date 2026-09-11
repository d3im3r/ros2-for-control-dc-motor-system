"""Launch file for Stage 02: Open-Loop System Identification via Step Response.

Launches:
  - Step response PWM profile generator (dc_motor_experiments/step_response)
  - CSV dataset logger (dc_motor_experiments/data_logger)
  - Real-time angular velocity monitor (dc_motor_experiments/velocity_monitor)
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_bringup = FindPackageShare('dc_motor_bringup')

    step_arg = DeclareLaunchArgument(
        'step',
        default_value='0.0',
        description='Step PWM amplitude percentage (-100.0 to 100.0)'
    )

    total_time_arg = DeclareLaunchArgument(
        'total_time',
        default_value='40.0',
        description='Total experiment acquisition duration in seconds'
    )

    base_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_bringup, 'launch', 'motor_system.launch.py'])
        )
    )

    step_profile_node = Node(
        package='dc_motor_experiments',
        executable='step_response',
        name='step_profile_node',
        output='screen',
        parameters=[{
            'step_percent': LaunchConfiguration('step'),
            'total_time': LaunchConfiguration('total_time'),
            'initial_time': 1.0,
            'step_end_time': 36.0,
        }]
    )

    data_logger_node = Node(
        package='dc_motor_experiments',
        executable='data_logger',
        name='step_response_db',
        output='screen',
        parameters=[{
            'total_time': LaunchConfiguration('total_time'),
        }]
    )

    velocity_monitor_node = Node(
        package='dc_motor_experiments',
        executable='velocity_monitor',
        name='step_response_graph',
        output='screen',
        parameters=[{
            'total_time': LaunchConfiguration('total_time'),
        }]
    )

    return LaunchDescription([
        step_arg,
        total_time_arg,
        base_launch,
        LogInfo(msg="[Stage 02] Launching System Identification Step Response Experiment..."),
        data_logger_node,
        velocity_monitor_node,
        step_profile_node,
    ])
