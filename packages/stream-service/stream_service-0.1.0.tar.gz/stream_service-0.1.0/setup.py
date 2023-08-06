from setuptools import setup

setup(
    name='stream_service',
    version='0.1.0',
    packages=['stream_service', 'stream_service.lib', 'stream_service.examples'],
    package_dir={'': 'src'},
    url='https://github.com/BR1py/stream_service',
    license='MIT',
    author='B_R',
    author_email='br_development@posteo.org',
    description='Client/Server implementation for data streaming in channels based on python >= 3.5'
)
