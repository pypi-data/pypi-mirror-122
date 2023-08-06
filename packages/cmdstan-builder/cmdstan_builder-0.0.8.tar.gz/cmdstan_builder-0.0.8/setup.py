import os
from subprocess import call

import setuptools
from setuptools.dist import Distribution

MIN_PYTHON_VERSION = "3.7"
SETUP_REQUIRES = ["wheel"]

DISTNAME = "cmdstan_builder"
DESCRIPTION = "A package to build the cmdstan binary and use it as an extension to EvalML"
LICENSE = "BSD-3-Clause"
VERSION = "0.0.8"

# Source: https://stackoverflow.com/a/62668026
# For now, we will upload a different wheel for both OSX and linux but
# do we actually need separate wheels?
class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True

with open("README.md", "r") as fh:
    long_description = fh.read()


def setup_package():
    # Install in a directory called stan
    call('pip install cmdstanpy==0.9.68', shell=True)
    import cmdstanpy

    cmdstanpy.install_cmdstan(dir=f"./{DISTNAME}/stan/", version="2.28.0")

    # Find all the build files and set them as package_data
    files = []
    for r, _, f in os.walk(f"./{DISTNAME}/stan/"):
        for file_ in f:
            files.append(os.path.join(r, file_))
    files = [f.split(f"./{DISTNAME}/")[1] for f in files]

    call(f'CMDSTAN={os.getcwd()}/{DISTNAME}/stan/cmdstan-2.28.0 STAN_BACKEND=CMDSTANPY pip install prophet==1.0.1', shell=True)
    call("pip uninstall pystan -y", shell=True)

    metadata = dict(
        name=DISTNAME,
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Alteryx, Inc.',
        author_email='support@featurelabs.com',
        license=LICENSE,
        version=VERSION,
        url='https://github.com/alteryx/cmdstan_ext/',
        python_requires=">={}".format(MIN_PYTHON_VERSION),
        setup_requires=SETUP_REQUIRES,
        install_requires=open("requirements.txt").readlines(),
        packages=setuptools.find_packages(),
        include_package_data=True,
        package_data={DISTNAME: files},
        distclass=BinaryDistribution
    )

    from setuptools import setup
    setup(**metadata)


if __name__ == "__main__":
    setup_package()
