from setuptools import find_packages, setup

package_name = 'dc_motor_experiments'

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
    maintainer='d3im3r',
    maintainer_email='demiranda@unal.edu.co',
    description='Nodes for step response excitation, data acquisition, and real-time visualization.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'step_response = dc_motor_experiments.step_response:main',
            'velocity_monitor = dc_motor_experiments.velocity_monitor:main',
            'data_logger = dc_motor_experiments.data_logger:main',
        ],
    },
)
