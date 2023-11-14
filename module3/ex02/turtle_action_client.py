import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from turtleaction.action import MessageTurtleCommands

class TurtleActionClient(Node):

    def __init__(self):
        super().__init__('turtle_action_client')
        self._action_client = ActionClient(self, MessageTurtleCommands, 'turtle_command')
        self.state = 0

    def send_goal(self, command, dist, angle):
        goal_msg = MessageTurtleCommands.Goal()
        goal_msg.command = command
        goal_msg.s = dist
        goal_msg.angle = angle

        self._action_client.wait_for_server(timeout_sec=1.0)

        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        self.get_logger().info('Goal sent!')
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):

        result = future.result().result
        self.get_logger().info(f'Feedback: {result.result}')
        if result.result:
            self.state += 1
            if self.state < 3:
                self.get_logger().info('Turtel get to da place!')
                if self.state == 1:
                    self.send_goal('turn_left', 2, 90)
                else:
                    self.send_goal('forward', 2, 90)
            else:
                self.get_logger().info('Turtel get to da final place!')
                rclpy.shutdown()

        else:
            self.get_logger().info('Turtle no get to da place :(')
            rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback: {feedback.odom}')

def main(args=None):
    rclpy.init(args=args)
    action_client = TurtleActionClient()
    action_client.send_goal('forward', 2, 90)
    rclpy.spin(action_client)

    #action_client.send_goal(str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
   
if __name__ == '__main__':
    main()
