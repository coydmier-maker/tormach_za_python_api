#!/usr/bin/env python3

import rclpy

from threading import Thread

from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from pymoveit2 import MoveIt2

from geometry_msgs.msg import Pose

from tf_transformations import quaternion_from_euler

from scene_manager import SceneManager


class ZA6Robot(Node):

    def __init__(self):

        super().__init__("za6_robot")

        #
        # Robot configuration
        #

        self.joint_names = [
            "joint_1",
            "joint_2",
            "joint_3",
            "joint_4",
            "joint_5",
            "joint_6",
        ]

        self.base_link_name = "base_link"

        self.end_effector_name = "tool0"

        self.group_name = "manipulator"

        #
        # MoveIt interface
        #

        self.moveit2 = MoveIt2(
            node=self,

            joint_names=self.joint_names,

            base_link_name=self.base_link_name,

            end_effector_name=self.end_effector_name,

            group_name=self.group_name,
        )

        #
        # Executor
        #

        self._executor = MultiThreadedExecutor()

        self._executor.add_node(self)

        self._executor_thread = Thread(
            target=self._executor.spin,
            daemon=True,
        )

        self._executor_thread.start()

        #
        # Scene Manager
        #

        self.scene = SceneManager(
        node=self,
        base_frame=self.base_link_name,

)

    #
    # Joint-space motion
    #

    def move_joints(self, joint_positions):

        self.get_logger().info(
            f"Moving to joints: {joint_positions}"
        )

        self.moveit2.move_to_configuration(joint_positions)

        self.moveit2.wait_until_executed()

    #
    # Pose-space motion
    #

    def move_pose(self, position, quat_xyzw):

        self.get_logger().info(
            f"Moving to pose: {position}"
        )

        self.moveit2.move_to_pose(
            position=position,
            quat_xyzw=quat_xyzw,
        )

        self.moveit2.wait_until_executed()

    def move_pose_xyz_rpy(
        self,

        x,
        y,
        z,

        roll,
        pitch,
        yaw,
    ):

        quat = quaternion_from_euler(
            roll,
            pitch,
            yaw,
        )

        self.move_pose(
            position=[x, y, z],

            quat_xyzw=[
                quat[0],
                quat[1],
                quat[2],
                quat[3],
            ]
        )

    #
    # Convenience motions
    #

    def home(self):

        self.move_joints([
            0.0,
            -1.57,
            1.57,
            0.0,
            0.0,
            0.0,
        ])

    #
    # Cleanup
    #

    def shutdown(self):

        self.executor.shutdown()

        self.destroy_node()