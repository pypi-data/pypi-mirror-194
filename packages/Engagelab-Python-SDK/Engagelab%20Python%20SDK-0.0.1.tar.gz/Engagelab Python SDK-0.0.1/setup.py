# coding: utf-8

from setuptools import setup, find_packages  # noqa: H301

NAME = "Engagelab Python SDK"
VERSION = "0.0.1"

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="World-leading Customer Engagement Platform",
    author="catroll",
    author_email="",
    url="https://docs.engagelab.com",
    keywords=["Email", ],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
