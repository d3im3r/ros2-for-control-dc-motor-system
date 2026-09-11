#!/usr/bin/env python3

import matplotlib.pyplot as plt

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class StepResponseGraph(Node):

    def __init__(self):
        super().__init__('step_response_graph')

        self.subscription = self.create_subscription(
            Float32,
            '/vel_rad_s',
            self.velocity_callback,
            10
        )

        self.declare_parameter('total_time', 40.0)
        self.total_time = float(
            self.get_parameter('total_time').value
        )
        self.max_samples = int(self.total_time / 0.1)
        self.counter = 0
        self.finished = False

        self.time_data = []
        self.velocity_data = []

        self.start_time = self.get_clock().now()

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], label='Velocidad angular')

        self.ax.set_xlim(0.0, self.total_time)
        self.ax.set_xlabel('Tiempo [s]')
        self.ax.set_ylabel('Velocidad angular [rad/s]')
        self.ax.set_title('Respuesta escalon del motor DC')
        self.ax.grid(True)
        self.ax.legend()

        self.vel_text = self.ax.text(
            0.72,
            0.90,
            'omega = 0.00 rad/s\nt = 0.00 s',
            transform=self.ax.transAxes,
            fontsize=11,
            fontweight='bold',
            verticalalignment='top',
            bbox=dict(
                boxstyle='round',
                facecolor='white',
                alpha=0.85
            )
        )

    def velocity_callback(self, msg):
        if self.finished:
            return

        now = self.get_clock().now()
        t = (now - self.start_time).nanoseconds * 1e-9
        velocity = float(msg.data)

        self.time_data.append(t)
        self.velocity_data.append(velocity)
        self.counter += 1

        self.line.set_data(self.time_data, self.velocity_data)

        if self.velocity_data:
            v_min = min(self.velocity_data)
            v_max = max(self.velocity_data)

            margin = max(
                1.0,
                0.1 * max(abs(v_min), abs(v_max), 1.0)
            )

            self.ax.set_ylim(v_min - margin, v_max + margin)

        self.vel_text.set_text(
            f'omega = {velocity:.2f} rad/s\n'
            f't = {t:.2f} s'
        )

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

        if self.counter >= self.max_samples:
            self.finished = True
            self.get_logger().info(
                f'Captura finalizada: '
                f'{self.max_samples} muestras adquiridas.'
            )


def main(args=None):
    rclpy.init(args=args)
    node = StepResponseGraph()

    plt.ion()
    plt.show()

    try:
        while rclpy.ok() and not node.finished:
            rclpy.spin_once(node, timeout_sec=0.05)
            plt.pause(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()

        plt.ioff()
        print(
            'Proceso ROS 2 finalizado. '
            'La grafica permanecera abierta hasta que la cierre.'
        )
        plt.show()


if __name__ == '__main__':
    main()
