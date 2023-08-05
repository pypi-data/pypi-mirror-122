from setuptools import find_packages, setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='repmsa',
    py_modules=['repmsa'],
    version='0.1.4',
    description='Finding the representetive seq in MSA',
    author='Muhammet Celik',
    license='MIT',
    install_requires=REQUIREMENTS,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.5'],
    test_suite='tests',
)
