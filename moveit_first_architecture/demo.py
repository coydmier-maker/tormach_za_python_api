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

    #
    # Add collision objects
    #

    robot.scene.load_yaml("scene.yaml")

    #
    # Example pose move
    #

    robot.move_pose(
        position=[0.7, -0.5, 0.5],

        quat_xyzw=[0.545, 0, 0.839, 0],
    )

    #
    # Shutdown
    #

    robot.shutdown()

    rclpy.shutdown()


if __name__ == "__main__":
    main()