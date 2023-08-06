from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cdataml",
    version='0.5.3',
    packages = ['cdataml'],
    url="https://github.com/joshuandwilliams/cdataml",
    license='LICENSE.txt',
    author="Joshua Williams",
    author_email="<jowillia@nbi.ac.uk>",
    description='Cell Death Area Data Collection for Machine Learning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['scripts/cdataml-test-script'],
    include_package_data=True,
    package_data={"cdataml": ['lesion_score_key.tif']},
    install_requires=['opencv-python', 'pandas', 'natsort', 'importlib_resources']
)
