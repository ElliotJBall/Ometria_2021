from setuptools import setup, find_packages


with open("README.rst") as f:
    readme = f.read()

setup(
    name="Elliot Ometria",
    version="0.1.0",
    description="Elliot Ometria software engineer take home 2021",
    long_description=readme,
    author="Elliot Ball",
    author_email="elliotjordball@gmail.com",
    url="https://github.com/ElliotJBall/Ometria_2021",
    packages=find_packages(exclude=("tests", "docs")),
)
