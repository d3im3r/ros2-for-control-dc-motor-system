"""Launch file for Stage 01: Motor Instrumentation and Plant Validation.

Topics involved:
  - /pwm_input: std_msgs/msg/Float32 (Command input to motor driver)
  - /vel_rad_s: std_msgs/msg/Float32 (Angular velocity in rad/s)
  - /vel_rpm:   std_msgs/msg/Float32 (Angular velocity in RPM)

Hardware node (ESP32 micro-ROS) interacts physically with the DC motor.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_bringup = FindPackageShare('dc_motor_bringup')

    base_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_bringup, 'launch', 'motor_system.launch.py'])
        )
    )

    return LaunchDescription([
        base_launch,
        LogInfo(
            msg="[Stage 01] Launching Motor Instrumentation & Validation Environment..."
        ),
        LogInfo(
            msg="[Stage 01] Active topics: /pwm_input (Float32), /vel_rad_s (Float32), /vel_rpm (Float32)"
        ),
        LogInfo(
            msg="[Stage 01] Ready for plant excitation and encoder response validation."
        ),
    ])
