from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='repmsa',
    py_modules=['repmsa'],
    version='0.1.6',
    description='Finding the representetive seq in MSA',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Muhammet Celik',
    license='MIT',
    install_requires=REQUIREMENTS,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.5'],
    test_suite='tests',
)
