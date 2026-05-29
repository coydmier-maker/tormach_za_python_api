from geometry_msgs.msg import PoseStamped


def make_pose(x, y, z, qx=0.0, qy=0.0, qz=0.0, qw=1.0, frame="base_link"):

    pose = PoseStamped()
    pose.header.frame_id = frame

    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z

    pose.pose.orientation.x = qx
    pose.pose.orientation.y = qy
    pose.pose.orientation.z = qz
    pose.pose.orientation.w = qw

    return pose