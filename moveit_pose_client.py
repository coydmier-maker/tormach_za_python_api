import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from moveit_msgs.action import MoveGroup
from geometry_msgs.msg import PoseStamped


class MoveItPoseClient(Node):

    def __init__(self):

        super().__init__('moveit_pose_client')

        self.client = ActionClient(self, MoveGroup, '/move_action')

        self.get_logger().info("Waiting for /move_action server...")
        self.client.wait_for_server()

    def send_pose_goal(self, pose: PoseStamped, group_name="arm"):

        goal = MoveGroup.Goal()

        # --- core MoveIt fields ---
        goal.request.group_name = group_name

        goal.request.num_planning_attempts = 10
        goal.request.allowed_planning_time = 5.0

        goal.request.max_velocity_scaling_factor = 0.1
        goal.request.max_acceleration_scaling_factor = 0.1

        # --- goal constraint ---
        goal.request.goal_constraints = []

        from moveit_msgs.msg import Constraints, PositionConstraint, OrientationConstraint
        from shape_msgs.msg import SolidPrimitive

        constraints = Constraints()

        # Position constraint
        pos_constraint = PositionConstraint()
        pos_constraint.header = pose.header
        pos_constraint.link_name = "tool0"   # IMPORTANT: may need adjustment

        box = SolidPrimitive()
        box.type = SolidPrimitive.BOX
        box.dimensions = [0.01, 0.01, 0.01]

        pos_constraint.constraint_region.primitives.append(box)
        pos_constraint.constraint_region.primitive_poses.append(pose.pose)
        pos_constraint.weight = 1.0

        constraints.position_constraints.append(pos_constraint)

        # Orientation constraint
        ori_constraint = OrientationConstraint()
        ori_constraint.header = pose.header
        ori_constraint.link_name = "tool0"
        ori_constraint.orientation = pose.pose.orientation
        ori_constraint.absolute_x_axis_tolerance = 0.1
        ori_constraint.absolute_y_axis_tolerance = 0.1
        ori_constraint.absolute_z_axis_tolerance = 0.1
        ori_constraint.weight = 1.0

        constraints.orientation_constraints.append(ori_constraint)

        goal.request.goal_constraints.append(constraints)

        self.get_logger().info("Sending pose goal to MoveIt...")

        future = self.client.send_goal_async(goal)

        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error("Goal rejected")
            return

        self.get_logger().info("Goal accepted, executing...")

        result_future = goal_handle.get_result_async()

        rclpy.spin_until_future_complete(self, result_future)

        self.get_logger().info("Motion complete")