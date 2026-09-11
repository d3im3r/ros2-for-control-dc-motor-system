#!/usr/bin/env python3

import csv
from datetime import datetime

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class StepResponseLogger(Node):

    def __init__(self):
        super().__init__('step_response_db')

        self.declare_parameter('total_time', 40.0)
        self.total_time = float(
            self.get_parameter('total_time').value
        )
        self.max_samples = int(self.total_time / 0.1)
        self.sample_count = 0
        self.finished = False

        self.vel_rad_s = 0.0
        self.pwm_percent = 0.0

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.filename = f'motor_step_response_{timestamp}.csv'

        self.csv_file = open(self.filename, mode='w', newline='')
        self.writer = csv.writer(self.csv_file)

        self.writer.writerow([
            'Time (s)',
            'Angular Velocity (rad/s)',
            'PWM (%)'
        ])

        self.start_time = self.get_clock().now()

        self.create_subscription(
            Float32,
            '/vel_rad_s',
            self.velocity_callback,
            10
        )

        self.create_subscription(
            Float32,
            '/pwm_input',
            self.pwm_callback,
            10
        )

        self.timer = self.create_timer(0.1, self.log_data)

        self.get_logger().info(
            f'Registrando {self.max_samples} muestras en: {self.filename}'
        )

    def velocity_callback(self, msg):
        self.vel_rad_s = float(msg.data)

    def pwm_callback(self, msg):
        self.pwm_percent = float(msg.data)

    def log_data(self):
        if self.finished:
            return

        now = self.get_clock().now()
        t = (now - self.start_time).nanoseconds * 1e-9

        self.writer.writerow([
            f'{t:.3f}',
            f'{self.vel_rad_s:.6f}',
            f'{self.pwm_percent:.3f}'
        ])
        self.csv_file.flush()

        self.sample_count += 1

        if self.sample_count >= self.max_samples:
            self.finished = True
            self.timer.cancel()

            self.get_logger().info(
                f'Se capturaron {self.max_samples} muestras.'
            )
            self.get_logger().info(
                f'Base de datos guardada en: {self.filename}'
            )

    def close_file(self):
        if not self.csv_file.closed:
            self.csv_file.close()


def main(args=None):
    rclpy.init(args=args)
    node = StepResponseLogger()

    try:
        while rclpy.ok() and not node.finished:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        node.close_file()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
