import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


class CleanCommand(setuptools.Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


setuptools.setup(
    name="rescape_python_helpers",
    version="0.0.64",
    author="Andy Likuski",
    author_email="andy@likuski.org",
    description="Functional and geospatial helpers for Rescape projects. Pyramda library by from https://github.com/jackfirth/pyramda incorporated in after it stopped working with new Python relases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/calocan/rescape-python-helpers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'clean': CleanCommand,
    },
    install_requires=[
        'pyramda',
        'inflection',
        'deepmerge'
    ],
)
