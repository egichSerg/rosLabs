from setuptools import find_packages, setup

package_name = 'robot_logic'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['launch/circle.launch.py']),
        ('share/' + package_name, ['launch/random.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yoy',
    maintainer_email='e.sergeev@g.nsu.ru',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'circle=robot_logic.circle_movement:main',
            'random=robot_logic.random_movement:main',
        ],
    },
)
