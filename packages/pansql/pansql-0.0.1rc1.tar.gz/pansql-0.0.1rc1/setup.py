from distutils.core import setup
from setuptools import find_packages

setup(
    name="pansql",
    version="0.0.1rc1",
    author="Harshad Hegde",
    author_email="hhegde@lbl.gov",
    url="https://github.com/hrshdhgd/pansql/",
    license="MIT",
    packages=find_packages(),
    package_dir={"pansql": "pansql"},
    package_data={"pansql": ["data/*.csv"]},
    description="sqldf for pandas",
    long_description=open("README.rst").read(),
    install_requires=['numpy', 'pandas', 'sqlalchemy'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)
