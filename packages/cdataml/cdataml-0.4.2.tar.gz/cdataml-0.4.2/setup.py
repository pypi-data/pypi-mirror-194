from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cdataml",
    version='0.4.2',
    author="Joshua Williams",
    author_email="<jowillia@nbi.ac.uk>",
    description='CDA Data for Machine Learning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joshuandwilliams/cdataml",
    install_requires=['opencv-python', 'pandas', 'natsort', 'importlib_resources'],
    packages = find_packages(),
    package_data={"data": ["*.tif"]},
    keywords=['python', 'plant pathology', 'cell death', 'machine learning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
