# MIT license LOL

from geometry_msgs.msg import Twist
from rclpy.node import Node

import rclpy


class Movmnt(Node):
    def __init__(self):
        super().__init__('movmnt')

        timer_period = 0.05
        self.timer = self.create_timer(timer_period, self.timer_movement_callback)

        self.move_pub = self.create_publisher(Twist, '/diff_drive/cmd_vel', 1)

        self.movement_msg = Twist()
        self.movement_msg.linear.x = 5.0
        self.movement_msg.linear.y = 0.0
        self.movement_msg.linear.z = 0.0

        self.movement_msg.angular.x = 0.0
        self.movement_msg.angular.y = 0.0
        self.movement_msg.angular.z = -0.1

    def timer_movement_callback(self):
        self.move_pub.publish(self.movement_msg)


def main(args=None):
    rclpy.init(args=args)

    mvmt = Movmnt()
    rclpy.spin(mvmt)

    mvmt.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
