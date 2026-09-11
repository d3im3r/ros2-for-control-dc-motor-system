from setuptools import find_packages, setup

package_name = 'dc_motor_control'

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
    description='Controllers for DC motor closed-loop speed regulation.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'pi_controller = dc_motor_control.pi_controller:main',
            'pid_controller = dc_motor_control.pid_controller:main',
        ],
    },
)
