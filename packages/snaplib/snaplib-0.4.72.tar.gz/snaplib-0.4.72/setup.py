from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
                "wheel>=0.3", 
                "twine>=1", 
                "pandas>=1", 
                "numpy>=1", 
                "matplotlib>=3", 
                "lightgbm>=3", 
                "sklearn>=1", 
                "seaborn>=0.12", 
                ]

setup(
    name="snaplib",
    version="0.4.72",
    author="Artsiom Kolas",
    author_email="artyom.kolas@gmail.com",
    description="Data preprocessing lib",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/kolasdevpy/snaplib",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)

