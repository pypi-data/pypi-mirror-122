import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

exec(compile(open('atrcopy/_version.py').read(), 'atrcopy/_version.py', 'exec'))
exec(compile(open('atrcopy/_metadata.py').read(), 'atrcopy/_metadata.py', 'exec'))

with open("README.rst", "r") as fp:
    long_description = fp.read()

if sys.platform.startswith("win"):
    scripts = ["scripts/atrcopy.bat"]
else:
    scripts = ["scripts/atrcopy"]

setup(name="atrcopy",
        version=__version__,
        author=__author__,
        author_email=__author_email__,
        url=__url__,
        packages=["atrcopy"],
        include_package_data=True,
        scripts=scripts,
        entry_points={"sawx.loaders": 'atrcopy = atrcopy.omnivore_loader'},
        description="Utility to manage file systems on Atari 8-bit (DOS 2) and Apple ][ (DOS 3.3) disk images.",
        long_description=long_description,
        license="MPL 2.0",
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
            "Topic :: Software Development :: Libraries",
            "Topic :: Utilities",
        ],
        python_requires = '>=3.6',
        install_requires = [
            'numpy',
        ],
        tests_require = [
            'pytest>3.0',
            'coverage',
            'pytest.cov',
        ],
    )
