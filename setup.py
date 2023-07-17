from setuptools import setup
import os

def read_version():
    here = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(here, 'mqttapi', '__version__.py')
    namespace = {}
    with open(version_file, 'r') as f:
        exec(f.read(), namespace)
    return namespace['__version__']

setup(
    name='mqttapi',
    version=read_version(),
    description='simplified mqtt library',
    author='Davi Luna',
    author_email='Sdavi738@gmail.com',
    packages=['mqttapi'],
    install_requires=[
    'mysql-connector-python',
    'paho-mqtt',
    'asyncio',
    'websockets',
    'websocket'
    ],
    keywords=[
        "mqtt api",
        "mosquitto api",
        "real-time",
        "messaging",
        "simplified mqtt",
        "paho-mqtt api",
        ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    url='https://github.com/davifurao/mqttapi',
)
