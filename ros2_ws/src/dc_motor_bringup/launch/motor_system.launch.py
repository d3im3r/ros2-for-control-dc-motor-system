"""Base launch file: Common infrastructure for DC motor system.

Manages shared hardware configuration and communication parameters.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    port_arg = DeclareLaunchArgument(
        'serial_port',
        default_value='/dev/ttyUSB0',
        description='Serial port connected to ESP32 micro-ROS client'
    )
    baudrate_arg = DeclareLaunchArgument(
        'baudrate',
        default_value='115200',
        description='Baudrate for serial micro-ROS connection'
    )

    return LaunchDescription([
        port_arg,
        baudrate_arg,
        LogInfo(
            msg=[
                '[motor_system] Base infrastructure ready. Serial port: ',
                LaunchConfiguration('serial_port'),
                ' @ ',
                LaunchConfiguration('baudrate'),
                ' baud.'
            ]
        ),
    ])
