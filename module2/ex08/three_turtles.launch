#!/usr/bin/env python3

import os

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    cwd = os.getcwd()
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim',
            namespace='turtlesim1',
            parameters=[cwd + '/turtlesim1.params.yaml'],
            remappings=[('/turtlesim1/turtle1/cmd_vel', '/turtle1/cmd_vel')]),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim',
            namespace='turtlesim2',
            parameters=[cwd + '/turtlesim2.params.yaml']),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim',
            namespace='turtlesim3',
            parameters=[cwd + '/turtlesim3.params.yaml']),
        Node(
            package='turtlesim',
            executable='mimic',
            name='mimic',
            namespace='mimic',
            remappings=[
                ('/mimic/input/pose', '/turtlesim1/turtle1/pose'),
                ('/mimic/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel')]),
        Node(
            package='turtlesim',
            executable='mimic',
            name='mimic2',
            namespace='mimic',
            remappings=[
                ('/mimic/input/pose', '/turtlesim2/turtle1/pose'),
                ('/mimic/output/cmd_vel', '/turtlesim3/turtle1/cmd_vel')])
    ])
