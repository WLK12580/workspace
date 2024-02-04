from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            namespace='turtlesim1',
            executable='turtlesim_node',
            name='sim'
        ),
        Node(
            package="turtlesim",
            namespace="turtlesim2",
            executable='turtlesim_node',
            name='sim'

        ),
        Node(
            package='turtlesim',
            executable='mimic',
            name='mimic',
            remappings=[
                ('/input/pose', '/turtlesim1/turtle1/pose'),  #mimic的主题/input/pose映射到/turtlesim1/turtle1/pose，
                ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'), #mimic的主题/output/cmd_vel投射到/turtlesim2/turtle1/cmd_vel
            ]) #/turtlesim1/turtle1/pose和/turtlesim2/turtle1/cmd_vel是topic,
            # 这意味着 mimic 将订阅 /turtlesim1/sim 的姿势主题，并将其重新发布，供 /turtlesim2/sim 的速度命令主题订阅。换句话说，turtlesim2 将模仿 turtlesim1 的
        ])