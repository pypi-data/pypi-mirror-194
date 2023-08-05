import os

from setuptools import setup

requires = open("requirements.txt", "r").readlines() if os.path.exists("requirements.txt") else open("./arizon_usb_apiserver.egg-info/requires.txt", "r").readlines()
print("#-------------------    ", str(os.listdir("./")))
setup(
    name="arizon-usb-apiserver",
    version="0.4.0",
    author="davidliyutong",
    author_email="davidliyutong@sjtu.edu.cn",
    description="Driver for Arizona USB Pressure Sensor",
    packages=[
        "arizon_usb_apiserver",
        "arizon_usb_apiserver.apiserver",
        "arizon_usb_apiserver.client",
        "arizon_usb_apiserver.client.restful",
        "arizon_usb_apiserver.client.grpc",
        "arizon_usb_apiserver.cmd",
        "arizon_usb_apiserver.grpc"
    ],
    python_requires=">=3.7",
    install_requires=requires,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown"
)