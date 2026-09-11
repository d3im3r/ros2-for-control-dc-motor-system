#!/usr/bin/env python3
"""PID Controller Node for DC Motor Speed Regulation."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class PIDControllerNode(Node):

    def __init__(self):
        super().__init__('pid_controller_node')

        self.declare_parameter('kp', 1.0)
        self.declare_parameter('ki', 0.1)
        self.declare_parameter('kd', 0.01)
        self.declare_parameter('setpoint', 0.0)

        self.kp = float(self.get_parameter('kp').value)
        self.ki = float(self.get_parameter('ki').value)
        self.kd = float(self.get_parameter('kd').value)
        self.setpoint = float(self.get_parameter('setpoint').value)

        self.integral_error = 0.0
        self.prev_error = 0.0
        self.current_vel = 0.0

        self.sub_vel = self.create_subscription(
            Float32,
            '/vel_rad_s',
            self.vel_callback,
            10
        )

        self.pub_pwm = self.create_publisher(
            Float32,
            '/pwm_input',
            10
        )

        self.timer = self.create_timer(0.01, self.control_loop)
        self.get_logger().info('PID Controller Node initialized.')

    def vel_callback(self, msg):
        self.current_vel = float(msg.data)

    def control_loop(self):
        dt = 0.01
        error = self.setpoint - self.current_vel
        self.integral_error += error * dt
        derivative_error = (error - self.prev_error) / dt
        self.prev_error = error

        u = (self.kp * error) + (self.ki * self.integral_error) + (self.kd * derivative_error)
        u_sat = max(-100.0, min(100.0, u))

        msg = Float32()
        msg.data = float(u_sat)
        self.pub_pwm.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PIDControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
