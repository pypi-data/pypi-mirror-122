from setuptools import setup, find_packages


requirements = ["xlwings==0.24.7","Excelutilities","openpyxl","PySimpleGUI"]
#The xlwings version has to be strict to work with the workbook setup

setup(
    name="Excelutilities",
    version="0.0.1",
    author="Ethan Horsfall",
    author_email="ethan.horsfall@gmail.com",
    description="Arbitrage master sheet for amazon",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)