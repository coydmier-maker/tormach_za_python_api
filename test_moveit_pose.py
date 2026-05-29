import rclpy
from geometry_helpers import make_pose
from moveit_pose_client import MoveItPoseClient


def main():

    rclpy.init()

    client = MoveItPoseClient()

    pose = make_pose(
        0.4, 0.0, 0.3,
        0.0, 0.0, 0.0, 1.0
    )

    client.send_pose_goal(pose, group_name="arm")

    client.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()