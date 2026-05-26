#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.action import FollowJointTrajectory

from builtin_interfaces.msg import Duration


class RobotAPI(Node):

    def __init__(self):

        super().__init__('robot_api')

        self.current_joint_state = None

        self.joint_names = [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6'
        ]

        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.trajectory_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/joint_trajectory_controller/follow_joint_trajectory'
        )

    def joint_state_callback(self, msg):

        self.current_joint_state = msg

    def wait_for_joint_state(self):

        while rclpy.ok() and self.current_joint_state is None:
            rclpy.spin_once(self)

    def get_joint_positions(self):

        self.wait_for_joint_state()

        return list(self.current_joint_state.position)

    def move_joints(self, positions, duration=3.0):

        self.get_logger().info('Waiting for trajectory server...')

        self.trajectory_client.wait_for_server()

        goal_msg = FollowJointTrajectory.Goal()

        trajectory = JointTrajectory()

        trajectory.joint_names = self.joint_names

        point = JointTrajectoryPoint()

        point.positions = positions

        point.time_from_start = Duration(
            sec=int(duration),
            nanosec=int((duration % 1) * 1e9)
        )

        trajectory.points.append(point)

        goal_msg.trajectory = trajectory

        self.get_logger().info('Sending trajectory...')

        future = self.trajectory_client.send_goal_async(goal_msg)

        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        result_future = goal_handle.get_result_async()

        rclpy.spin_until_future_complete(self, result_future)

        self.get_logger().info('Trajectory complete')

    def offset_joint(self, joint_index, delta):

        current = self.get_joint_positions()

        current[joint_index] += delta

        self.move_joints(current)