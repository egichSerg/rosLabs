from setuptools import find_packages, setup

package_name = 'fullname'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yoy',
    maintainer_email='e.sergeev@g.nsu.ru',
    description='names sum',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'SummFullName = fullname.service_member_function:main',
            'client = fullname.client_member_function:main',
        ],
    },
)
