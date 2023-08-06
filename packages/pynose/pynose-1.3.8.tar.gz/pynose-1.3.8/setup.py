from setuptools import setup
import os
import sys

this_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
# Get the package version from the nose/__version__.py file
with open(os.path.join(this_dir, "nose", "__version__.py"), "rb") as f:
    exec(f.read().decode("utf-8"), about)
VERSION = about["__version__"]

if sys.argv[-1] == "publish":
    reply = None
    input_method = input
    confirm_text = ">>> Confirm release PUBLISH to PyPI? (yes/no): "
    reply = str(input_method(confirm_text)).lower().strip()
    if reply == "yes":
        print("\n*** Checking code health with flake8:\n")
        if sys.version_info >= (3, 9):
            os.system("python -m pip install 'flake8==6.0.0'")
        else:
            os.system("python -m pip install 'flake8==5.0.4'")
        flake8_status = os.system("flake8 --exclude=recordings,temp")
        if flake8_status != 0:
            print("\nWARNING! Fix flake8 issues before publishing to PyPI!\n")
            sys.exit()
        else:
            print("*** No flake8 issues detected. Continuing...")
        print("\n*** Removing existing distribution packages: ***\n")
        os.system("rm -f dist/*.egg; rm -f dist/*.tar.gz; rm -f dist/*.whl")
        os.system("rm -rf build/bdist.*; rm -rf build/lib")
        print("\n*** Installing build: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'build>=0.10.0'")
        print("\n*** Installing pkginfo: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'pkginfo>=1.9.6'")
        print("\n*** Installing twine: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'twine>=4.0.2'")
        print("\n*** Installing tqdm: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade tqdm")
        print("\n*** Rebuilding distribution packages: ***\n")
        os.system("python -m build")  # Create new tar/wheel
        print("\n*** Publishing The Release to PyPI: ***\n")
        os.system("python -m twine upload dist/*")  # Requires ~/.pypirc Keys
        print("\n*** The Release was PUBLISHED SUCCESSFULLY to PyPI! :) ***\n")
    else:
        print("\n>>> The Release was NOT PUBLISHED to PyPI! <<<\n")
    sys.exit()

addl_args = dict(
    packages=[
        "nose", "nose.ext", "nose.plugins", "nose.sphinx", "nose.tools"
    ],
    scripts=["bin/nosetests"],
)

setup(
    name="pynose",
    version=VERSION,
    author="Michael Mintz",
    author_email="mdmintz@gmail.com",
    description="pynose fixes nose to extend unittest and make testing easier",
    long_description="""
    pynose is a updated version of nose, originally created by Jason Pellerin.
    This version of nose is compatible with Python 3.6+ (including 3.11 & up).

    Changes from legacy "nose" include:
    * Fixes "AttributeError: module 'collections' has no attribute 'Callable'."
    * Fixes all "flake8" issues from the original "nose".
    * The default logging level was changed to hide "debug"-level logs.
    * The unit tests are no longer included with the repo to save space.

    The original description of "nose":

    nose extends the test loading and running features of unittest, making
    it easier to write, find and run tests.

    By default, nose will run tests in files or directories under the current
    working directory whose names include "test" or "Test" at a word boundary
    (like "test_this" or "functional_test" or "TestClass" but not
    "libtest"). Test output is similar to that of unittest, but also includes
    captured stdout output from failing tests, for easy print-style debugging.

    These features, and many more, are customizable through the use of
    plugins. Plugins included with nose provide support for doctest, code
    coverage and profiling, flexible attribute-based test selection,
    output capture and more. More information about writing plugins may be
    found on in the nose API documentation, here:
    https://nose.readthedocs.io/en/latest/
    """,
    license="MIT",
    keywords="test unittest doctest automatic discovery",
    url="https://nose.readthedocs.io/en/latest/",
    package_data={"": ["*.txt"]},
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
    ],
    **addl_args
)
