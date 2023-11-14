import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from numpy import sqrt

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

    def execute_callback(self, goal_handle):
        self.get_logger().info('Started execute callback!')

        # feedback
        feedback_msg = MessageTurtleCommands.Feedback()
        feedback_msg.odom = 0
        goal_handle.publish_feedback(feedback_msg)

        # main
        command = goal_handle.request.command
        dist = goal_handle.request.s
        angle = goal_handle.request.angle * 0.0174533

        dir = Twist()
        dir.angular.x = 0.
        dir.angular.y = 0.
        dir.angular.z = 0.
        dir.linear.x = 0.
        dir.linear.y = 0.
        dir.linear.z = 0.

        if command == 'forward':
            dir.linear.x = float(dist)
        elif command == 'turn_left':
            dir.angular.z = -float(angle)
        elif command == 'turn_right':
            dir.angular.z = float(angle)
        else:
            self.get_logger().info('invalid command!')
            res = MessageTurtleCommands.Result()
            res.result = False
            return res

        rclpy.spin_once(self.pose_subscription)
        self.start_pose = self.pose_subscription.get_turtle_pose()
        self.pose = self.start_pose
        self.get_logger().info(f'Got pose: {self.start_pose}')
        final_angle = self.start_pose.theta + dir.angular.z
        angle_diff = abs(final_angle - self.start_pose.theta)

        self.cmd_publisher.publish(dir)
#        time.sleep(1)
        odometry = 0

        while (odometry < dir.linear.x and command == 'forward') or (angle_diff > 0.1 and command != 'forward'):
            self.get_logger().info(f'odometry: {odometry}\n dir.linear.x: {dir.linear.x}\nangle_diff: {angle_diff}')
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

    def pose_callback(self, msg):
        self.pose = msg


def main(args=None):
    rclpy.init(args=args)

    turtle_action_server = TurtleActionServer()

    rclpy.spin(turtle_action_server)


if __name__ == '__main__':
    main()
