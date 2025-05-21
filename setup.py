from setuptools import setup

setup(
    name='terraform-aws-manager',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'PyYAML>=5.4',
    ],
    entry_points={
        'console_scripts': [
            'tfaws=main:main',
        ],
    },
    author='Jeff Silver',
    description='Automate Terraform workflows in AWS using Python.',
    license='MIT',
)
