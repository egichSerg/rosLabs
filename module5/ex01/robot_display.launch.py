from launch import LaunchDescription
from launch.substitutions import Command

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

import os


def generate_launch_description():
    ld = LaunchDescription()

    default_path = os.getcwd()
    model_path = os.path.join(default_path, 't1.urdf')
    rviz_path = os.path.join(default_path, 'urdf.rviz')

    robot_description_content = ParameterValue(Command(['xacro ', model_path]), value_type=str)

    robot_state_publisher_node = Node(package='robot_state_publisher',
                                      executable='robot_state_publisher',
                                      parameters=[{
                                          'robot_description': robot_description_content,
                                      }])
    ld.add_action(robot_state_publisher_node)

    ld.add_action(Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
    ))

    ld.add_action(Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_path]
    ))

    return ld
