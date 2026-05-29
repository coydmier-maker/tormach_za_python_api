#!/usr/bin/env python3

import rclpy

from za6_robot import ZA6Robot


def main():

    rclpy.init()

    robot = ZA6Robot()

    #
    # Move robot
    #

    robot.home()
    
    robot.shutdown()

    rclpy.shutdown()


if __name__ == "__main__":
    main()