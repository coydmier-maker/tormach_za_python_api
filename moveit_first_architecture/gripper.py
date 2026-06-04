import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_srvs.srv import SetBool


class Gripper(Node):
    def __init__(self):
        super().__init__('gripper')

        # Publisher to IO channel
        self.pub = self.create_publisher(Bool, '/dout01', 10)

        # Enable IO service
        self.enable_client = self.create_client(SetBool, '/enable_io')

        self.io_enabled = False

    def enable_io(self):
        if self.io_enabled:
            return True

        if not self.enable_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().error("enable_io service not available")
            return False

        req = SetBool.Request()
        req.data = True

        future = self.enable_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        if future.result() and future.result().success:
            self.io_enabled = True
            self.get_logger().info("IO enabled")
            return True
        else:
            self.get_logger().error("Failed to enable IO")
            return False

    def set(self, open: bool):
        if not self.io_enabled:
            self.enable_io()

        msg = Bool()
        msg.data = open
        self.pub.publish(msg)

    def open(self):
        self.set(True)

    def close(self):
        self.set(False)


def main():
    rclpy.init()
    node = Gripper()

    node.enable_io()

    node.get_logger().info("Testing gripper...")
    node.close()
    rclpy.spin_once(node, timeout_sec=1.0)

    node.open()
    rclpy.spin_once(node, timeout_sec=1.0)

    rclpy.shutdown()


if __name__ == '__main__':
    main()