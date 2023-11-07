import sys


from name.srv import FullNameSumService

import rclpy
from rclpy.node import Node

class clientAsync(Node):

    def __init__(self):
        super().__init__('clientAdderAsync')
        self.cli = self.create_client(FullNameSumService, 'full_name_service')

        while not self.cli.wait_for_service(timeout_sec = 1.0):
            self.get_logger().info('Timeout on waiting for service response. Waiting...')
        
        self.req = FullNameSumService.Request()

    def sendRequest(self, fn, n, ln):
        self.req.last_name = fn
        self.req.name = n
        self.req.first_name = ln
        self.future = self.cli.call_async(self.req)

        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main():
    rclpy.init()

    clientAdderAsync = clientAsync()
    response = clientAdderAsync.sendRequest(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))

    clientAdderAsync.get_logger().info(f'full name is {response.full_name}')

    clientAdderAsync.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
