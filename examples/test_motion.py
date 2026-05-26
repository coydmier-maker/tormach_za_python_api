#!/usr/bin/env python3

import rclpy

from robot import RobotAPI


def main():

    rclpy.init()

    robot = RobotAPI()

    print('Current joints:')
    print(robot.get_joint_positions())

    # Move joint 2 slightly
    robot.offset_joint(1, 0.1)

    robot.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()