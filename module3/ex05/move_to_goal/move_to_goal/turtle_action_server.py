import time
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from numpy import sqrt
from math import atan

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtleaction.action import MessageTurtleCommands


class TurtleActionServer(Node):

    class Subscriptor(Node):
        def __init__(self):    
            super().__init__('turtle_action_server_pose_subscriptor')
            self.pose_subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
            self.pose = Pose()
            rclpy.spin_once(self)

        def pose_callback(self, msg):
            self.pose = msg

        def get_turtle_pose(self):
            return self.pose

    def __init__(self):
        super().__init__('turtle_action_server')
        self._action_server = ActionServer(
                self,
                MessageTurtleCommands,
                'turtle_command',
                self.execute_callback)

        self.cmd_publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.pose_subscription = self.Subscriptor()
        self.pose = Pose()


    def rotation_angle(self, turtle_pose, x, y):
        x_turtle, y_turtle = turtle_pose.x, turtle_pose.y
        rotation_angle = turtle_pose.theta # угол, на который черепаха повернута сейчас
        speed_vector = np.array([x - x_turtle, y - y_turtle])

        basis = np.array([1, 0])
        speed_vector_angle = 2. * np.pi - np.arccos(np.dot(speed_vector, basis) / (np.linalg.norm(speed_vector) * np.linalg.norm(basis)))
        if speed_vector[1] >= 0:
            speed_vector_angle = np.arccos(np.dot(speed_vector, basis) / (np.linalg.norm(speed_vector) * np.linalg.norm(basis)))

    # угол, на который черепаха будет повернута в результате
        turtle_angle = speed_vector_angle
    # сделано так, что сначала якобы вектор basis лежит под углом theta_turtle к оси Ox,
    # затем мы поворачиваем его так, чтобы он лежал на положительной полуоси Ox,
    # и находим угол между ним и вектором скорости черепахи
        speed_vector_angle -= rotation_angle
        if speed_vector_angle >= 2 * np.pi:
            speed_vector_angle -= 2 * np.pi
        elif speed_vector_angle < 0:
            speed_vector_angle += 2 * np.pi

        rotation_angle = speed_vector_angle if speed_vector_angle <= np.pi else -(2 * np.pi - speed_vector_angle)
        return rotation_angle, turtle_angle

    def execute_callback(self, goal_handle):
        self.get_logger().info('Started execute callback!')

        # feedback
        feedback_msg = MessageTurtleCommands.Feedback()
        feedback_msg.odom = 0
        goal_handle.publish_feedback(feedback_msg)

        # main
        goal_x = goal_handle.request.x
        goal_y = goal_handle.request.y

        dir = Twist()
        dir.angular.x = 0.
        dir.angular.y = 0.
        dir.angular.z = 0.
        dir.linear.x = 0.
        dir.linear.y = 0.
        dir.linear.z = 0.

        rclpy.spin_once(self.pose_subscription)
        self.start_pose = self.pose_subscription.get_turtle_pose()
        self.pose = self.start_pose
        self.get_logger().info(f'Got pose: {self.start_pose}')

#        f = lambda x, y : atan(x / y) if x * y > 0 else np.pi + atan(x / y) if x < 0 and y > 0 else atan(x / y)
#        deltaX, deltaY = goal_x - self.start_pose.x, goal_y - self.start_pose.y
#        final_angle = -(np.pi - f(abs(deltaX), abs(deltaY))) if deltaX < 0 and deltaY < 0 else f(abs(deltaX), abs(deltaY))
#        angle_diff = final_angle - self.start_pose.theta

        angle_diff, final_angle = self.rotation_angle(self.start_pose, goal_x, goal_y)

        self.get_logger().info(f'final_angle: {final_angle}, angle_diff: {angle_diff}')

        dir.angular.z = angle_diff

        self.cmd_publisher.publish(dir)
        time.sleep(1)
        dir.angular.z = 0.
        self.get_logger().info('finished rotation')

        dir.linear.x = sqrt((self.start_pose.x - goal_x)**2 + (self.start_pose.y - goal_y)**2)
        odometry = 0

        self.cmd_publisher.publish(dir)

        while odometry < dir.linear.x:
            self.get_logger().info(f'odometry: {odometry}\n dir.linear.x: {dir.linear.x}')

            rclpy.spin_once(self.pose_subscription)
            self.pose = self.pose_subscription.get_turtle_pose()
            self.get_logger().info(f'Got pose: {self.pose}')

            odometry = sqrt((self.pose.x - self.start_pose.x)**2 + (self.pose.y - self.start_pose.y)**2)
            angle_diff = abs(final_angle - self.pose.theta)

            feedback_msg.odom = int(odometry)
            goal_handle.publish_feedback(feedback_msg)

        self.get_logger().info('finished loop!')

        # closing
        goal_handle.succeed()

        result = MessageTurtleCommands.Result()
        result.result = True
        self.get_logger().info('Finished execute callback!')
        return result


def main(args=None):
    rclpy.init(args=args)

    turtle_action_server = TurtleActionServer()

    rclpy.spin(turtle_action_server)


if __name__ == '__main__':
    main()
