import setuptools


setuptools.setup(
    name='jsonformat',
    version='0.0.1',
    license="MIT",
    entry_points={
        'console_scripts': ['jsonformat=jsonformat:cli'],
    },
    author='Alex Pylypenko',
    description='Simple command line utility to format json files.',
    packages=['jsonformat'],
    install_requires=[
        'setuptools',
        'pip'
    ],
    python_requires='>=3.3'
)