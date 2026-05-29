def main():
    rclpy.init()

    robot = ZA6Robot()

    robot.home()

    rclpy.spin(robot)

    robot.shutdown()

    rclpy.shutdown()


if __name__ == "__main__":
    main()