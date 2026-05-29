#!/usr/bin/env python3

import rclpy

from rclpy.node import Node

from rclpy.executors import MultiThreadedExecutor

from pymoveit2 import MoveIt2

from threading import Thread

class ZA6Mover(Node):

    def __init__(self):

        super().__init__("za6_mover")

        self.moveit2 = MoveIt2(
            node=self,

            joint_names=[
                "joint_1",
                "joint_2",
                "joint_3",
                "joint_4",
                "joint_5",
                "joint_6",
            ],

            base_link_name="base_link",

            end_effector_name="tool0",

            group_name="manipulator",
        )

    def move_home(self):

        joint_positions = [
            0.0,
            -1.57,
            1.57,
            0.0,
            0.0,
            0.0,
        ]

        self.get_logger().info("Moving robot...")

        self.moveit2.move_to_configuration(joint_positions)

        self.moveit2.wait_until_executed()

        self.get_logger().info("Motion complete")


def main():

    rclpy.init()

    node = ZA6Mover()

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    executor_thread = Thread(
        target=executor.spin,
	daemon=True
    )

    executor_thread.start()

    node.move_home()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
