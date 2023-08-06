from setuptools import setup, find_packages


def read(f):
    return open(f, 'r', encoding='utf-8').read()


setup(
    name="metabootstrap",
    version="1.0.1",
    url="https://bitbucket.org/isnstudio/metabootstrap/src/master/",
    description="Apis for Django Rest Framework made for Webix clients",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="ISN Studio",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.8",
    project_urls={
        "Source": "https://bitbucket.org/isnstudio/metabootstrap/src/master/"
    }
)
