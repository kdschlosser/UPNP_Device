# -*- coding: utf-8 -*-

from setuptools import setup
import UPNP_Device


setup(
    name=UPNP_Device.__title__,
    version=UPNP_Device.__version__,
    description=UPNP_Device.__doc__,
    url=UPNP_Device.__url__,
    author=UPNP_Device.__author__,
    author_email=UPNP_Device.__author_email__,
    long_description=open("README.md").read(),
    packages=["UPNP_Device"],
    install_requires=['requests', 'lxml', 'six', 'ifaddr'],
    entry_points={
        "console_scripts": [
            "UPNP_Device=UPNP_Device.__main__:main",
            "upnp_device=UPNP_Device.__main__:main"
        ]
    },
)
