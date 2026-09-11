#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class StepProfileNode(Node):

    def __init__(self):
        super().__init__('step_profile_node')

        self.declare_parameter('step_percent', 0.0)
        self.declare_parameter('initial_time', 1.0)
        self.declare_parameter('step_end_time', 36.0)
        self.declare_parameter('total_time', 40.0)

        self.step_percent = float(
            self.get_parameter('step_percent').value
        )
        self.initial_time = float(
            self.get_parameter('initial_time').value
        )
        self.step_end_time = float(
            self.get_parameter('step_end_time').value
        )
        self.total_time = float(
            self.get_parameter('total_time').value
        )

        self.step_percent = max(
            -100.0,
            min(100.0, self.step_percent)
        )

        self.publisher = self.create_publisher(
            Float32,
            '/pwm_input',
            10
        )

        self.msg = Float32()
        self.start_time = self.get_clock().now()
        self.finished = False
        self.previous_state = None

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.get_logger().info(
            f'Prueba automatica: escalon = '
            f'{self.step_percent:.1f} %'
        )

    def timer_callback(self):
        now = self.get_clock().now()
        t = (now - self.start_time).nanoseconds * 1e-9

        if t < self.initial_time:
            pwm = 0.0
            state = 'INITIAL_ZERO'
        elif t < self.step_end_time:
            pwm = self.step_percent
            state = 'STEP'
        elif t < self.total_time:
            pwm = 0.0
            state = 'FINAL_ZERO'
        else:
            self.msg.data = 0.0
            self.publisher.publish(self.msg)
            self.finished = True
            self.timer.cancel()
            self.get_logger().info(
                'Prueba finalizada. PWM = 0 %.'
            )
            return

        self.msg.data = float(pwm)
        self.publisher.publish(self.msg)

        if state != self.previous_state:
            self.previous_state = state
            self.get_logger().info(
                f't = {t:.2f} s | PWM = {pwm:.1f} %'
            )


def main(args=None):
    rclpy.init(args=args)
    node = StepProfileNode()

    try:
        while rclpy.ok() and not node.finished:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            msg = Float32()
            msg.data = 0.0
            node.publisher.publish(msg)
        except Exception:
            pass

        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
